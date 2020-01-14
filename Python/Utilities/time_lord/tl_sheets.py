"""
The lunch pop-up for getting the lunch times.
"""

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.4.6'

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

class sheet_editor_button(QtGui.QTreeWidgetItem):

    def __init__(self, parent, sub, timesheet):
        super(sheet_editor_button, self).__init__(parent)
        task_id = timesheet['entity']['id']
        task = timesheet['entity']['name']
        project = timesheet['project']['name']
        project_id = timesheet['project']['id']
        entity = sg_data.get_entity_from_task(task_id=task_id)
        entity_name = entity['entity']['name']
        entity_id = entity['entity']['id']
        start = timesheet['sg_task_start'].time()
        end = timesheet['sg_task_end'].time()
        duration = timesheet['duration'] / 60.0

        self.ts_id = QtGui.QLabel()
        self.ts_id.setText(str(timesheet['id']))
        self.treeWidget().setItemWidget(self, 0, self.ts_id)

        self.project = QtGui.QLabel()
        self.project.setText(project)
        self.treeWidget().setItemWidget(self, 1, self.project)

        self.entity = QtGui.QLabel()
        self.entity.setText(entity_name)
        self.treeWidget().setItemWidget(self, 2, self.entity)

        self.task = QtGui.QLabel()
        self.task.setText(task)
        self.treeWidget().setItemWidget(self, 3, self.task)

        self.start = QtGui.QTimeEdit()
        self.start.setTime(start)
        self.treeWidget().setItemWidget(self, 4, self.start)

        self.end = QtGui.QTimeEdit()
        self.end.setTime(end)
        self.treeWidget().setItemWidget(self, 5, self.end)

        self.duration = QtGui.QLabel()
        self.duration.setText('%0.2f hrs' % duration)
        self.treeWidget().setItemWidget(self, 6, self.duration)

        self.edit = QtGui.QPushButton()
        self.edit.setText('Edit')
        self.treeWidget().setItemWidget(self, 7, self.edit)

        # time_table = QtGui.QTreeWidgetItem(add_key, [str(timesheet['id']),            # 0
        #                                              project,                         # 1
        #                                              entity_name,                     # 2
        #                                              task,                            # 3
        #                                              'start: %s' % start,             # 4
        #                                              'end: %s' % end,                 # 5
        #                                              'total: %0.2f hrs' % duration,   # 6
        #                                              ''                               # 7
        #                                              ]
        #                                    )


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
                    for timesheet in val:
                        sheet = sheet_editor_button(self.ui.sheet_tree, add_key, timesheet)
                        print(sheet)
                        # task_id = timesheet['entity']['id']
                        # task = timesheet['entity']['name']
                        # project = timesheet['project']['name']
                        # project_id = timesheet['project']['id']
                        # entity = sg_data.get_entity_from_task(task_id=task_id)
                        # entity_name = entity['entity']['name']
                        # entity_id = entity['entity']['id']
                        # start = timesheet['sg_task_start'].time().strftime('%I:%M %p')
                        # end = timesheet['sg_task_end'].time().strftime('%I:%M %p')
                        # duration = timesheet['duration'] / 60.0
                        #
                        # time_table = QtGui.QTreeWidgetItem(add_key, [str(timesheet['id']),
                        #                                              project,
                        #                                              entity_name,
                        #                                              task,
                        #                                              'start: %s' % start,
                        #                                              'end: %s' % end,
                        #                                              'total: %0.2f hrs' % duration,
                        #                                              ''
                        #                                              ]
                        #                                    )
                        # # # time_table.setCheckState(0, QtCore.Qt.CheckState.Unchecked)
                        # print('time_table: ', time_table)
                        # add_key.addChild(time_table)
                        # edit = QtGui.QPushButton('Edit')
                        # # edit.clicked.connect(lambda: self.edit_timesheet(timesheet['id']))
                        # self.ui.sheet_tree.setItemWidget(time_table, 7, edit)

                    add_main_key.addChild(add_key)
                self.ui.sheet_tree.addTopLevelItem(add_main_key)
            self.ui.sheet_tree.expandAll()
            self.ui.sheet_tree.resizeColumnToContents(True)

    def edit_timesheet(self, ts_id=None):
        if ts_id:
            print('ts: %s' % ts_id)

    def update_saved_settings(self):
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('sort_by', self.ui.date_rdo.isChecked())
        self.settings.setValue('whose_timesheet', self.ui.whose_timesheets.currentIndex())
        self.settings.setValue('order', self.ui.order.currentIndex())

    def closeEvent(self, *args, **kwargs):
        self.update_saved_settings()
        time.sleep(0.5)


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

