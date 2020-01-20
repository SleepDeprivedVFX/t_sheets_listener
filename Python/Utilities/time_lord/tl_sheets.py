"""
The lunch pop-up for getting the lunch times.
"""

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.4.8'

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
    progress = QtCore.Signal(list)
    daily_total = QtCore.Signal(float)
    weekly_total = QtCore.Signal(float)


class sheet_engine(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.kill_it = False
        self.signals = sheet_signals()

        # Signal connections
        self.signals.req_update.connect(self.prep_update)

    def kill(self):
        self.kill_it = True

    def prep_update(self, data):
        # Create Database to return
        logger.debug('Update has been requested.  Processing...')
        progress_total = 20
        self.signals.progress.emit(['Beginning update...', progress_total])
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

            record_totals = date_diff + len(users_list)
            progress_add = record_totals / 40  # Percentage of the progress bar this will cover

            if sort_by:
                # Iterate through the days to start building the update_list
                logger.debug('Date sorting the timesheets')
                for x in range(0, int(date_diff) + 1):
                    if order == 'desc':
                        date_record = end_date - timedelta(days=x)
                    else:
                        date_record = start_date + timedelta(days=x)
                    timesheet_list = {}
                    for this_user in users_list:
                        user_name = this_user['name']
                        progress_total += progress_add
                        self.signals.progress.emit(['Getting timesheets for %s' % user_name, progress_total])
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
                logger.debug('Person sorting the timesheets')
                for this_user in users_list:
                    user_name = this_user['name']
                    timesheet_list = {}
                    for x in range(0, int(date_diff) + 1):
                        if order == 'desc':
                            date_record = end_date - timedelta(days=x)
                        else:
                            date_record = start_date + timedelta(days=x)
                        progress_total += progress_add
                        self.signals.progress.emit(['Getting timesheets for %s' % user_name, progress_total])
                        timesheets = tl_time.get_all_user_timesheets_by_date(user=this_user,
                                                                             date=date_record,
                                                                             order=order)
                        # print timesheets
                        timesheet_list[date_record] = timesheets
                    update_list.append({user_name: timesheet_list})
                    del timesheet_list
        logger.debug('Returning Update list...')

        progress_total = 65
        self.signals.progress.emit(['Sending the updated list...', progress_total])
        logger.debug('update list length: %s' % len(update_list))
        self.signals.update.emit(update_list)
        logger.debug('Update list returned.')
        return update_list

    def update_totals(self):
        while not self.kill_it:
            daily_total = tl_time.get_daily_total(user=user, lunch_id=lunch_task_id)
            weekly_total = tl_time.get_weekly_total(user=user, lunch_id=lunch_task_id)
            self.signals.daily_total.emit(daily_total)
            self.signals.weekly_total.emit(weekly_total)
            time.sleep(20)

    def run(self, *args, **kwargs):
        self.update_totals()


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
        self.engine.signals.progress.connect(self.update_progress)
        self.engine.signals.daily_total.connect(self.update_daily_total)
        self.engine.signals.weekly_total.connect(self.update_weekly_total)

        # NOTE: Temporary for quicker release, but the following need to go once fixed
        self.ui.sort_by.hide()
        self.ui.export_btn.setStyleSheet('color: rgb(120, 120, 120);')
        self.ui.export_btn.setDisabled(True)

        # Set the saved settings.
        try:
            self.ui.whose_timesheets.setCurrentIndex(self.saved_whose_timesheet)
            self.ui.order.setCurrentIndex(self.saved_order)
            if self.saved_sort_by:
                self.ui.date_rdo.setChecked(True)
            else:
                self.ui.person_rdo.setChecked(True)
        except:
            pass
        # NOTE: Also temp
        self.ui.date_rdo.setChecked(True)

        # Setup connections.
        self.engine.signals.update.connect(self.update_list)
        self.request_update()

        self.engine.start()

    def update_daily_total(self, total=None):
        if total:
            daily_total = total
            self.ui.todays_total.setText('%0.2f' % daily_total)

    def update_weekly_total(self, total=None):
        if total:
            weekly_total = total
            self.ui.weeks_total.setText('%0.2f' % weekly_total)

    def request_update(self):
        logger.info('Requesting Update...')
        self.ui.editor_status.setText('Updating Time Sheets')
        self.ui.editor_progress.setValue(5)
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
        self.ui.editor_status.setText('Request sent...')
        self.ui.editor_progress.setValue(15)
        self.engine.signals.req_update.emit(updata)
        logger.debug('Update requested.')

    def update_progress(self, data):
        status = data[0]
        progress = data[1]
        self.ui.editor_status.setText(status)
        self.ui.editor_progress.setValue(int(progress))

    def update_list(self, data=None):
        if data:
            progress_total = 65
            self.update_progress(['Updating UI...', progress_total])
            self.ui.sheet_tree.clear()
            self.ui.sheet_tree.setHeaderLabels(['TS ID', 'Project', 'Asset', 'Task', 'Start', 'End',
                                                'Duration', 'Edit'])
            # self.ui.sheet_tree.setColumnWidth(150, 150)
            self.ui.sheet_tree.setAlternatingRowColors(True)

            record_len = len(data)
            progress_add = record_len / 25

            record_date = datetime.now().date()

            for record in data:
                progress_total += progress_add
                self.update_progress(['Adding timesheets...', progress_total])
                main_key = record.keys()[0]
                block_data = record[main_key]
                sorted_by = type(main_key)
                if sorted_by == datetime:
                    record_date = main_key.date()
                    main_key = str(main_key.date())
                # print main_key

                add_main_key = QtGui.QTreeWidgetItem()
                add_main_key.setText(0, main_key)

                for key, val in block_data.items():
                    # print key
                    if type(key) == datetime:
                        key = str(key.date())
                        record_date = key.date()
                    add_key = QtGui.QTreeWidgetItem()
                    add_key.setFirstColumnSpanned(False)
                    add_key.setText(0, key)
                    daily_total = 0.0
                    add_key.setText(6, 'Daily Total: %0.2f hrs' % daily_total)

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
                        start_date = start.date()
                        if start_date == record_date:
                            start = datetime.strftime(start, '%I:%M %p')
                            # print(d)
                            if timesheet['sg_task_end']:
                                end = timesheet['sg_task_end']
                            else:
                                end = datetime.now()
                            end = datetime.strftime(end, '%I:%M %p')
                            duration = timesheet['duration'] / 60.0
                            if task_id != lunch_task_id:
                                daily_total += (timesheet['duration'] / 60.0)
                            add_key.setText(6, 'Daily Total: %0.2f hrs' % daily_total)

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

            progress_total = 100
            self.update_progress(['Finalizing and expanding...', progress_total])

            self.ui.sheet_tree.itemDoubleClicked.connect(self.edit_timesheet)
            self.ui.sheet_tree.expandAll()
            self.ui.sheet_tree.resizeColumnToContents(True)
            progress_total = 0
            self.update_progress(['', progress_total])

    def edit_timesheet(self, data=None):
        self.ui.editor_status.setText('Edit triggered!')
        self.ui.editor_progress.setValue(10)
        if data:
            try:
                ts_id = int(data.text(0))
                project = data.text(1)
                entity = data.text(2)
                task = data.text(3)

                if ts_id:
                    logger.debug('Getting timesheet....')
                    self.ui.editor_status.setText('Getting timesheet....')
                    self.ui.editor_progress.setValue(25)
                    edit_timesheet = tl_time.get_timesheet_by_id(tid=ts_id)
                    self.ui.editor_status.setText('Timesheet Received!')
                    self.ui.editor_progress.setValue(65)
                    logger.debug('Timesheet recieved.')
                    if edit_timesheet:
                        start = edit_timesheet['sg_task_start']
                        end = edit_timesheet['sg_task_end']
                        _user = edit_timesheet['user']
                    else:
                        start = None
                        end = None
                        _user = None

                    self.ui.editor_status.setText('Sending to the Editor...')
                    self.ui.editor_progress.setValue(100)
                    ts = time_editor(tid=ts_id, proj=project, ent=entity, task=task, start=start, end=end, user=_user)
                    ts.exec_()
                    self.ui.editor_status.setText('')
                    self.ui.editor_progress.setValue(0)
                    if ts.result() == 1:
                        self.ui.sheet_tree.clear()
                        time.sleep(0.5)
                        self.request_update()
            except Exception as e:
                logger.debug('Unable to edit this record: %s' % e)

    def update_saved_settings(self):
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('sort_by', self.ui.date_rdo.isChecked())
        self.settings.setValue('whose_timesheet', self.ui.whose_timesheets.currentIndex())
        self.settings.setValue('order', self.ui.order.currentIndex())

    def closeEvent(self, *args, **kwargs):
        self.update_saved_settings()
        if self.engine.isRunning():
            while self.engine.isRunning():
                self.engine.kill()
                self.engine.quit()
        self.engine.kill_it = True
        time.sleep(0.5)


class time_editor(QtGui.QDialog):
    def __init__(self, parent=None, tid=None, proj=None, ent=None, task=None, start=None, end=None, user=None):
        QtGui.QDialog.__init__(self, parent)

        self.editor = editor.Ui_Editor()
        self.editor.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
        self.setWindowTitle("Time Editor v%s" % __version__)
        self.editor.tid.setText('TID: %s' % tid)
        self.editor.project.setText('PRJ: %s' % proj)
        self.editor.entity.setText('ENT: %s' % ent)
        self.editor.task.setText('TSK: %s' % task)
        self.editor.start.setDateTime(start)
        self.editor.end.setDateTime(end)
        self.user = user

        self.editor.update_btn.clicked.connect(self.update_timesheet)
        self.editor.delete_btn.clicked.connect(self.delete_timesheet)
        self.editor.cancel_btn.clicked.connect(self.reject)

    def update_timesheet(self):
        tid = self.editor.tid.text()
        tid = int(tid.split(': ')[1])
        update = QtGui.QMessageBox()
        update.setText('Are you sure you want to update %s?' % tid)
        update.addButton('Yes', QtGui.QMessageBox.AcceptRole)
        update.addButton('No', QtGui.QMessageBox.RejectRole)
        ret = update.exec_()
        if ret == QtGui.QMessageBox.AcceptRole:
            start = self.editor.start.dateTime().toPython()
            end = self.editor.end.dateTime().toPython()
            logger.debug('Doing update...')
            do_update = tl_time.update_current_times(user=user, tid=tid, start_time=start, end_time=end)
            logger.debug('Updated: %s' % do_update)
            self.accept()
        else:
            logger.debug('Rejected!')
            self.close()

    def delete_timesheet(self):
        tid = self.editor.tid.text()
        tid = int(tid.split(': ')[1])
        delete = QtGui.QMessageBox()
        delete.setText('Are you sure you want to delete TID %s?  This can not be undone!' % tid)
        delete.addButton('Delete', QtGui.QMessageBox.AcceptRole)
        delete.addButton('Cancel', QtGui.QMessageBox.RejectRole)
        ret = delete.exec_()
        if ret == QtGui.QMessageBox.AcceptRole:
            tl_time.delete_timelog_by_id(tid=tid)
            self.accept()
        else:
            logger.debug('Rejected!')
            self.close()


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

