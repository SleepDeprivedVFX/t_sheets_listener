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
    out_time = (datetime.now() - timedelta(hours=1)).time()
    sys.argv += ['-o', str(out_time)]


# -----------------------------------------------------------------------------------------------------------
# Main Window
# -----------------------------------------------------------------------------------------------------------
class end_of_day(QtGui.QWidget):
    def __init__(self):
        super(end_of_day, self).__init__(parent=None)

        # Preps the arguments in case they are missing.
        arguments = sys.argv[1:]
        options = getopt.getopt(arguments, 's:e:', longopts=['start=', 'end='])
        if options[0]:
            split_options = options[0]
            for opt, arg in split_options:
                if opt in ('-o', '--out'):
                    out_time = QtCore.QTime.fromString(arg)

        # Variables
        self.stay_opened = True

        # Setup UI
        self.ui = tle.Ui_endofday()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))

    def stay_clocked_in(self):
        self.stay_opened = False
        self.close()

    def clock_out(self):
        self.stay_opened = False
        latest_timesheet = tl_time.get_last_timesheet(user=user)
        tl_time.clock_out_time_sheet()

    def closeEvent(self, event, *args, **kwargs):
        if self.stay_opened:
            event.ignore()
            logger.warning('You can\'t close the window this way!')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = end_of_day()
    w.show()
    sys.exit(app.exec_())

