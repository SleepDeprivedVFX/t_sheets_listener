"""
This utility is an early stage bridge designed to get data from the Time Lord and Shotgun Systems
and save it to an Excel Spreadsheet.  It is a temporary system which will eventually be replaced by
a possible NIM connection (for ASC) and possibly a direct connection to PayChex.  We'll see how it
goes.
"""

from ui import time_lord_reports as tlr
from PySide import QtCore, QtGui
import xlsxwriter as xls
from bin.companions import companions
from bin import configuration
from bin import shotgun_collect
from bin.time_continuum import continuum
from datetime import datetime, timedelta
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
import shotgun_api3 as sgapi
import webbrowser


__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.4.9'

config = configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'tl_reports.log'
log_root = os.path.join(sys.path[0], 'logs')
if not os.path.exists(log_root):
    os.makedirs(log_root)
log_path = os.path.join(log_root, log_file)
debug = config['debug_logging']
if debug == 'True' or debug == 'true' or debug == True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('tl_reports')
logger.setLevel(level=level)
fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                              backupCount=int(config['log_days']))
fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
fh.setFormatter(fm)
logger.addHandler(fh)

logger.info('Time Lord Reports Utility has started.')

# --------------------------------------------------------------------------------------------------
# Setup Shotgun Connection
# --------------------------------------------------------------------------------------------------
sg = sgapi.Shotgun(config['sg_url'], config['sg_name'], config['sg_key'])
logger.debug('Shotgun is connected.')

# --------------------------------------------------------------------------------------------------
# Connect Time Lord Components
# --------------------------------------------------------------------------------------------------
# setup continuum
tl_time = continuum(sg, config=config)

# Setup and get users
users = companions(sg, config=config)
user = users.get_user_from_computer()

# setup shotgun data connection
sg_data = shotgun_collect.sg_data(sg, config=config)

lunch_task = sg_data.get_lunch_task(lunch_proj_id=int(config['admin_proj_id']),
                                    task_name=config['lunch'])


# ------------------------------------------------------------------------------------------------
# Signal Emitters
# ------------------------------------------------------------------------------------------------
class report_signals(QtCore.QObject):
    output_monitor = QtCore.Signal(dict)
    get_payroll = QtCore.Signal(dict)
    req_report = QtCore.Signal(dict)
    snd_report_project_hours = QtCore.Signal(dict)


class payroll_engine(QtCore.QThread):
    # Main Worker thread.
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.signals = report_signals()

        # Connections
        self.signals.get_payroll.connect(self.make_payroll_reports)
        self.signals.req_report.connect(self.start_reports)

    def make_payroll_reports(self, data={}):
        # This saves the data into an excel spreadsheet
        if data:
            print('Data: %s' % data)
            output = data['output']
            start = data['start']
            end = data['end']

            # Start the Excel Sheet
            payroll_excel = xls.Workbook(output)
            payroll = payroll_excel.add_worksheet()

            # Formatting
            payroll.set_column('A:A', 20)
            bold = payroll_excel.add_format({'bold': True})
            highlight = payroll_excel.add_format({'bg_color': 'yellow'})
            heading = payroll_excel.add_format({'bg_color': '#CCFFFF'})

            # First Row
            payroll.write(0, 0, 'Summary report for %s through %s' % (start, end), bold)

            # Third Row
            payroll.write('A3', 'payroll_id', heading)
            payroll.write('B3', 'type', heading)
            payroll.write('C3', 'hours', heading)
            payroll.write('D3', 'fname', heading)
            payroll.write('E3', 'lname', heading)
            payroll.write('F3', 'group_name', heading)
            payroll.write('G3', 'start_date', heading)
            payroll.write('H3', 'end_date', heading)

            # start row for dynamic records
            row = 4

            all_users = users.get_all_users()
            if all_users:
                for u in all_users:
                    # Get the basic data from Shotgun
                    name = u['name']
                    first_name = name.split(' ')[0]
                    last_name = name.split(' ')[1]
                    uid = u['id']
                    get_group = u['permission_rule_set']['name']
                    if get_group == 'Coordinator':
                        get_group = 'Coord'
                    elif get_group == 'Independent Artist':
                        get_group = 'Artist'
                    if u['sg_hourly']:
                        u_type = 'REG'
                    else:
                        u_type = 'SAL'

                    # Collect the total hours for the user
                    user_total = tl_time.get_user_total_in_range(user=uid, start=start, end=end,
                                                                 lunch_id=int(lunch_task['id']))
                    payroll.write(row, 1, u_type)
                    payroll.write(row, 2, round(user_total, 2), highlight)
                    payroll.write(row, 3, first_name)
                    payroll.write(row, 4, last_name, highlight)
                    payroll.write(row, 5, get_group)
                    payroll.write(row, 6, start)
                    payroll.write(row, 7, end)

                    # Setup and send UI update
                    out_msg = {
                        'name': name,
                        'type': u_type,
                        'level': get_group,
                        'total': round(user_total, 2)
                    }
                    self.signals.output_monitor.emit(out_msg)

                    # Iterate
                    row += 1
                row += 2
                payroll.write(row, 0, 'Salary', bold)
                row += 1
                for u in all_users:
                    if not u['sg_hourly']:
                        payroll.write(row, 0, u['name'], highlight)
                        row += 1

            # Finish up the document.
            payroll_excel.close()

            # Open the Excel sheet
            webbrowser.open(output)

    def start_reports(self, data={}):
        return_data = {}
        highest_value = 0.0
        if data:
            primary = data['primary']
            primary_id = data['primary_id']
            secondary = data['secondary']
            secondary_id = data['secondary_id']
            trinary = data['trinary']
            trinary_id = data['trinary_id']
            quaternary = data['quaternary']
            quaternary_id = data['quaternary_id']
            quinternary = data['quinternary']
            quinternary_id = data['quinternary_id']
            all_time = data['all_time']
            start = data['start']
            end = data['end']

            filters = [
                ['entity_type', 'is', 'Asset']
            ]
            fields = ['code', 'entity_type']
            asset_steps = sg.find('Step', filters, fields)
            filters = [
                ['entity_type', 'is', 'Shot']
            ]
            shot_steps = sg.find('Step', filters, fields)

            if primary == 'Projects':
                if secondary_id == 1:
                    all_timesheets = tl_time.get_all_timsheets_in_range(start=start, end=end, all_time=all_time)
                else:
                    all_timesheets = tl_time.get_all_timsheets_in_range(proj_id=secondary_id, start=start, end=end,
                                                                        all_time=all_time)
                total_time = 0.0
                projects = []
                artists = []
                tasks = []
                for ts in all_timesheets:
                    total_time += ts['duration']
                    if ts['project']['name'] not in projects:
                        projects.append(ts['project']['name'])
                    if ts['user'] not in artists:
                        artists.append(ts['user'])
                    if ts['entity'] not in tasks:
                        tasks.append(ts['entity'])
                return_data['__specs__'] = {'total_time': total_time}
                return_data['timesheets'] = all_timesheets
                return_data['projects'] = projects
                return_data['artists'] = artists
                return_data['tasks'] = tasks
                return_data['asset_steps'] = asset_steps
                return_data['shot_steps'] = shot_steps
                self.signals.snd_report_project_hours.emit(return_data)


class reports_ui(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.settings = QtCore.QSettings('Adam Benson', 'time_lord_reports')
        self.last_output = self.settings.value('last_output', '.')

        self.engine = payroll_engine()
        self.engine.start()

        self.ui = tlr.Ui_Time_Lord_Reports()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))

        # Set the start and end dates
        self.guess_dates()

        # Set combo box options
        self.ui.secondary_org.hide()
        self.ui.trinary_org.hide()
        self.ui.quaternary_org.hide()
        self.ui.quinternary_org.hide()

        # Make change set connections
        self.ui.primary_org.currentIndexChanged.connect(lambda: self.set_search_options(driver=self.ui.primary_org,
                                                                                        list=self.ui.secondary_org))
        self.ui.secondary_org.currentIndexChanged.connect(lambda: self.set_search_options(driver=self.ui.secondary_org,
                                                                                          list=self.ui.trinary_org))
        self.ui.trinary_org.currentIndexChanged.connect(lambda: self.set_search_options(driver=self.ui.trinary_org,
                                                                                        list=self.ui.quaternary_org))
        self.ui.quaternary_org.currentIndexChanged.connect(lambda: self.set_search_options(
            driver=self.ui.quaternary_org,
            list=self.ui.quinternary_org)
                                                           )

        # Connect the buttons
        self.ui.run_btn.clicked.connect(self.run_reports)

        # Connect report processors
        self.engine.signals.snd_report_project_hours.connect(self.project_hours_report)

    def run_reports(self):
        primary = self.ui.primary_org.currentText()
        primary_id = self.ui.primary_org.itemData(self.ui.primary_org.currentIndex())
        secondary = self.ui.secondary_org.currentText()
        secondary_id = self.ui.secondary_org.itemData(self.ui.secondary_org.currentIndex())
        trinary = self.ui.trinary_org.currentText()
        trinary_id = self.ui.trinary_org.itemData(self.ui.trinary_org.currentIndex())
        quaternary = self.ui.quaternary_org.currentText()
        quaternary_id = self.ui.quaternary_org.itemData(self.ui.quaternary_org.currentIndex())
        quinternary = self.ui.quinternary_org.currentText()
        quinternary_id = self.ui.quinternary_org.itemData(self.ui.quinternary_org.currentIndex())
        all_time = self.ui.all_time.isChecked()
        start = self.ui.start_time.dateTime().toPython()
        end = self.ui.end_time.dateTime().toPython()

        data = {
            'primary': primary,
            'primary_id': primary_id,
            'secondary': secondary,
            'secondary_id': secondary_id,
            'trinary': trinary,
            'trinary_id': trinary_id,
            'quaternary': quaternary,
            'quaternary_id': quaternary_id,
            'quinternary': quinternary,
            'quinternary_id': quinternary_id,
            'all_time': all_time,
            'start': start,
            'end': end,
        }
        self.engine.signals.req_report.emit(data)

    def guess_dates(self):
        guess_end_date = (datetime.today() - timedelta(days=(datetime.today().isoweekday() % 7) + 1)).date()
        guess_start_date = (guess_end_date - timedelta(days=13))
        self.ui.start_time.setDate(guess_start_date)
        self.ui.end_time.setDate(guess_end_date)

    def project_hours_report(self, data=None):
        print('DATA RECIEVED: %s' % data.keys())
        if data:
            self.ui.data_tree.clear()
            # header = self.ui.data_tree.horizontalHeader()
            # header.setResizeMode(2, QtGui.QHeaderView.Stretch)
            # row = self.ui.graphs_table.rowCount()
            # print(row)
            specs = data['__specs__']
            projects = data['projects']
            artists = data['artists']
            tasks = data['tasks']
            timesheets = data['timesheets']
            total_time = float(specs['total_time'])
            asset_steps = data['asset_steps']
            shot_steps = data['shot_steps']

            import time

            print('projects: %s' % projects)
            print('artists: %s' % artists)
            print('tasks: %s' % tasks)
            print('total_time: %s' % total_time)
            print('asset_steps: %s' % asset_steps)
            print('shot_steps: %s' % shot_steps)
            print('+' * 120)
            time.sleep(10)

            report = {
                'project': {
                    'Assets': {
                        'asset': {
                            'Tasks': {
                                'Timesheet': []
                            }
                        }
                    },
                    'Shots': {
                        'Tasks': {
                            'Timesheets': []
                        }
                    }
                }
            }
            for ts in timesheets:
                proj = ts['project']['name']
                if proj not in report.keys():
                    report[proj] = {}
                ent_type = ts['entity.Task.entity']['type']
                if ent_type not in report[proj].keys():
                    report[proj][ent_type] = {}
                entity = ts['entity.Task.entity']['name']
                if entity not in report[proj][ent_type].keys():
                    report[proj][ent_type][entity] = {}
                task = ts['entity']['name'].split('.')[0]
                if task not in report[proj][ent_type][entity].keys():
                    report[proj][ent_type][entity][task] = [ts]
                else:
                    report[proj][ent_type][entity].setdefault(task, []).append(ts)
            print(report)



            # for proj in projects:
            #     print('=' * 120)
            #     print(proj)
            #     if proj not in report.keys():
            #         report[proj] = {}
            #     project_total = 0.0
            #     project_widget = QtGui.QTreeWidgetItem()
            #     project_timesheets = []
            #     project_assets = []
            #     project_shots = []
            #     project_tasks = []
            #     task_timesheets = {}
            #     for ts in timesheets:
            #         if proj == ts['project']['name']:
            #             project_timesheets.append(ts)
            #             project_total += ts['duration'] / 60.0
            #             if ts['entity.Task.entity']['type'] == 'Asset' and \
            #                     ts['entity.Task.entity'] not in project_assets:
            #                 project_assets.append(ts)
            #             elif ts['entity.Task.entity']['type'] == 'Shot' and \
            #                     ts['entity.Task.entity'] not in project_shots:
            #                 project_shots.append(ts)
            #             task = ts['entity']['name'].split('.')[0]
            #             if task not in project_tasks:
            #                 project_tasks.append(task)
            #             task_timesheets[ts['id']] = (task, ts)
            #             # if ts['entity'] not in project_tasks:
            #             #     project_tasks.append(ts)
            #     for asset in project_assets:
            #         print(asset['entity.Task.entity']['name'])
            #         for t in project_tasks:
            #             print(t)
            #             for tid, task in task_timesheets.items():
            #                 if t == task[0]:
            #                     if task[1]['entity.Task.entity']['type'] == 'Asset' and \
            #                             task[0] in asset['entity']['name']:
            #                         print(tid, task[1])
            #
            #     project_widget.setText(0, proj)
            #     project_widget.setText(6, 'Total Hours: %0.2f' % project_total)
            #
            #     # for asset in project_assets:
            #     #     print(asset['entity.Task.entity']['name'])
            #     #     print('- ' * 120)
            #     #     asset_duration = 0.0
            #     #     asset_widget = QtGui.QTreeWidgetItem()
            #     #     asset_widget.setText(0, asset['entity.Task.entity']['name'])
            #     #     for ts in timesheets:
            #     #         if asset == ts:
            #     #             asset_duration += ts['duration'] / 60.0
            #     #             for step in asset_steps:
            #     #                 step_tasks = []
            #     #                 for task in project_tasks:
            #     #                     if step['code'] in task['entity']['name']:
            #     #                         step_tasks.append(ts)
            #     #                 if step_tasks:
            #     #                     print(step['code'])
            #     #                     task_duration = 0.0
            #     #                     step_widget = QtGui.QTreeWidgetItem()
            #     #                     step_widget.setText(0, step['code'])
            #     #                     for task in step_tasks:
            #     #                         task_duration += task['duration'] / 60.0
            #     #                         print(task)
            #     #                         task_widget = QtGui.QTreeWidgetItem()
            #     #                         task_widget.setText(0, task['entity']['name'])
            #     #                         task_widget.setText(6, 'Hours: %0.2f' % (task['duration'] / 60.0))
            #     #                         step_widget.addChild(task_widget)
            #     #                     step_widget.setText(6, 'Task Hours: %0.2f' % task_duration)
            #     #                     asset_widget.addChild(step_widget)
            #     #
            #     #     asset_widget.setText(6, 'Total Hours: %0.2f' % asset_duration)
            #     #     project_widget.addChild(asset_widget)
            #     # for shot in project_shots:
            #     #     print(shot['entity.Task.entity']['name'])
            #     #     print(' -' * 120)
            #     #     shot_duration = 0.0
            #     #     shot_widget = QtGui.QTreeWidgetItem()
            #     #     shot_widget.setText(0, shot['entity.Task.entity']['name'])
            #     #     for ts in timesheets:
            #     #         if shot == ts['entity.Task.entity']:
            #     #             shot_duration += ts['duration'] / 60.0
            #     #     shot_widget.setText(6, 'Total Hours: %0.2f' % shot_duration)
            #     self.ui.data_tree.addTopLevelItem(project_widget)

    def set_search_options(self, driver=None, list=None):
        drv_obj = driver.currentText()
        drv_obj_index = driver.currentIndex()
        drv_obj_name = driver.objectName()
        if drv_obj != 'None' or drv_obj_index > 0:
            # list.show()
            list.clear()
            if drv_obj_name == 'primary_org':
                list.show()
                if drv_obj == 'Artists':
                    list.addItem('All Artists', 1)
                    all_users = users.get_all_users()
                    if all_users:
                        for u in all_users:
                            list.addItem(u['name'], u['id'], u['email'])
                elif drv_obj == 'Projects':
                    list.addItem('All Projects', 1)
                    all_projects = sg_data.get_active_projects()
                    if all_projects:
                        for proj in all_projects:
                            list.addItem(proj['name'], int(proj['id']))
                elif drv_obj == 'Entities (Assets)':
                    list.addItem('All Assets', 1)
                    all_assets = sg_data.get_active_assets()
                    if all_assets:
                        for asset in all_assets:
                            list.addItem(asset['code'], asset['id'])
                elif drv_obj == 'Entities (Shots)':
                    list.addItem('All Shots', 1)
                    all_shots = sg_data.get_active_shots()
                    if all_shots:
                        for shot in all_shots:
                            list.addItem(shot['code'], shot['id'])
                elif drv_obj == 'All Entities':
                    list.addItem('All Entities', 1)
                    all_shots = sg_data.get_active_shots()
                    all_assets = sg_data.get_active_assets()
                    entities = all_assets + all_shots
                    everything = sorted(entities, key=lambda x: (x['code']))
                    if everything:
                        for thing in everything:
                            list.addItem(thing['code'], thing['id'])
                elif drv_obj == 'Tasks':
                    list.addItem('All Tasks')
                    all_tasks = sg_data.get_all_tasks()
                    if all_tasks:
                        for task in all_tasks:
                            list.addItem(task)
                else:
                    list.addItem('None', 0)
            elif drv_obj_name == 'secondary_org':
                list.show()
                list.addItem('Total Hours', 1)
                if driver.findText('All Artists', 1) >= 0:
                    list.addItem('Hours', 2)
                    list.addItem('Projects', 3)
                    list.addItem('Assets', 4)
                    list.addItem('Shots', 5)
                    list.addItem('Tasks', 6)
                    list.addItem('Lunches', 7)
                if driver.findText('All Projects', 1) >= 0:
                    list.addItem('Artists', 2)
                    list.addItem('Assets', 3)
                    list.addItem('Shots', 4)
                    list.addItem('Tasks', 5)
                if driver.findText('All Assets', 1) >= 0:
                    list.addItem('Artists', 2)
                    list.addItem('Projects', 3)
                    list.addItem('Tasks', 4)
                if driver.findText('All Shots', 1) >= 0:
                    list.addItem('Artists', 2)
                    list.addItem('Projects', 3)
                    list.addItem('Tasks', 4)
                if driver.findText('All Entities', 1) >= 0:
                    list.addItem('Artists', 2)
                    list.addItem('Projects', 3)
                    list.addItem('Tasks', 4)
                if driver.findText('All Tasks', 1) >= 0:
                    list.addItem('Artists', 2),
                    list.addItem('Projects', 3)
            elif drv_obj_name == 'trinary_org':
                if drv_obj == 'Projects':
                    list.show()
                    all_projects = sg_data.get_active_projects()
                    if all_projects:
                        list.addItem('All Projects', 1)
                        for proj in all_projects:
                            list.addItem(proj['name'], proj['id'])
                elif drv_obj == 'Artists':
                    list.show()
                    all_users = users.get_all_users()
                    if all_users:
                        list.addItem('All Artists', 1)
                        for u in all_users:
                            list.addItem(u['name'], u['id'])
                else:
                    list.hide()
            elif drv_obj_name == 'quaternary_org':
                if drv_obj == 'All Artists':
                    list.show()
                    # TODO: Here I will probably need to start getting actual data:
                    #       But it's going to depend on the primary organizer
        else:
            list.clear()
            list.addItem('None', 0)
            list.hide()
        width = list.minimumSizeHint().width()
        list.setMinimumWidth(width * 3)

    def set_trinary_search_options(self):
        pass

    def closeEvent(self, *args, **kwargs):
        if self.engine.isRunning():
            self.engine.exit()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = reports_ui()
    w.show()
    sys.exit(app.exec_())


