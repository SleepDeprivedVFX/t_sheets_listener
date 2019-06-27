"""
TIME LORD

Design and implementation are based around the Doctor Who character.  Everything
will be named accordingly.

This system is being designed to interact with Shotgun and any number of DCCs.
Here is a list of it's basic requirements:

    1. Replace T-Sheets with a user interface that allows artists to clock in and out of tasks in the same way.
    2. Integrate into Shotgun DCCs.  Detect files that are not currently clocked in, and (possibly) automatically
        update the time sheet with the data at hand.
    3. Be able to detect files put into an IAP (Internal Auto Publisher) and retroactively check time sheets against
        what the artist was clocked into.  For example:
            Artist drops a file into the system at 12:30.  The were not clocked in. System assumes a 10 am start time
            and clocks them in at 10 and continues counting forward or clocks out.
            Artist drops a a file into the system at 3:30.  The last file was at 12:30.  The system adjusts the clock
            to make the new file clock in at 12:30 and out at 3:30.
Without the need for doubling up the database in T-Sheets the new system should actually be much lighter, since it will
only be running simple shotgun commands on things.

NOTES:
    1. The user is always the main entry point.  No user, no time log.  Thus:
        a. The main UI running on someone's computer will take their login account to get the user
        b. The IAP account will get it's user data from the server upon drag-n-drop

REQUIREMENTS:
    1. This tool will most likely require ActiveState python to be installed on everyone's systems.
"""

import shotgun_api3 as sgapi
import os
import sys
from PySide import QtGui, QtCore
import logging
from datetime import datetime

# Time Lord Libraries
from bin.time_continuum import continuum
from bin.companions import companions
from bin import configuration
from ui import time_lord_clock as tlu

config = configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'psychic_paper.log'
log_path = os.path.join(config['log_path'], log_file)
if config['debug_logging'] == 'True' or 'true' or True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('psychic_paper')
logger.setLevel(level=level)
fh = logging.FileHandler(filename=log_path)
fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
fh.setFormatter(fm)
logger.addHandler(fh)

logger.info('The Time Lord has started!')

# --------------------------------------------------------------------------------------------------
# Setup Shotgun Connection
# --------------------------------------------------------------------------------------------------
sg = sgapi.Shotgun(config['sg_url'], config['sg_name'], config['sg_key'])
logger.debug('Shotgun is connected.')

# --------------------------------------------------------------------------------------------------
# Connect Time Lord Components
# --------------------------------------------------------------------------------------------------
# setup continuum
cont = continuum(sg)

# Setup and get users
users = companions(sg)
user = users.get_user_from_computer()
if user:
    print user['name']
else:
    print 'User could not be found!'


# ------------------------------------------------------------------------------------------------------
# Signal Emitters
# ------------------------------------------------------------------------------------------------------
class time_signals(QtCore.QObject):
    log = QtCore.Signal(str)
    error = QtCore.Signal(str)
    debug = QtCore.Signal(str)
    kill_signal = QtCore.Signal(bool)
    main_clock = QtCore.Signal(str)
    in_clock = QtCore.Signal(str)
    out_clock = QtCore.Signal(str)


# ------------------------------------------------------------------------------------------------------
# Primary Issues
# ------------------------------------------------------------------------------------------------------
class time_engine(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.time_signal = time_signals()
        self.kill_it = False
        self.kill_signal = self.time_signal.kill_signal.connect(self.kill)

    def kill(self):
        self.kill_it = True

    def run(self, *args, **kwargs):
        self.run_the_clock()

    def run_the_clock(self):
        second = int(datetime.now().second)
        while not self.kill_it:
            if int(datetime.now().second) != second:
                second = int(datetime.now().second)
                self.time_signal.main_clock.emit(str(second))


class time_lord_ui(QtGui.QMainWindow):

    def __init__(self):
        super(time_lord_ui, self).__init__(parent=None)

        # Setup settings system
        self.settings = QtCore.QSettings('AdamBenson', 'TimeLord')

        # Signal setup
        self.time_signal = time_signals()

        # Setup Engine
        self.time_engine = time_engine()

        # Setup UI
        self.ui = tlu.Ui_TimeLord()
        self.ui.setupUi(self)

        # Set main user info
        self.ui.artist_label.setText(user['name'])

        # self.ui.daily_total_progress.setValue(12)
        self.ui.clock_button.clicked.connect(self.start_time)

        # Connect the signals to the functions below
        self.time_engine.time_signal.main_clock.connect(self.main_clock)

        test = QtGui.QTransform()
        test.rotate(45)
        self.ui.time_hour.setTransform(test)

        # The following test line will need to be automatically filled in future
        # cont.get_previous_work_day('06-17-2019', regular_days=config['regular_days'])

    def start_time(self):
        self.time_engine.kill_it = False
        self.time_engine.start()

    def main_clock(self, in_time):
        # Function that automatically updates UI when triggered by a signal
        # self.ui.test_counter.setText(in_time)
        angle = int(in_time) * 6
        test = QtGui.QTransform()
        test.rotate(angle)
        self.ui.time_hour.setTransform(test)
        self.ui.time_hour.update()
        print angle


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('AdamBenson')
    app.setOrganizationDomain('adamdbenson.com')
    app.setApplicationName('TimeLord')
    window = time_lord_ui()
    window.show()
    sys.exit(app.exec_())

