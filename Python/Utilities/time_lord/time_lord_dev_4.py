"""
Another rebuild of the Time Lord System.  Loosely based on 0.5.1, the first Python 3 upgrade attempt.
"""

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.5.2'


import shotgun_api3 as sgapi
import os
import sys
from PySide2 import QtGui, QtCore, QtWidgets
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from dateutil import parser
import pickle

# Time Lord Libraries
from bin.time_continuum import continuum
from bin.companions import companions
from bin import configuration
from bin import shotgun_collect
from bin import comm_system
from ui import time_lord_clock as tlu
import time
import socket
import inspect
import pprint

config = configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'psychic_paper.log'
log_root = os.path.join(sys.path[0], 'logs')
log_path = os.path.join(log_root, log_file)
debug = config['debug_logging']
if debug == 'True' or debug == 'true' or debug == True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('psychic_paper')
logger.setLevel(level=level)
fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                              backupCount=int(config['log_days']))
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
tl_time = continuum(sg, config=config, sub='time_lord')

# Setup and get users
users = companions(sg, config=config, sub='time_lord')
user = users.get_user_from_computer()

# setup shotgun data connection
sg_data = shotgun_collect.sg_data(sg, config=config, sub='time_lord')

lunch_task = sg_data.get_lunch_task(lunch_proj_id=int(config['admin_proj_id']),
                                    task_name=config['lunch'])

# --------------------------------------------------------------------------------------------------
# Setup the comm system
# --------------------------------------------------------------------------------------------------
comm = comm_system.comm_sys(sg, config=config, sub='time_lord')
logger.info('Communication system online.')

