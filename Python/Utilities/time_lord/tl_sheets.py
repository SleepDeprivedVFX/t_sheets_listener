"""
The lunch pop-up for getting the lunch times.
"""

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.5.1'

import shotgun_api3 as sgapi
import os
import sys
import getopt
from PySide2 import QtGui, QtCore, QtWidgets
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
    req_project_update = QtCore.Signal(str)
    req_entity_update = QtCore.Signal(int)
    req_task_update = QtCore.Signal(dict)
    send_project_update = QtCore.Signal(dict)
    send_entity_update = QtCore.Signal(dict)
    send_task_update = QtCore.Signal(dict)


class sheet_engine(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.kill_it = False
        self.signals = sheet_signals()

        # Signal connections
        self.signals.req_update.connect(self.prep_update)
        self.signals.req_entity_update.connect(self.send_entity_update)
        self.signals.req_task_update.connect(self.send_task_update)

    def kill(self):
        self.kill_it = True

    def send_entity_update(self, proj_id=None):
        logger.debug('Collecting Entities for return')
        if proj_id:
            asset_entities = sg_data.get_project_assets(proj_id=proj_id)
            shot_entities = sg_data.get_project_shots(proj_id=proj_id)
            entities = asset_entities + shot_entities
            self.signals.send_entity_update.emit(entities)

    def send_task_update(self, context=None):
        if context:
            entity_id = context['entity_id']
            entity_name = context['entity_name']
            proj_id = context['proj_id']
            tasks = sg_data.get_entity_tasks(entity_id=entity_id, entity_name=entity_name, proj_id=proj_id)
            if tasks:
                self.signals.send_task_update.emit(tasks)

    def prep_update(self, data):
        # Create Database to return
        logger.debug('Update has been requested.  Processing...')
        progress_total = 20
        self.signals.progress.emit(['Beginning update...', progress_total])
        update_list = []
        if data:
            start_date = data['start_date'].toPython()
            end_date = data['end_date'].toPython()
            sod = parser.parse('00:00:00').time()
            eod = parser.parse('23:59:59').time()
            start_date = datetime.combine(start_date, sod)
            end_date = datetime.combine(end_date, eod)
            whose_timesheet = data['whose_timesheet']
            # sort_by is "Date" when True and "Artist" when false.
            sort_by = data['sort_by']

            if whose_timesheet == 0:
                users_list = users.get_all_users()
            else:
                users_list = [users.get_user_by_id(uid=whose_timesheet)]

            timesheets = tl_time.get_all_timsheets_in_range(start=start_date, end=end_date, users=users_list)
            ordered_timesheets = {}
            if timesheets:
                for ts in timesheets:
                    if sort_by:
                        ts_start = ts['sg_task_start']
                        ts_start_date = ts_start.date()
                        if ts_start_date not in ordered_timesheets.keys():
                            ordered_timesheets[ts_start_date] = {}
                        artist = ts['user']
                        artist_id = artist['id']
                        artist_name = artist['name']
                        if artist_name not in ordered_timesheets[ts_start_date].keys():
                            ordered_timesheets[ts_start_date][artist_name] = {
                                'timesheet': [ts]
                            }
                        else:
                            ordered_timesheets[ts_start_date][artist_name].setdefault('timesheet', []).append(ts)
                    else:
                        artist = ts['user']
                        artist_id = artist['id']
                        artist_name = artist['name']
                        if artist_name not in ordered_timesheets.keys():
                            ordered_timesheets[artist_name] = {}
                        ts_start = ts['sg_task_start']
                        ts_start_date = ts_start.date()
                        if ts_start_date not in ordered_timesheets[artist_name].keys():
                            ordered_timesheets[artist_name][ts_start_date] = {
                                'timesheet': [ts]
                            }
                        else:
                            ordered_timesheets[artist_name][ts_start_date].setdefault('timesheet', []).append(ts)

        logger.debug('Returning Update list...')

        progress_total = 65
        self.signals.progress.emit(['Sending the updated list...', progress_total])
        logger.debug('update list length: %s' % len(update_list))
        self.signals.update.emit(ordered_timesheets)
        logger.debug('Update list returned.')
        update_list = ordered_timesheets
        return update_list

    def update_totals(self):
        while not self.kill_it:
            daily_total = tl_time.get_daily_total(user=user, lunch_id=lunch_task_id)
            weekly_total = tl_time.get_weekly_total(user=user, lunch_id=lunch_task_id)
            self.signals.daily_total.emit(daily_total)
            self.signals.weekly_total.emit(weekly_total)
            time.sleep(2)

    def run(self, *args, **kwargs):
        self.update_totals()


class sheets(QtWidgets.QWidget):
    """
    The main sheets UI.
    """
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.engine = sheet_engine()

        self.dropdowns = sg_data.get_all_project_dropdowns(user=user)

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
        self.saved_window_position = self.settings.value('geometry', None)
        self.saved_whose_timesheet = self.settings.value('whose_timesheet', '.')
        self.saved_sort_by = self.settings.value('sort_by', '.')
        self.saved_order = self.settings.value('order', '.')
        self.restoreGeometry(self.saved_window_position)

        # Connect buttons
        self.ui.update_btn.clicked.connect(self.request_update)
        self.engine.signals.progress.connect(self.update_progress)
        self.engine.signals.daily_total.connect(self.update_daily_total)
        self.engine.signals.weekly_total.connect(self.update_weekly_total)

        # Manual Sheet Triggers
        self.ui.new_project.currentIndexChanged.connect(self.req_update_entities)
        self.ui.new_entity.currentIndexChanged.connect(self.req_update_tasks)
        self.engine.signals.send_entity_update.connect(self.update_entities)
        self.engine.signals.send_task_update.connect(self.update_tasks)

        # Set manual date and times
        new_start_date = datetime.now().date()
        new_start_time = datetime.now().time()
        new_end_date = new_start_date
        new_end_time = (datetime.now() + timedelta(hours=1)).time()

        self.ui.new_start_date.setDate(new_start_date)
        self.ui.new_start_time.setTime(new_start_time)
        self.ui.new_end_date.setDate(new_end_date)
        self.ui.new_end_time.setTime(new_end_time)

        self.ui.new_entity.addItem('Select Asset/Shot', 0)
        self.ui.add_time_btn.clicked.connect(self.req_add_time)
        self.ui.cancel_btn.clicked.connect(self.reset_manual_form)
        self.ui.new_artist_label.setText('%s' % user['name'])

        # NOTE: Temporary for quicker release, but the following need to go once fixed
        self.ui.export_btn.setStyleSheet('color: rgb(120, 120, 120);')
        self.ui.export_btn.setDisabled(True)
        self.ui.excel_rdo.setDisabled(True)
        self.ui.csv_rdo.setDisabled(True)
        self.ui.txt_rdo.setDisabled(True)
        self.ui.editor_progress.hide()
        self.ui.editor_status.hide()

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

        # Setup Manual Timesheet entry
        self.setup_manual_timesheets()

        # Setup connections.
        self.engine.signals.update.connect(self.update_list)
        self.request_update()

        self.engine.start()

    def setup_manual_timesheets(self):
        all_projects = sg_data.get_active_projects(user=user)
        self.ui.new_project.addItem('Select A Project', 0)
        for proj in all_projects:
            self.ui.new_project.addItem(proj['name'], proj['id'])

    def req_add_time(self):
        """
        This function will collect the data and send the signal to add a new timesheet entry.
        :return:
        """
        project_index = self.ui.new_project.currentIndex()
        project = self.ui.new_project.itemData(project_index)
        project_name = self.ui.new_project.currentText()
        if project == 0:
            alert = QtWidgets.QMessageBox()
            alert.setText('You Must Select A Project!')
            alert.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
            alert.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
            alert.exec_()
            self.ui.new_project.setFocus()
            return False
        entity_index = self.ui.new_entity.currentIndex()
        entity = self.ui.new_entity.itemData(entity_index)
        if entity == 0:
            alert = QtWidgets.QMessageBox()
            alert.setText('You Must Select an Asset or Shot!')
            alert.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
            alert.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
            alert.exec_()
            self.ui.new_entity.setFocus()
            return False
        task_index = self.ui.new_task.currentIndex()
        task = self.ui.new_task.itemData(task_index)
        task_name = self.ui.new_task.currentText()
        if task == 0:
            alert = QtWidgets.QMessageBox()
            alert.setText('You Must Select A Task!')
            alert.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
            alert.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
            alert.exec_()
            self.ui.new_task.setFocus()
            return False

        # Build new context and clock the user back in to what they were clocked into before lunch
        context = {
            'Project': {
                'id': project,
                'name': project_name
            },
            'Task': {
                'id': task,
                'content': task_name
            }
        }
        start_date = self.ui.new_start_date.date().toPython()
        start_time = self.ui.new_start_time.time().toPython()
        start = datetime.combine(start_date, start_time)
        end_date = self.ui.new_end_date.date().toPython()
        end_time = self.ui.new_end_time.time().toPython()
        end = datetime.combine(end_date, end_time)

        # Add the timesheet
        new_timesheet = tl_time.create_new_timesheet(user=user, context=context, start_time=start)
        if new_timesheet:
            clock_out = tl_time.clock_out_time_sheet(timesheet=new_timesheet, clock_out=end)
            if clock_out:
                self.ui.new_project.setCurrentIndex(0)
                self.ui.new_entity.clear()
                self.ui.new_entity.addItem('Select Asset/Shot', 0)
                self.request_update()
                self.ui.tabs.setCurrentIndex(0)

    def reset_manual_form(self):
        self.ui.new_project.setCurrentIndex(0)
        self.ui.new_entity.clear()
        self.ui.new_entity.addItem('Select Asset/Shot', 0)
        self.ui.tabs.setCurrentIndex(0)

    def req_update_entities(self, message=None):
        """
        This function will trigger another function that will update_entities.  The reason for this (instead of going
        directly to update_entities) is that update_entities requires more elaborate data than a
        currentIndexChanged.connect() event can support.
        :param message: String trigger.  Does nothing.
        :return:
        """
        logger.debug('req_update_entities: %s' % message)
        proj_id = self.ui.new_project.itemData(self.ui.new_project.currentIndex())
        self.engine.signals.req_entity_update.emit(proj_id)
        self.update_task_dropdown()

    def req_update_tasks(self, message=None):
        """
        This method askes for a regular update from an onChangeEvent with no data
        :param message:
        :return:
        """
        logger.debug('Request Update Tasks activated.')
        ent_id = self.ui.new_entity.itemData(self.ui.new_entity.currentIndex())
        ent_name = self.ui.new_entity.currentText()
        proj_index = self.ui.new_project.currentIndex()

        if ent_id:
            context = {
                'entity_id': ent_id,
                'entity_name': ent_name,
                'proj_id': self.ui.new_project.itemData(proj_index)
            }
            logger.debug('sending the req_task_update: %s' % context)
            self.engine.signals.req_task_update.emit(context)
            logger.debug('Done sending task context.')

    def update_entities(self, entities=None):
        """
        Processes data from a Shotgun Assets and Shots entity collection.
        :param entities: (dict) A combined dictionary from 2 queries
        :return: None
        """
        logger.debug('update entity dropdown signal %s' % entities)
        logger.debug(entities)
        if entities:
            # Put in the Assets first... Oh!  Use the categories and Sequences?
            self.ui.new_entity.clear()
            self.ui.new_entity.addItem('Select Asset/Shot', 0)
            for entity in entities:
                self.ui.new_entity.addItem(entity['code'], entity['id'])
            self.ui.new_entity.update()

    def update_tasks(self, tasks=None):
        logger.debug('update_task_dropdown message received: %s' % tasks)
        logger.debug('Setting tasks...')
        logger.debug(tasks)
        if tasks:
            self.ui.new_task.clear()
            self.ui.new_task.addItem('Select Task', 0)
            for task in tasks:
                self.ui.new_task.addItem(task['content'], task['id'])
        else:
            self.ui.new_task.clear()
            self.ui.new_task.addItem('Select Task', 0)

    def update_task_dropdown(self, tasks=None):
        logger.debug('update_task_dropdown message received: %s' % tasks)
        logger.debug('Setting tasks...')
        logger.debug(tasks)
        if tasks:
            self.ui.new_task.clear()
            self.ui.new_task.addItem('Select Task', 0)
            for task in tasks:
                self.ui.new_task.addItem(task['content'], task['id'])
        else:
            self.ui.new_task.clear()
            self.ui.new_task.addItem('Select Task', 0)

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
            sort_dir = self.ui.order.currentIndex()

            self.ui.sheet_tree.clear()
            self.ui.sheet_tree.setHeaderLabels(['TS ID', 'Project', 'Asset', 'Task', 'Start', 'End',
                                                'Duration', 'Edit'])
            self.ui.sheet_tree.setAlternatingRowColors(True)

            expand = None
            expand_2 = None

            primary_keys = list(data)
            if type(primary_keys[0]) == str:
                sort_dir = 0
            primary_keys = sorted(primary_keys, reverse=sort_dir)
            # Reset the sort direction
            sort_dir = self.ui.order.currentIndex()

            for primary in primary_keys:
                if type(primary) != str:
                    key = '%s' % primary
                    secondary_sort = 0
                    record_date = primary
                else:
                    key = primary
                    secondary_sort = sort_dir
                add_main_key = QtWidgets.QTreeWidgetItem()
                add_main_key.setText(0, str(key))

                # Check to expand the first row
                if not expand:
                    expand = add_main_key
                secondary_keys = data[primary].keys()
                secondary_keys = sorted(secondary_keys, reverse=secondary_sort)
                for secondary in secondary_keys:
                    if type(secondary) == datetime.date:
                        sub_key = '%s' % secondary
                        record_date = secondary
                    else:
                        sub_key = secondary
                    add_key = QtWidgets.QTreeWidgetItem()
                    add_key.setFirstColumnSpanned(False)
                    add_key.setText(0, str(sub_key))
                    if not expand_2:
                        expand_2 = add_key
                    daily_total = 0.0
                    add_key.setText(6, 'Daily Total: %0.2f hrs' % daily_total)

                    these_timesheets = list(data[primary][secondary].values())[0]
                    these_timesheets = sorted(these_timesheets, key=lambda i: i['sg_task_end'], reverse=sort_dir)
                    # print(these_timesheets)
                    for timesheet in these_timesheets:

                        task_id = timesheet['entity']['id']
                        task = timesheet['entity']['name']
                        project = timesheet['project']['name']
                        project_id = timesheet['project']['id']
                        entity = timesheet['entity.Task.entity']
                        entity_name = entity['name']
                        entity_id = entity['id']
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

                            time_table = QtWidgets.QTreeWidgetItem(add_key, [str(timesheet['id']),
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
            row = self.ui.sheet_tree.indexFromItem(expand)
            row_2 = self.ui.sheet_tree.indexFromItem(expand_2)
            self.ui.sheet_tree.expand(row)
            self.ui.sheet_tree.expand(row_2)
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
                    ts = time_editor(tid=ts_id, proj=project, ent=entity, task=task, start=start, end=end, user=_user,
                                     dropdowns=self.dropdowns)
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
            closing = 0.0
            self.ui.editor_status.setText('Closing...')
            while self.engine.isRunning():
                self.ui.editor_progress.setValue(closing)
                self.engine.kill()
                self.engine.quit()
                closing += 0.000002
        self.engine.kill_it = True


class time_editor(QtWidgets.QDialog):
    def __init__(self, parent=None, tid=None, proj=None, ent=None, task=None, start=None, end=None, user=None,
                 dropdowns=None):
        """
        The editor dialog that pops up when a user double clicks a time log in the main UI
        :param parent: The main UI
        :param tid: ID of the timesheet being edited
        :param proj: Project of the timesheet being edited
        :param ent: Entity of the timesheet being edited
        :param task: Task of the timesheet being edited
        :param start: Start time from the timesheet
        :param end: End time from the timesheet
        :param user: User whose timesheet is being edited
        :param dropdowns: A list of the project dropdowns from the sg_data.get_all_project_dropdowns()
        """
        QtWidgets.QDialog.__init__(self, parent)

        self.dropdowns = dropdowns
        self.editor = editor.Ui_Editor()
        self.editor.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
        self.setWindowTitle("Time Editor v%s" % __version__)
        self.editor.tid.setText('TID: %s' % tid)
        # FIXME: Have to convert these to drop downs.... ew.... with selections...
        #       This may go into building a new algorithm for collecting all projects, assets, shots and tasks for
        #       everything
        projects = dropdowns.keys()
        self.editor.project_dd.addItem('Select Project', 0)
        for project in projects:
            self.editor.project_dd.addItem(project, dropdowns[project]['__specs__']['id'])
        self.editor.project_dd.setCurrentIndex(self.editor.project_dd.findText(proj))
        entities = dropdowns[proj].keys()
        self.editor.entity_dd.addItem('Select Entity', 0)
        for entity in entities:
            if entity != '__specs__':
                self.editor.entity_dd.addItem(entity, dropdowns[proj][entity]['__specs__']['id'])
        self.editor.entity_dd.setCurrentIndex(self.editor.entity_dd.findText(ent))
        tasks = dropdowns[proj][ent].keys()
        self.editor.task_dd.addItem('Select Task', 0)
        for tsk in tasks:
            if tsk != '__specs__':
                self.editor.task_dd.addItem(tsk, dropdowns[proj][ent][tsk]['__specs__']['id'])
        self.editor.task_dd.setCurrentIndex(self.editor.task_dd.findText(task))

        start_date = start.date()
        start_time = start.time()
        end_date = end.date()
        end_time = end.time()
        self.editor.start_date.setDate(start_date)
        self.editor.start_time.setTime(start_time)
        self.editor.end_date.setDate(end_date)
        self.editor.end_time.setTime(end_time)
        self.user = user

        self.editor.update_btn.clicked.connect(self.update_timesheet)
        self.editor.delete_btn.clicked.connect(self.delete_timesheet)
        self.editor.cancel_btn.clicked.connect(self.reject)

        self.editor.project_dd.currentIndexChanged.connect(self.update_entities)
        self.editor.entity_dd.currentIndexChanged.connect(self.update_tasks)

    def update_entities(self):
        project = self.editor.project_dd.currentText()
        project_id = self.editor.project_dd.itemData(self.editor.project_dd.currentIndex())
        self.editor.entity_dd.clear()
        self.editor.entity_dd.addItem('Select Entity', 0)
        self.editor.task_dd.clear()
        self.editor.task_dd.addItem('Select Task', 0)
        entities = self.dropdowns[project].keys()
        if project_id != 0:
            for entity in entities:
                if entity != '__specs__':
                    self.editor.entity_dd.addItem(entity, self.dropdowns[project][entity]['__specs__']['id'])

    def update_tasks(self):
        project = self.editor.project_dd.currentText()
        project_id = self.editor.project_dd.itemData(self.editor.project_dd.currentIndex())
        entity = self.editor.entity_dd.currentText()
        entity_id = self.editor.entity_dd.itemData(self.editor.entity_dd.currentIndex())
        self.editor.task_dd.clear()
        self.editor.task_dd.addItem('Select Task', 0)
        if project_id != 0 and entity_id != 0:
            if entity:
                tasks = self.dropdowns[project][entity].keys()
                for task in tasks:
                    if task != '__specs__':
                        self.editor.task_dd.addItem(task, self.dropdowns[project][entity][task]['__specs__']['id'])

    def update_timesheet(self):
        tid = self.editor.tid.text()
        tid = int(tid.split(': ')[1])
        reason = self.editor.reason.toPlainText()
        if len(reason) < 8:
            alert = QtWidgets.QMessageBox()
            alert.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
            alert.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
            alert.setText('The reason you gave for the change does not say enough.  Please put in a reason for changing '
                          'this timesheet.')
            alert.exec_()
            self.editor.reason.setFocus()
            return False
        update = QtWidgets.QMessageBox()
        update.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
        update.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        update.setText('Are you sure you want to update %s?' % tid)
        update.addButton('Yes', QtWidgets.QMessageBox.AcceptRole)
        update.addButton('No', QtWidgets.QMessageBox.RejectRole)
        ret = update.exec_()
        if ret == QtWidgets.QMessageBox.AcceptRole:
            start_date = self.editor.start_date.date().toPython()
            start_time = self.editor.start_time.time().toPython()
            end_date = self.editor.end_date.date().toPython()
            end_time = self.editor.end_time.time().toPython()
            start = datetime.combine(start_date, start_time)
            end = datetime.combine(end_date, end_time)
            proj = self.editor.project_dd.itemData(self.editor.project_dd.currentIndex())
            task = self.editor.task_dd.itemData(self.editor.task_dd.currentIndex())

            logger.debug('Doing update...')
            # TODO: Add a "Conflicting Timesheet" check!
            do_update = tl_time.update_current_times(user=user, tid=tid, start_time=start, end_time=end, proj_id=proj,
                                                     task_id=task, reason=reason)
            logger.debug('Updated: %s' % do_update)
            self.accept()
        else:
            logger.debug('Rejected!')
            self.close()

    def delete_timesheet(self):
        tid = self.editor.tid.text()
        tid = int(tid.split(': ')[1])
        delete = QtWidgets.QMessageBox()
        delete.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
        delete.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        delete.setText('Are you sure you want to delete TID %s?  This can not be undone!' % tid)
        delete.addButton('Delete', QtWidgets.QMessageBox.AcceptRole)
        delete.addButton('Cancel', QtWidgets.QMessageBox.RejectRole)
        ret = delete.exec_()
        if ret == QtWidgets.QMessageBox.AcceptRole:
            tl_time.delete_timelog_by_id(tid=tid)
            self.accept()
        else:
            logger.debug('Rejected!')
            self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName('AdamBenson')
    app.setOrganizationDomain('adamdbenson.com')
    app.setApplicationName('Sheets')
    splash_pix = QtGui.QPixmap('ui/resources/Time_Lord_Logo.png')
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    o = sheets()
    o.show()
    splash.finish(o)
    sys.exit(app.exec_())

