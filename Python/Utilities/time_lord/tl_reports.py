"""
This utility is an early stage bridge designed to get data from the Time Lord and Shotgun Systems
and save it to an Excel Spreadsheet.  It is a temporary system which will eventually be replaced by
a possible NIM connection (for ASC) and possibly a direct connection to PayChex.  We'll see how it
goes.
"""

from ui import time_lord_reports as tlr
from PySide import QtCore, QtGui
import xlsxwriter as xls
# from openpyxl import Workbook as xlwb
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
import pprint

pp = pprint.PrettyPrinter(indent=1)

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.4.14'

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
        self.signals.req_report.connect(self.start_project_reports)

    def make_payroll_reports(self, data={}):
        # This saves the data into an excel spreadsheet
        if data:
            print('Data:')
            pp.pprint(data)
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

    def start_project_reports(self, data={}):
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
            output_path = data['output']

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

                tree_structure = {}

                for ts in all_timesheets:
                    try:
                        total_time += ts['duration']
                        if ts['project']['name'] not in projects:
                            projects.append(ts['project']['name'])
                        if ts['user'] not in artists:
                            artists.append(ts['user'])
                        if ts['entity'] not in tasks:
                            tasks.append(ts['entity'])

                        # ----------------------------------------------------------------------------------------
                        # Add the project database
                        proj = ts['project']['name']
                        if proj not in tree_structure.keys():
                            tree_structure[proj] = {
                                '_duration_': ts['duration'],
                                '_avg_time_': [ts['duration']],
                                '_avgs_': {}
                            }
                        else:
                            duration = tree_structure[proj]['_duration_']
                            duration += ts['duration']
                            tree_structure[proj]['_duration_'] = duration
                            tree_structure[proj].setdefault('_avg_time_', []).append(ts['duration'])

                        # ----------------------------------------------------------------------------------------
                        # Get and set the Entity Type: Usually "Asset" or "Shot"
                        ent_type = ts['entity.Task.entity']['type']
                        if ent_type not in tree_structure[proj].keys():
                            tree_structure[proj][ent_type] = {
                                '_duration_': ts['duration'],
                                '_avg_time_': [ts['duration']],
                                '_avgs_': {}
                            }

                            # add the averages for the parent
                            if ent_type not in tree_structure[proj]['_avgs_'].keys():
                                tree_structure[proj]['_avgs_'][ent_type] = ts['duration']
                            else:
                                ent_type_avg = tree_structure[proj]['_avgs_'][ent_type]
                                ent_type_avg += ts['duration']
                                tree_structure[proj]['_avgs_'][ent_type] = ent_type_avg
                        else:
                            duration = tree_structure[proj][ent_type]['_duration_']
                            duration += ts['duration']
                            tree_structure[proj][ent_type]['_duration_'] = duration
                            tree_structure[proj][ent_type].setdefault('_avg_time_', []).append(ts['duration'])

                            # Add the averages for the parent
                            if ent_type not in tree_structure[proj]['_avgs_'].keys():
                                tree_structure[proj]['_avgs_'][ent_type] = ts['duration']
                            else:
                                ent_type_avg = tree_structure[proj]['_avgs_'][ent_type]
                                ent_type_avg += ts['duration']
                                tree_structure[proj]['_avgs_'][ent_type] = ent_type_avg

                        # ----------------------------------------------------------------------------------------
                        # Get and set the Entity data
                        entity = ts['entity.Task.entity']['name']
                        if entity not in tree_structure[proj][ent_type].keys():
                            tree_structure[proj][ent_type][entity] = {
                                '_duration_': ts['duration'],
                                '_avg_time_': [ts['duration']],
                                '_avgs_': {}
                            }

                            # add the averages for the parent
                            if entity not in tree_structure[proj][ent_type]['_avgs_'].keys():
                                tree_structure[proj][ent_type]['_avgs_'][entity] = ts['duration']
                            else:
                                entity_avg = tree_structure[proj][ent_type]['_avgs_'][entity]
                                entity_avg += ts['duration']
                                tree_structure[proj][ent_type]['_avgs_'][entity] = entity_avg
                        else:
                            duration = tree_structure[proj][ent_type][entity]['_duration_']
                            duration += ts['duration']
                            tree_structure[proj][ent_type][entity]['_duration_'] = duration
                            tree_structure[proj][ent_type][entity].setdefault('_avg_time_', []).append(ts['duration'])

                            # add the averages for the parent
                            if entity not in tree_structure[proj][ent_type]['_avgs_'].keys():
                                tree_structure[proj][ent_type]['_avgs_'][entity] = ts['duration']
                            else:
                                entity_avg = tree_structure[proj][ent_type]['_avgs_'][entity]
                                entity_avg += ts['duration']
                                tree_structure[proj][ent_type]['_avgs_'][entity] = entity_avg

                        # ----------------------------------------------------------------------------------------
                        # Get and set the task level
                        task = ts['entity']['name'].split('.')[0]
                        if task not in tree_structure[proj][ent_type][entity].keys():
                            tree_structure[proj][ent_type][entity][task] = {
                                'timesheets': [ts],
                                '_duration_': ts['duration'],
                                '_avg_time_': [ts['duration']],
                                '_avgs_': {}
                            }

                            # add the averages for the parent
                            if task not in tree_structure[proj][ent_type][entity]['_avgs_'].keys():
                                tree_structure[proj][ent_type][entity]['_avgs_'][task] = ts['duration']
                            else:
                                task_avg = tree_structure[proj][ent_type][entity]['_avgs_'][task]
                                task_avg += ts['duration']
                                tree_structure[proj][ent_type][entity]['_avgs_'][task] = task_avg
                        else:
                            duration = tree_structure[proj][ent_type][entity][task]['_duration_']
                            duration += ts['duration']
                            tree_structure[proj][ent_type][entity][task].setdefault('timesheets', []).append(ts)
                            tree_structure[proj][ent_type][entity][task].setdefault('_avg_time_',
                                                                                    []).append(ts['duration'])
                            tree_structure[proj][ent_type][entity][task]['_duration_'] = duration

                            # add the averages for the parent
                            if task not in tree_structure[proj][ent_type][entity]['_avgs_'].keys():
                                tree_structure[proj][ent_type][entity]['_avgs_'][task] = ts['duration']
                            else:
                                task_avg = tree_structure[proj][ent_type][entity]['_avgs_'][task]
                                task_avg += ts['duration']
                                tree_structure[proj][ent_type][entity]['_avgs_'][task] = task_avg

                        # ----------------------------------------------------------------------------------------
                        # Set the artist name
                        artist = ts['user']['name']
                        if artist not in tree_structure[proj][ent_type][entity][task].keys():
                            tree_structure[proj][ent_type][entity][task][artist] = {
                                '_duration_': ts['duration'],
                                '_avg_time_': [ts['duration']],
                                '_avgs': {}
                            }

                            # add the averages for the parent
                            if artist not in tree_structure[proj][ent_type][entity][task]['_avgs_'].keys():
                                tree_structure[proj][ent_type][entity][task]['_avgs_'][artist] = ts['duration']
                            else:
                                artist_avg = tree_structure[proj][ent_type][entity][task]['_avgs_'][artist]
                                artist_avg += ts['duration']
                                tree_structure[proj][ent_type][entity][task]['_avgs_'][artist] = artist_avg
                        else:
                            duration = tree_structure[proj][ent_type][entity][task][artist]['_duration_']
                            duration += ts['duration']
                            tree_structure[proj][ent_type][entity][task][artist]['_duration_'] = duration
                            tree_structure[proj][ent_type][entity][task][artist].setdefault('_avg_time_',
                                                                                            []).append(ts['duration'])

                            # add the averages for the parent
                            if artist not in tree_structure[proj][ent_type][entity][task]['_avgs_'].keys():
                                tree_structure[proj][ent_type][entity][task]['_avgs_'][artist] = ts['duration']
                            else:
                                artist_avg = tree_structure[proj][ent_type][entity][task]['_avgs_'][artist]
                                artist_avg += ts['duration']
                                tree_structure[proj][ent_type][entity][task]['_avgs_'][artist] = artist_avg
                    except Exception as e:
                        logger.error('Start Projects Report: Fit hit the shan: %s | %s' % (e, ts))
                        continue

                return_data['__specs__'] = {'total_time': total_time}
                return_data['timesheets'] = all_timesheets
                return_data['projects'] = projects
                return_data['artists'] = artists
                return_data['tasks'] = tasks
                return_data['asset_steps'] = asset_steps
                return_data['shot_steps'] = shot_steps
                return_data['tree_structure'] = tree_structure
                self.signals.snd_report_project_hours.emit(return_data)


class reports_ui(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.settings = QtCore.QSettings('Adam Benson', 'time_lord_reports')
        self.last_output = self.settings.value('last_output', '.')
        self.saved_window_position = self.settings.value('geometry', '')
        self.restoreGeometry(self.saved_window_position)

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

        self.ui.all_time.setChecked(True)

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
        self.ui.output_path.textChanged.connect(self.set_output)

        # Connect the buttons
        self.ui.run_btn.clicked.connect(self.run_reports)

        # Connect report processors
        self.engine.signals.snd_report_project_hours.connect(self.project_hours_report)

        # Create Main EXCEL sheet
        output = self.ui.output_path.text()
        if output:
            self.report = xls.Workbook(output)
        else:
            self.report = xls.Workbook('temp.xlsx')

    def set_output(self):
        output = self.ui.output_path.text()

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
        output_path = self.ui.output_path.text()

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
            'output': output_path,
        }
        self.engine.signals.req_report.emit(data)

    def guess_dates(self):
        guess_end_date = (datetime.today() - timedelta(days=(datetime.today().isoweekday() % 7) + 1)).date()
        guess_start_date = (guess_end_date - timedelta(days=13))
        self.ui.start_time.setDate(guess_start_date)
        self.ui.end_time.setDate(guess_end_date)

    def project_hours_report(self, data=None):
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
            tree_structure = data['tree_structure']

            report_page = self.report.add_worksheet('Project Actuals')
            report_page.set_column('A:A', 20)
            bold = self.report.add_format({'bold': True})
            highlight = self.report.add_format({'bg_color': 'yellow'})
            heading = self.report.add_format({'bg_color': '#CCFFFF'})

            report_page.write(0, 0, 'Actuals Report for Projects')
            report_page.write('A3', 'Project', heading)
            report_page.write('B3', 'Entity Type', heading)
            report_page.write('C3', 'Entity', heading)
            report_page.write('D3', 'Task', heading)
            report_page.write('E3', 'Artist', heading)
            report_page.write('F3', 'Proj Hrs', heading)
            report_page.write('G3', 'Type Hrs', heading)
            report_page.write('H3', 'Type %% Total', heading)
            report_page.write('I3', 'Entity Hrs', heading)
            report_page.write('J3', 'Entity %% Total', heading)
            report_page.write('K3', 'Task Hrs', heading)
            report_page.write('L3', 'Task %% Total', heading)
            report_page.write('M3', 'Artist Hrs', heading)
            report_page.write('N3', 'Artist %% Total', heading)

            row = 3

            # Build the tree
            for proj, details in tree_structure.items():
                proj_label = QtGui.QTreeWidgetItem()
                proj_label.setText(0, proj)
                proj_duration = float(details['_duration_']) / 60.0
                proj_label.setText(5, '%0.2f hrs' % proj_duration)

                # Excel
                row += 1
                report_page.write(row, 0, proj)
                report_page.write(row, 5, proj_duration)

                for ent_type, entities in details.items():

                    if ent_type not in ['_duration_', '_avg_time_', '_avgs_']:
                        ent_type_label = QtGui.QTreeWidgetItem()
                        ent_type_label.setText(1, ent_type)
                        ent_type_duration = float(entities['_duration_']) / 60.0
                        ent_type_label.setText(5, '%0.2f hrs' % ent_type_duration)
                        ent_type_avg = ((ent_type_duration / proj_duration) * 100)
                        ent_type_label.setText(6, '%0.2f%% time' % ent_type_avg)

                        # Excel
                        row += 1
                        report_page.write(row, 1, ent_type)
                        report_page.write(row, 6, ent_type_duration)
                        report_page.write(row, 7, '%0.2f%%' % ent_type_avg)

                        for entity, steps in entities.items():
                            # Get the current averages.
                            avg = 0.0
                            for k, v in entities['_avgs_'].items():
                                if k == entity:
                                    avg += v

                            if entity not in ['_duration_', '_avg_time_', '_avgs_']:
                                entity_label = QtGui.QTreeWidgetItem()
                                entity_label.setText(2, entity)
                                entity_duration = float(steps['_duration_']) / 60.0
                                entity_label.setText(5, '%0.2f Hrs' % entity_duration)
                                entity_avg = (float(entity_duration) / float(ent_type_duration)) * 100.0
                                entity_label.setText(6, '%0.2f%% time' % entity_avg)

                                # Excel
                                row += 1
                                report_page.write(row, 2, entity)
                                report_page.write(row, 8, entity_duration)
                                report_page.write(row, 9, '%0.2f%%' % entity_avg)

                                for step, tasks in steps.items():
                                    if step not in ['_duration_', '_avg_time_', '_avgs_']:
                                        step_label = QtGui.QTreeWidgetItem()
                                        step_label.setText(3, step)
                                        step_duration = float(tasks['_duration_']) / 60.0
                                        step_label.setText(5, '%0.2f hrs' % step_duration)
                                        step_average = step_duration / entity_duration * 100.0
                                        step_label.setText(6, '%0.2f%% time' % step_average)
                                        step_artists = tasks['_avgs_']

                                        # Excel
                                        row += 1
                                        report_page.write(row, 3, step)
                                        report_page.write(row, 10, step_duration)
                                        report_page.write(row, 11, '%0.2f%%' % step_average)

                                        for artist, hours in step_artists.items():
                                            artist_label = QtGui.QTreeWidgetItem()
                                            artist_label.setText(4, artist)
                                            artist_label.setText(5, '%0.2f Hrs' % (hours / 60.0))
                                            artist_avg = (hours / 60.0) / step_duration * 100.0
                                            artist_label.setText(6, '%0.2f%% time' % artist_avg)
                                            step_label.addChild(artist_label)

                                            # Excel
                                            row += 1
                                            report_page.write(row, 4, artist)
                                            report_page.write(row, 12, (hours / 60.0))
                                            report_page.write(row, 13, '%0.2f%%' % artist_avg)

                                        entity_label.addChild(step_label)
                                ent_type_label.addChild(entity_label)
                        proj_label.addChild(ent_type_label)

                self.ui.data_tree.addTopLevelItem(proj_label)
            # self.ui.data_tree.resizeColumnToContents(5)
            # self.ui.data_tree.resizeColumnToContents(6)
            # self.ui.data_tree.resizeColumnToContents(7)
            self.report.close()

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
                    all_tasks = sg_data.get_all_task_steps()
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
        self.update_saved_settings()
        if self.engine.isRunning():
            self.engine.exit()

    def update_saved_settings(self):
        """
        Saves the window settings
        :return:
        """
        self.settings.setValue('geometry', self.saveGeometry())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('AdamBenson')
    app.setOrganizationDomain('adamdbenson.com')
    app.setApplicationName('TimeLordReports')
    splash_pix = QtGui.QPixmap('ui/resources/Time_Lord_Logo.png')
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    w = reports_ui()
    w.show()
    splash.finish(w)
    sys.exit(app.exec_())


