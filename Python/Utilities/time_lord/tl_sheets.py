"""
The lunch pop-up for getting the lunch times.
"""

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.4.6'

import shotgun_api3 as sgapi
import os
import sys
import getopt
from PySide import QtGui, QtCore
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta
from dateutil import parser

# Time Lord Libraries
from bin.time_continuum import continuum
from bin.companions import companions
import bin.configuration
import bin.shotgun_collect

from ui import time_lord_lunch as tll

config = bin.configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'sheets.log'
log_root = os.path.join(sys.path[0], 'logs')
if not os.path.exists(log_root):
    os.makedirs(log_root)
log_path = os.path.join(log_root, log_file)
debug = config['debug_logging']
if debug == 'True' or debug == 'true' or debug == True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('sheets')
logger.setLevel(level=level)
fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                              backupCount=int(config['log_days']))
fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
fh.setFormatter(fm)
logger.addHandler(fh)

logger.info('Sheets Utility has started.')

# --------------------------------------------------------------------------------------------------
# Setup Shotgun Connection
# --------------------------------------------------------------------------------------------------
sg = sgapi.Shotgun(config['sg_url'], config['sg_name'], config['sg_key'])
logger.debug('Shotgun is connected.')

# --------------------------------------------------------------------------------------------------
# Connect Time Lord Components
# --------------------------------------------------------------------------------------------------
# setup continuum
tl_time = continuum(sg, config=config, sub='sheets')

# Setup and get users
users = companions(sg, config=config, sub='sheets')
user = users.get_user_from_computer()

# setup shotgun data connection
sg_data = bin.shotgun_collect.sg_data(sg, config=config, sub='sheets')

lunch_proj_id = int(config['admin_proj_id'])
lunch_task_id = sg_data.get_lunch_task(lunch_proj_id=lunch_proj_id, task_name=config['lunch'])
if lunch_task_id:
    lunch_task_id = int(lunch_task_id['id'])


class sheets(QtGui.QWidget):
    pass


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('AdamBenson')
    app.setOrganizationDomain('adamdbenson.com')
    app.setApplicationName('Sheets')
    o = sheets()
    o.show()
    sys.exit(app.exec_())

