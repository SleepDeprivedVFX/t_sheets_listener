"""
The lunch pop-up for getting the lunch times.
"""

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.4.0'

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
debug = config['debug_logging']
if debug == 'True' or debug == 'true' or debug == True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('end_of_day')
logger.setLevel(level=level)
fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                              backupCount=int(config['log_days']))
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
tl_time = continuum(sg, config=config, sub='eod')

# Setup and get users
users = companions(sg, config=config, sub='eod')
user = users.get_user_from_computer()

# setup shotgun data connection
sg_data = bin.shotgun_collect.sg_data(sg, config=config, sub='eod')

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
    set_button = QtCore.Signal(str)
    interrupt = QtCore.Signal(bool)


class eod_timer(QtCore.QThread):
    def __init__(self, parent=None):
        super(eod_timer, self).__init__(parent)

        self.eod_signals = eod_signals()
        self.kill_it = False
        self.set_time = None
        self.eod_signals.kill_signal.connect(self.kill)
        self.eod_signals.set_time.connect(self.out_time)

        self.timer = int(config['timer'])

    def out_time(self, message=None):
        logger.info('out_time message: %s' % message)
        # if message:
        self.set_time = message
        # else:
        #     self.set_time = None

    def kill(self):
        self.kill_it = True

    def run(self, *args, **kwargs):
        self.chronograph()

    def chronograph(self):
        second = int(datetime.now().second)
        minute = int(datetime.now().minute)
        user_clocked_in = tl_time.is_user_clocked_in(user=user)

        # Start the timer loop.
        while not self.kill_it:
            if int(datetime.now().second) != second:
                # Make sure the chronograph has the set time from the ui
                if not self.set_time:
                    self.eod_signals.get_time.emit(True)

                # Set the auto-clock-out time
                if self.set_time:
                    # print('if self.set_time: %s' % self.set_time)
                    set_time = parser.parse(self.set_time)
                    auto_clock_out = set_time + timedelta(minutes=(self.timer * 2))
                else:
                    self.eod_signals.get_time.emit(True)
                    auto_clock_out = None

                # Do an occasional check of user clock in status
                if int(datetime.now().minute) != minute:
                    minute = int(datetime.now().minute)
                    # if not user_clocked_in:
                    user_clocked_in = tl_time.is_user_clocked_in(user=user)
                    if not user_clocked_in:
                        self.eod_signals.interrupt.emit(True)
                # Set the clocks
                second = int(datetime.now().second)
                if auto_clock_out:
                    time_left = str(auto_clock_out - datetime.now())
                else:
                    time_left = '00:00:00'
                self.eod_signals.set_button.emit('Clock Out: %s' % time_left)
                # logger.info('auto_clock_out', auto_clock_out)
                # logger.info(datetime.now())
                if auto_clock_out and datetime.now() > auto_clock_out and user_clocked_in:
                    self.eod_signals.last_time.emit('Time Lord Auto Clock Out')
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
                    logger.info('out time: %s' % time_out)

        if not time_out:
            time_out = datetime.now()

        # Variables
        self.stay_opened = True

        # Setup UI
        self.ui = tle.Ui_endofday()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
        self.setWindowTitle('End Of Day v%s' % __version__)

        self.ui.yes_btn.clicked.connect(self.stay_clocked_in)
        self.ui.no_btn.clicked.connect(self.clock_out)
        self.ui.last_time.setDateTime(time_out)

        # Threads and connections
        self.eod_timer = eod_timer()
        self.eod_timer.eod_signals.last_time.connect(self.clock_out)
        self.eod_timer.eod_signals.get_time.connect(self.set_time)
        self.eod_timer.eod_signals.set_button.connect(self.set_button)
        self.eod_timer.eod_signals.interrupt.connect(self.stay_clocked_in)
        self.eod_timer.start()
        self.eod_timer.eod_signals.set_time.emit(time_out)

    def set_button(self, text=None):
        if text:
            self.ui.no_btn.setText(text)

    def stay_clocked_in(self):
        # This routine basically just closes the window and takes no further action.  It's like a close feature.
        self.stay_opened = False
        self.eod_timer.kill_it = True
        self.close()

    def set_time(self, message=None):
        get_time = self.ui.last_time.text()
        time_out = str(parser.parse(get_time))
        self.eod_timer.eod_signals.set_time.emit(time_out)

    def clock_out(self, auto=None):
        self.stay_opened = False
        time_out = parser.parse(self.ui.last_time.text())
        if tl_time.is_user_clocked_in(user=user):
            latest_timesheet = tl_time.get_latest_timesheet(user=user)
            tl_time.clock_out_time_sheet(timesheet=latest_timesheet, clock_out=time_out, auto=auto)
        self.eod_timer.kill_it = True
        self.close()

    def closeEvent(self, event, *args, **kwargs):
        if self.stay_opened:
            self.eod_timer.kill_it = True
            event.ignore()
            logger.warning('You can\'t close the window this way!')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = end_of_day()
    w.show()
    sys.exit(app.exec_())

