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
__version__ = '0.0.1'

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


class payroll_engine(QtCore.QThread):
    # Main Worker thread.
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.signals = report_signals()

        # Connections
        self.signals.get_payroll.connect(self.make_reports)

    def make_reports(self, data={}):
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


class reports_ui(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.settings = QtCore.QSettings('Adam Benson', 'alpha_payroll_collector')
        self.last_output = self.settings.value('last_output', '.')

        self.engine = payroll_engine()
        self.engine.start()

        self.ui = tlr.Ui_Time_Lord_Reports()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))

        # Set the start and end dates
        self.guess_dates()

        # Set combo box options
        width = self.ui.secondary_org.minimumSizeHint().width()
        self.ui.secondary_org.setMinimumWidth(width)

        # Make change set connections
        self.ui.primary_org.currentIndexChanged.connect(lambda: self.set_search_options(driver=self.ui.primary_org,
                                                                                        list=self.ui.secondary_org))
        self.ui.secondary_org.currentIndexChanged.connect(lambda: self.set_search_options(driver=self.ui.secondary_org,
                                                                                          list=self.ui.trinary_org))

    def guess_dates(self):
        guess_end_date = (datetime.today() - timedelta(days=(datetime.today().isoweekday() % 7) + 1)).date()
        guess_start_date = (guess_end_date - timedelta(days=13))
        self.ui.start_time.setDate(guess_start_date)
        self.ui.end_time.setDate(guess_end_date)

    def set_search_options(self, driver=None, list=None):
        drv_obj = driver.currentText()
        drv_obj_index = driver.currentIndex()
        drv_obj_name = driver.objectName()
        if drv_obj != 'None' or drv_obj_index > 0:
            list.clear()
            if drv_obj_name == 'primary_org':
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
                            list.addItem(proj['name'], proj['id'])
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
                    pass
                else:
                    list.addItem('None', 0)
        else:
            list.clear()
            list.addItem('None', 0)
        width = list.minimumSizeHint().width()
        print('Width: %s' % width)
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


