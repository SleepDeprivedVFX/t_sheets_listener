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
"""

import shotgun_api3 as sgapi
import os
import sys
from PySide import QtGui, QtCore
import ConfigParser
import logging

# Time Lord Libraries
from bin.time_continuum import continuum

from ui import time_lord_clock as tlu

sys_path = sys.path
config_file = 'dalek.cfg'
try:
    print 'Finding configuration file...'
    config_path = [f for f in sys_path if os.path.isfile(f + '/' + config_file)][0] + '/' + config_file
    config_path = config_path.replace('\\', '/')
    print 'Configuration found!'
except IndexError, e:
    raise e

# Create the configuration connection
configuration = ConfigParser.ConfigParser()
print 'Reading the configuration file...'
configuration.read(config_path)

# Parse out the configuration to local variables
# Shotgun
cfg_sg_url = configuration.get('Shotgun', 'sg_url')
cfg_sg_key = configuration.get('Shotgun', 'sg_key')
cfg_sg_name = configuration.get('Shotgun', 'sg_name')

# Time Lord
cfg_regular_days = configuration.get('Time Lord', 'regular_days')
cfg_weekend_days = configuration.get('Time Lord', 'weekend_days')
cfg_regular_start = configuration.get('Time Lord', 'regular_start')
cfg_regular_end = configuration.get('Time Lord', 'regular_end')
cfg_approx_lunch_start = configuration.get('Time Lord', 'approx_lunch_start')
cfg_approx_lunch_end = configuration.get('Time Lord', 'approx_lunch_end')
cfg_ot_type = configuration.get('Time Lord', 'ot_type')
cfg_ot_hours = configuration.get('Time Lord', 'ot_hours')
cfg_dt_hours = configuration.get('Time Lord', 'dt_hours')

# Logging
cfg_debug_logging = configuration.get('Logging', 'debugging')
cfg_log_path = configuration.get('Logging', 'log_path')

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'psychic_paper.log'
log_path = os.path.join(cfg_log_path, log_file)

logger = logging.getLogger('psychic_paper')
if cfg_debug_logging == 'True' or True:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
fh = logging.FileHandler(log_path)
lf = logging.Formatter('%(asctime)s - :%(lineno)d - %(message)s')
logger.addHandler(lf)
logger.addHandler(fh)

logger.info('The Time Lord has started!')

# Setup Shotgun Connection
sg = sgapi.Shotgun(cfg_sg_url, cfg_sg_name, cfg_sg_key)

# setup continuum
cont = continuum()


# ------------------------------------------------------------------------------------------------------
# Signal Emitters
# ------------------------------------------------------------------------------------------------------
class time_signals(QtCore.QObject):
    log = QtCore.Signal(str)
    error = QtCore.Signal(str)
    debug = QtCore.Signal(str)


# ------------------------------------------------------------------------------------------------------
# Primary Issues
# ------------------------------------------------------------------------------------------------------
class time_engine(QtCore.QThread):
    pass


class time_lord:
    def __init__(self):
        pass


class time_lord_ui(QtGui.QMainWindow):

    def __init__(self):
        super(time_lord_ui, self).__init__(parent=None)

        # Setup settings system
        self.settings = QtCore.QSettings('AdamBenson', 'TimeLord')

        # Setup UI
        self.ui = tlu.Ui_TimeLord()
        self.ui.setupUi(self)
        self.ui.daily_total_progress.setValue(12)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('AdamBenson')
    app.setOrganizationDomain('adamdbenson.com')
    app.setApplicationName('TimeLord')
    window = time_lord_ui()
    window.show()
    sys.exit(app.exec_())

