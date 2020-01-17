"""
The lunch pop-up for getting the lunch times.
"""

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.4.7'

import shotgun_api3 as sgapi
import os
import sys
import getopt
from PySide import QtGui, QtCore
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta
from dateutil import parser
import time
import webbrowser

# Time Lord Libraries
from bin.time_continuum import continuum
from bin.companions import companions
import bin.configuration
import bin.shotgun_collect

from ui import time_lord_sheets as tls
from ui import time_lord_edit_timesheet as editor

config = bin.configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'sheets.log'
log_root = os.path.join(sys.path[0], 'logs')
if not os.path.exists(log_root):
    os.makedirs(log_root)
log_path = os.path.join(log_root, log_file)
debug = config['debug_logging']
if debug == 'True' or debug == 'true' or debug == True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('sheets')
logger.setLevel(level=level)
fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                              backupCount=int(config['log_days']))
fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
fh.setFormatter(fm)
logger.addHandler(fh)

logger.info('Sheets Utility has started.')

# --------------------------------------------------------------------------------------------------
# Setup Shotgun Connection
# --------------------------------------------------------------------------------------------------
sg = sgapi.Shotgun(config['sg_url'], config['sg_name'], config['sg_key'])
logger.debug('Shotgun is connected.')

# --------------------------------------------------------------------------------------------------
# Connect Time Lord Components
# --------------------------------------------------------------------------------------------------
# setup continuum
tl_time = continuum(sg, config=config, sub='sheets')

# Setup and get users
users = companions(sg, config=config, sub='sheets')
user = users.get_user_from_computer()

# setup shotgun data connection
sg_data = bin.shotgun_collect.sg_data(sg, config=config, sub='sheets')

lunch_proj_id = int(config['admin_proj_id'])
lunch_task_id = sg_data.get_lunch_task(lunch_proj_id=lunch_proj_id, task_name=config['lunch'])
if lunch_task_id:
    lunch_task_id = int(lunch_task_id['id'])


class sheet_signals(QtCore.QObject):
    message = QtCore.Signal(str)
    update = QtCore.Signal(list)
    req_update = QtCore.Signal(dict)


class sheet_engine(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.kill_it = False
        self.signals = sheet_signals()

        # Signal connections
        self.signals.req_update.connect(self.prep_update)

    def prep_update(self, data):
        # Create Database to return
        print('Update has been requested.  Processing...')
        update_list = []
        if data:
            start_date = data['start_date']
            end_date = data['end_date']
            whose_timesheet = data['whose_timesheet']
            sort_by = data['sort_by']
            order = data['order']

            if order == 0:
                order = 'asc'
            else:
                order = 'desc'

            if whose_timesheet == 0:
                users_list = users.get_all_users()
            else:
                users_list = [users.get_user_by_id(uid=whose_timesheet)]

            # Sort by Date is True

            # Get the date difference
            start_month = start_date.month()
            start_day = start_date.day()
            start_year = start_date.year()
            end_month = end_date.month()
            end_day = end_date.day()
            end_year = end_date.year()
            start_date = parser.parse('%02d/%02d/%02d' % (start_month, start_day, start_year))
            end_date = parser.parse('%02d/%02d/%02d' % (end_month, end_day, end_year))

            if order == 'desc':
                date_diff = start_date - end_date
            else:
                date_diff = end_date - start_date
            date_diff = date_diff.days

            if sort_by:
                # Iterate through the days to start building the update_list
                print('Date sorting the timesheets')
                for x in range(0, int(date_diff) + 1):
                    if order == 'desc':
                        date_record = end_date - timedelta(days=x)
                    else:
                        date_record = start_date + timedelta(days=x)
                    timesheet_list = {}
                    for this_user in users_list:
                        user_name = this_user['name']
                        # print date_record, order
                        timesheets = tl_time.get_all_user_timesheets_by_date(user=this_user,
                                                                             date=date_record,
                                                                             order=order)
                        # print timesheets
                        timesheet_list[user_name] = timesheets
                    update_list.append({date_record: timesheet_list})
                    del timesheet_list
            else:
                # Sort by Person is True
                print('Person sorting the timesheets')
                for this_user in users_list:
                    user_name = this_user['name']
                    timesheet_list = {}
                    for x in range(0, int(date_diff) + 1):
                        if order == 'desc':
                            date_record = end_date - timedelta(days=x)
                        else:
                            date_record = start_date + timedelta(days=x)
                        timesheets = tl_time.get_all_user_timesheets_by_date(user=this_user,
                                                                             date=date_record,
                                                                             order=order)
                        # print timesheets
                        timesheet_list[date_record] = timesheets
                    update_list.append({user_name: timesheet_list})
                    del timesheet_list
        print('Returning Update list...')
        print('update list length: %s' % len(update_list))
        self.signals.update.emit(update_list)
        print('Update list returned.')
        return update_list


class sheets(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.engine = sheet_engine()

        self.ui = tls.Ui_TimeSheets()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
        self.setWindowTitle('Time Lord Sheets v%s' % __version__)

        # set the user name
        self.ui.artist_name.setText(user['name'])

        # Set Whose_Timesheet
        self.ui.whose_timesheets.clear()
        self.ui.whose_timesheets.addItem('My Timesheets', user['id'])
        if user['permission_rule_set']['name'] in config['permissions']:
            self.ui.whose_timesheets.addItem('All Artists', 0)
            get_all_artists = users.get_all_users()
            for artist in get_all_artists:
                self.ui.whose_timesheets.addItem(artist['name'], artist['id'])

        self.ui.editor_progress.setValue(0)
        self.ui.editor_status.setText('')

        # Set the default start and end times
        start_time = (datetime.now() - timedelta(weeks=2)).date()
        end_time = datetime.now().date()
        self.ui.start_date.setDate(start_time)
        self.ui.end_date.setDate(end_time)

        # Replace Saved settings
        self.settings = QtCore.QSettings(__author__, 'TimeSheets')
        self.saved_window_position = self.settings.value('geometry', '')
        self.saved_whose_timesheet = self.settings.value('whose_timesheet', '.')
        self.saved_sort_by = self.settings.value('sort_by', '.')
        self.saved_order = self.settings.value('order', '.')
        self.restoreGeometry(self.saved_window_position)

        # Connect buttons
        self.ui.update_btn.clicked.connect(self.request_update)

        # Set the saved settings.
        try:
            self.ui.whose_timesheets.setCurrentIndex(self.saved_whose_timesheet)
            self.ui.order.setCurrentIndex(self.saved_order)
            if self.saved_sort_by:
                self.ui.date_rdo.setChecked()
            else:
                self.ui.person_rdo.setChecked()
        except:
            pass

        self.engine.start()

        # Setup connections.
        self.engine.signals.update.connect(self.update_list)
        self.request_update()

    def request_update(self):
        print('Requesting Update...')
        # Emit the initial data to start the first load of the data.  Based on the initial settings.
        whose_timesheet = self.ui.whose_timesheets.itemData(self.ui.whose_timesheets.currentIndex())
        sort_by = self.ui.date_rdo.isChecked()
        order = self.ui.order.currentIndex()
        start_date = self.ui.start_date.date()
        end_date = self.ui.end_date.date()
        updata = {
            'whose_timesheet': whose_timesheet,
            'sort_by': sort_by,
            'order': order,
            'start_date': start_date,
            'end_date': end_date
        }
        self.engine.signals.req_update.emit(updata)
        print('Update requested.')

    def update_list(self, data=None):
        if data:
            self.ui.sheet_tree.clear()
            self.ui.sheet_tree.setHeaderLabels(['TS ID', 'Project', 'Asset', 'Task', 'Start', 'End',
                                                'Duration', 'Edit'])
            # self.ui.sheet_tree.setColumnWidth(150, 150)
            self.ui.sheet_tree.setAlternatingRowColors(True)

            # Rummage through the data
            all_rows = []

            all_starts = []
            all_ends = []
            all_projects = []
            all_entities = []
            all_tasks = []
            all_ts_ids = []
            all_durations = []
            all_edits = []

            for record in data:
                main_key = record.keys()[0]
                block_data = record[main_key]
                sorted_by = type(main_key)
                if sorted_by == datetime:
                    main_key = str(main_key.date())
                # print main_key

                add_main_key = QtGui.QTreeWidgetItem()
                add_main_key.setText(0, main_key)

                for key, val in block_data.items():
                    # print key
                    if type(key) == datetime:
                        key = str(key.date())
                    add_key = QtGui.QTreeWidgetItem()
                    add_key.setFirstColumnSpanned(False)
                    add_key.setText(0, key)

                    # Set an incrementer for the next loop
                    for timesheet in val:
                        # sheet = sheet_editor_button(self.ui.sheet_tree, add_key, timesheet)
                        # add_key.addChild(sheet)
                        # print(sheet)
                        task_id = timesheet['entity']['id']
                        task = timesheet['entity']['name']
                        project = timesheet['project']['name']
                        project_id = timesheet['project']['id']
                        entity = sg_data.get_entity_from_task(task_id=task_id)
                        entity_name = entity['entity']['name']
                        entity_id = entity['entity']['id']
                        start = timesheet['sg_task_start']
                        start = datetime.strftime(start, '%I:%M %p')
                        # print(d)
                        if timesheet['sg_task_end']:
                            end = timesheet['sg_task_end']
                        else:
                            end = datetime.now()
                        end = datetime.strftime(end, '%I:%M %p')
                        duration = timesheet['duration'] / 60.0

                        time_table = QtGui.QTreeWidgetItem(add_key, [str(timesheet['id']),
                                                                     project,
                                                                     entity_name,
                                                                     task,
                                                                     'start: %s' % start,
                                                                     'end: %s' % end,
                                                                     'total: %0.2f hrs' % duration,
                                                                     'Double Click To Edit'
                                                                     ]
                                                           )
                        add_key.addChild(time_table)
                    add_main_key.addChild(add_key)

                self.ui.sheet_tree.addTopLevelItem(add_main_key)

            self.ui.sheet_tree.itemDoubleClicked.connect(self.edit_timesheet)
            self.ui.sheet_tree.expandAll()
            self.ui.sheet_tree.resizeColumnToContents(True)

    def edit_timesheet(self, data=None):
        self.ui.editor_status.setText('Edit triggered!')
        self.ui.editor_progress.setValue(10)
        if data:
            ts_id = data.text(0)
            project = data.text(1)
            entity = data.text(2)
            task = data.text(3)

            if ts_id:
                print('Getting timesheet....')
                self.ui.editor_status.setText('Getting timesheet....')
                self.ui.editor_progress.setValue(25)
                edit_timesheet = tl_time.get_timesheet_by_id(tid=ts_id)
                self.ui.editor_status.setText('Timesheet Received!')
                self.ui.editor_progress.setValue(65)
                print('Timesheet recieved.')
                if edit_timesheet:
                    start = edit_timesheet['sg_task_start']
                    end = edit_timesheet['sg_task_end']
                else:
                    start = None
                    end = None
                print('Sending to the Editor...')

                self.ui.editor_status.setText('Sending to the Editor...')
                self.ui.editor_progress.setValue(100)
                time_editor.edit_timesheet(ts_id=ts_id, proj=project, entity=entity, task=task, start=start, end=end)
                self.ui.editor_status.setText('')
                self.ui.editor_progress.setValue(0)

    def update_saved_settings(self):
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('sort_by', self.ui.date_rdo.isChecked())
        self.settings.setValue('whose_timesheet', self.ui.whose_timesheets.currentIndex())
        self.settings.setValue('order', self.ui.order.currentIndex())

    def closeEvent(self, *args, **kwargs):
        self.update_saved_settings()
        time.sleep(0.5)


class time_editor(QtGui.QDialog):
    def __init__(self, Editor=None, ts_id=None, proj=None, entity=None, task=None, start=None, end=None):
        super(time_editor, self).__init__(Editor)

        if not start:
            start = datetime.now()
        if not end:
            end = datetime.now()

        # Editor.setStyleSheet("background-color: rgb(100, 100, 100);\n"
        #                      "color: rgb(230, 230, 230);")
        self.verticalLayout = QtGui.QVBoxLayout(Editor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtGui.QLabel(Editor)
        self.title.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";")
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.project = QtGui.QLabel(Editor)
        self.project.setObjectName("project")
        self.verticalLayout.addWidget(self.project)
        self.entity = QtGui.QLabel(Editor)
        self.entity.setObjectName("entity")
        self.verticalLayout.addWidget(self.entity)
        self.task = QtGui.QLabel(Editor)
        self.task.setObjectName("task")
        self.verticalLayout.addWidget(self.task)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.start_label = QtGui.QLabel(Editor)
        self.start_label.setObjectName("start_label")
        self.horizontalLayout.addWidget(self.start_label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.start = QtGui.QDateTimeEdit(Editor)
        self.start.setCalendarPopup(True)
        self.start.setObjectName("start")
        self.horizontalLayout.addWidget(self.start)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.end_label = QtGui.QLabel(Editor)
        self.end_label.setObjectName("end_label")
        self.horizontalLayout_2.addWidget(self.end_label)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.end = QtGui.QDateTimeEdit(Editor)
        self.end.setObjectName("end")
        self.horizontalLayout_2.addWidget(self.end)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(Editor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Discard | QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        # self.retranslateUi(Editor)
        # QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Editor.accept)
        # QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Editor.reject)
        # QtCore.QMetaObject.connectSlotsByName(Editor)
        self.start.setDateTime(start)
        self.end.setDateTime(end)

    @staticmethod
    def edit_timesheet(parent=None, ts_id=None, proj=None, entity=None, task=None, start=None, end=None):
        editor = time_editor(parent, ts_id, proj, entity, task, start, end)
        result = editor.exec_()
        return result


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('AdamBenson')
    app.setOrganizationDomain('adamdbenson.com')
    app.setApplicationName('Sheets')
    splash_pix = QtGui.QPixmap('ui/resources/Time_Lord_Logo.png')
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    o = sheets()
    o.show()
    splash.finish(o)
    sys.exit(app.exec_())

