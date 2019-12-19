"""
The Scope is a simple viewer for seeing who is clocked in, what they're working on, and how long they've been doing it.
It is an admin only tool.
"""

import shotgun_api3 as sgapi
import os
import sys
from PySide import QtGui, QtCore
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta
from dateutil import parser
import time
import math

# Time Lord Libraries
from bin.time_continuum import continuum
from bin.companions import companions
import bin.configuration
import bin.shotgun_collect
from bin.comm_system import comm_sys

from ui import time_lord_scope as tls

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.4.1'

config = bin.configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'scope.log'
log_root = os.path.join(sys.path[0], 'logs')
if not os.path.exists(log_root):
    os.makedirs(log_root)
log_path = os.path.join(log_root, log_file)
debug = config['debug_logging']
if debug == 'True' or debug == 'true' or debug == True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('scope')
logger.setLevel(level=level)
fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                              backupCount=int(config['log_days']))
fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
fh.setFormatter(fm)
logger.addHandler(fh)

logger.info('Scope Utility has started.')

# --------------------------------------------------------------------------------------------------
# Setup Shotgun Connection
# --------------------------------------------------------------------------------------------------
sg = sgapi.Shotgun(config['sg_url'], config['sg_name'], config['sg_key'])
logger.debug('Shotgun is connected.')

# --------------------------------------------------------------------------------------------------
# Connect Time Lord Components
# --------------------------------------------------------------------------------------------------
# setup continuum
tl_time = continuum(sg, config=config, sub='scope')

# Setup and get users
users = companions(sg, config=config, sub='scope')
user = users.get_user_from_computer()

# setup shotgun data connection
sg_data = bin.shotgun_collect.sg_data(sg, config=config, sub='scope')

# Setup the communications system
comm = comm_sys(sg, config=config, sub='scope')


class scope_signals(QtCore.QObject):
    user_running_time = QtCore.Signal(dict)


class scope_engine(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

        self.scope_signals = scope_signals()

        # Build Scope
        self.scope = {258: {'name': 'John Ployhar'}}

    def run(self, *args, **kwargs):
        second = int(datetime.now().second)
        minute = datetime.now().minute
        active_timesheets = tl_time.get_active_timesheets()
        self.compare_lists(active_timesheets)
        while True:
            if second != int(datetime.now().second):
                second = int(datetime.now().second)
                if minute != datetime.now().minute:
                    minute = datetime.now().minute
                    active_timesheets = tl_time.get_active_timesheets()
                    self.compare_lists(active_timesheets)
                    print self.scope

                    # Update the Lists:

    def compare_lists(self, timesheets=None):
        # Check the timesheets against the scope list
        if timesheets:
            for timesheet in timesheets:
                user = timesheet['user']
                username = user['name']
                userid = user['id']
                project = timesheet['project']
                proj_name = project['name']
                proj_id = project['id']
                task = timesheet['entity']
                task_name = task['name']
                task_id = task['id']
                start_time = timesheet['sg_task_start']

                if userid not in self.scope.keys():
                    self.scope[userid] = {
                        'name': username,
                        'project': proj_name,
                        'proj_id': proj_id,
                        'entity': None,
                        'task': task_name,
                        'task_id': task_id,
                        'start_time': start_time,
                        'table_id': None
                    }

        # Check Scope List against Timesheets
        for uid, data in self.scope.items():
            # test = next(item for item in timesheets if item['user']['id'] == uid)
            test = filter(lambda item: item['user']['id'] == uid, timesheets)
            if not test:
                # remove from the scope
                del self.scope[uid]


class scope(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.scope_engine = scope_engine()

        self.ui = tls.Ui_WhosWorking()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))

        # Setup column widths
        header = self.ui.slave_list.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        header.setResizeMode(3, QtGui.QHeaderView.Stretch)

        self.ui.slave_list.clear()
        self.scope_engine.start()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    o = scope()
    o.show()
    sys.exit(app.exec_())



