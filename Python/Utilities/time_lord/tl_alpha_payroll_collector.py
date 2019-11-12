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
from dateutil import parser
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
import shotgun_api3 as sgapi


__author__ = 'Adam Benson'
__version__ = '0.0.1'

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


# ------------------------------------------------------------------------------------------------
# Signal Emitters
# ------------------------------------------------------------------------------------------------
class payroll_signals(QtCore.QObject):
    output_monitor = QtCore.Signal(str)


class payroll_engine(QtCore.QThread):
    # Main Worker thread.
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)


class payroll_ui(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.ui = apc.Ui_QuickPayroll()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = payroll_ui()
    w.show()
    sys.exit(app.exec_())


