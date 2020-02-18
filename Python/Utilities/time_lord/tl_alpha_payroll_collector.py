"""
This utility is an early stage bridge designed to get data from the Time Lord and Shotgun Systems
and save it to an Excel Spreadsheet.  It is a temporary system which will eventually be replaced by
a possible NIM connection (for ASC) and possibly a direct connection to PayChex.  We'll see how it
goes.
"""

from ui import time_lord_alpha_payroll_collector as apc
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
__version__ = '0.5.1'

config = configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'tl_alpha_payroll_collect.log'
log_root = os.path.join(sys.path[0], 'logs')
if not os.path.exists(log_root):
    os.makedirs(log_root)
log_path = os.path.join(log_root, log_file)
debug = config['debug_logging']
if debug == 'True' or debug == 'true' or debug == True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('payroll_collect')
logger.setLevel(level=level)
fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                              backupCount=int(config['log_days']))
fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
fh.setFormatter(fm)
logger.addHandler(fh)

logger.info('Alpha Payroll Collection Utility has started.')

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
class payroll_signals(QtCore.QObject):
    output_monitor = QtCore.Signal(dict)
    get_payroll = QtCore.Signal(dict)


class payroll_engine(QtCore.QThread):
    # Main Worker thread.
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.signals = payroll_signals()

        # Connections
        self.signals.get_payroll.connect(self.collect_payroll)

    def collect_payroll(self, data={}):
        if data:
            # print('Data: %s' % data)
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


class payroll_ui(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.settings = QtCore.QSettings('Adam Benson', 'alpha_payroll_collector')
        self.last_output = self.settings.value('last_output', '.')

        self.engine = payroll_engine()
        self.engine.start()

        self.ui = apc.Ui_QuickPayroll()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))

        # Setup column widths
        header = self.ui.screen_output.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)

        # Setup the connections.
        self.ui.file_output_btn.clicked.connect(self.set_output_file)
        self.ui.cancel_btn.clicked.connect(self.cancel)
        self.ui.process_btn.clicked.connect(self.request_payroll)

        # Defaults
        self.ui.screen_output.clear()
        self.guess_dates()

        self.engine.signals.output_monitor.connect(self.update_monitor)

    def guess_dates(self):
        guess_end_date = (datetime.today() - timedelta(days=(datetime.today().isoweekday() % 7) + 1)).date()
        guess_start_date = (guess_end_date - timedelta(days=13))
        self.ui.start_date.setDate(guess_start_date)
        self.ui.end_date.setDate(guess_end_date)

    def cancel(self):
        self.close()

    def set_output_file(self):
        output = QtGui.QFileDialog.getSaveFileName(self, 'Save File As', self.settings.value('last_output'),
                                                   '*.xlsx *.xls')
        if output[0]:
            self.settings.setValue('last_output', output[0])
            self.ui.file_output.setText(output[0])

    def request_payroll(self):
        output_file = self.ui.file_output.text()
        if not output_file:
            logger.warning('No File Output Set!')
            return False
        start_date = self.ui.start_date.text()
        print('Start_date: %s' % start_date)
        end_date = self.ui.end_date.text()
        print('End_date: %s' % end_date)

        request = {'output': output_file, 'start': start_date, 'end': end_date}
        self.engine.signals.get_payroll.emit(request)

    def update_monitor(self, monitor=None):
        if monitor:
            name = monitor['name']
            wage_type = ' %s ' % monitor['type']
            level = ' %s ' % monitor['level']
            total = str(monitor['total'])

            row_count = self.ui.screen_output.rowCount()
            if row_count > 1:
                row = row_count - 1
            else:
                row = 0
            self.ui.screen_output.insertRow(row)
            name_label = QtGui.QLabel()
            name_label.setText(name)
            self.ui.screen_output.setCellWidget(row, 0, name_label)
            wage_label = QtGui.QLabel()
            wage_label.setText(wage_type)
            self.ui.screen_output.setCellWidget(row, 1, wage_label)
            level_label = QtGui.QLabel()
            level_label.setText(level)
            self.ui.screen_output.setCellWidget(row, 2, level_label)
            dots = QtGui.QLabel()
            dots.setText('.' * 200)
            self.ui.screen_output.setCellWidget(row, 3, dots)
            total_label = QtGui.QLabel()
            total_label.setText(total)
            self.ui.screen_output.setCellWidget(row, 4, total_label)

    def closeEvent(self, *args, **kwargs):
        if self.engine.isRunning():
            while self.engine.isRunning():
                self.engine.quit()
            self.engine.exit()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = payroll_ui()
    w.show()
    sys.exit(app.exec_())


