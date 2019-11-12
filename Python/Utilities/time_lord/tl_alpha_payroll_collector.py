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



