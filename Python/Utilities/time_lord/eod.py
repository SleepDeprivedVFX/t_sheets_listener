"""
The lunch pop-up for getting the lunch times.
"""

import shotgun_api3 as sgapi
import os
import sys
import getopt
from PySide import QtGui, QtCore
import logging
from datetime import datetime, timedelta
from dateutil import parser

# Time Lord Libraries
from bin.time_continuum import continuum
from bin.companions import companions
import bin.configuration
import bin.shotgun_collect

from ui import time_lord_eod as tle

config = bin.configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'end_of_day.log'
log_root = os.path.join(sys.path[0], 'logs')
if not os.path.exists(log_root):
    os.makedirs(log_root)
log_path = os.path.join(log_root, log_file)
if config['debug_logging'] == 'True' or 'true' or True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('end_of_day')
logger.setLevel(level=level)
fh = logging.FileHandler(filename=log_path)
fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
fh.setFormatter(fm)
logger.addHandler(fh)


logger.info('End of Day has started.')

# --------------------------------------------------------------------------------------------------
# Setup Shotgun Connection
# --------------------------------------------------------------------------------------------------
sg = sgapi.Shotgun(config['sg_url'], config['sg_name'], config['sg_key'])
logger.debug('Shotgun is connected.')

# --------------------------------------------------------------------------------------------------
# Connect Time Lord Components
# --------------------------------------------------------------------------------------------------
# setup continuum
tl_time = continuum(sg)

# Setup and get users
users = companions(sg)
user = users.get_user_from_computer()

# setup shotgun data connection
sg_data = bin.shotgun_collect.sg_data(sg)

# Check the system arguments and append current start and end times if they're missing.
if len(sys.argv) < 2:
    out_time = (datetime.now() - timedelta(minutes=int(config['timer'])))
    sys.argv += ['-o', str(out_time)]


# -----------------------------------------------------------------------------------------------------------
# Signals and Threads
# -----------------------------------------------------------------------------------------------------------
class eod_signals(QtCore.QObject):
    last_time = QtCore.Signal(str)
    kill_signal = QtCore.Signal(bool)
    set_time = QtCore.Signal(str)
    get_time = QtCore.Signal(bool)


class eod_timer(QtCore.QThread):
    def __init__(self, parent=None):
        super(eod_timer, self).__init__(parent)

        self.eod_signals = eod_signals()
        self.kill_it = False
        self.set_time = None
        self.eod_signals.kill_signal.connect(self.kill)
        self.eod_signals.set_time.connect(self.out_time)

    def out_time(self, message=None):
        print 'out_time message: %s' % message
        self.set_time = parser.parse(message)

    def kill(self):
        self.kill_it = True

    def run(self, *args, **kwargs):
        self.chronograph()

    def chronograph(self):
        second = int(datetime.now().second)

        # Make sure the chronograph has the set time from the ui
        if not self.set_time:
            self.eod_signals.get_time.emit(True)

        # Set the auto-clock-out time
        auto_clock_out = self.set_time + timedelta(minutes=int(config['timer']))

        # Start the timer loop.
        while not self.kill_it:
            if int(datetime.now().second) != second:
                # Set the clocks
                second = int(datetime.now().second)
                if datetime.now() > auto_clock_out:
                    self.eod_signals.last_time.emit('Clock out')
                    self.kill_it = True


# -----------------------------------------------------------------------------------------------------------
# Main Window
# -----------------------------------------------------------------------------------------------------------
class end_of_day(QtGui.QWidget):
    def __init__(self):
        super(end_of_day, self).__init__(parent=None)

        # Preps the arguments in case they are missing.
        arguments = sys.argv[1:]
        options = getopt.getopt(arguments, 'o:', longopts=['out='])
        time_out = None
        if options[0]:
            split_options = options[0]
            for opt, arg in split_options:
                if opt in ('-o', '--out'):
                    time_out = parser.parse(arg)
                    print 'out time: %s' % time_out

        if not time_out:
            time_out = datetime.now()

        # Variables
        self.stay_opened = True

        # Setup UI
        self.ui = tle.Ui_endofday()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))

        self.ui.yes_btn.clicked.connect(self.stay_clocked_in)
        self.ui.no_btn.clicked.connect(self.clock_out)
        self.ui.last_time.setDateTime(time_out)

        # Threads and connections
        self.eod_timer = eod_timer()
        self.eod_timer.eod_signals.last_time.connect(self.clock_out)
        self.eod_timer.eod_signals.get_time.connect(self.set_time)
        self.eod_timer.start()
        self.eod_timer.eod_signals.set_time.emit(time_out)

    def stay_clocked_in(self):
        self.stay_opened = False
        self.close()

    def set_time(self):
        get_time = self.ui.last_time.text()
        print 'set_time get_time: %s' % get_time
        time_out = parser.parse(get_time)
        print 'time_out sends: %s' % time_out
        self.eod_timer.eod_signals.set_time.emit(time_out)

    def clock_out(self):
        self.stay_opened = False
        time_out = self.ui.last_time.text()
        latest_timesheet = tl_time.get_last_timesheet(user=user)
        tl_time.clock_out_time_sheet(timesheet=latest_timesheet, clock_out=time_out)
        self.close()

    def closeEvent(self, event, *args, **kwargs):
        if self.stay_opened:
            event.ignore()
            logger.warning('You can\'t close the window this way!')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = end_of_day()
    w.show()
    sys.exit(app.exec_())

