"""
The lunch pop-up for getting the lunch times.
"""

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.4.3'

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
log_file = 'lunch_menu.log'
log_root = os.path.join(sys.path[0], 'logs')
if not os.path.exists(log_root):
    os.makedirs(log_root)
log_path = os.path.join(log_root, log_file)
debug = config['debug_logging']
if debug == 'True' or debug == 'true' or debug == True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('lunch_menu')
logger.setLevel(level=level)
fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                              backupCount=int(config['log_days']))
fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
fh.setFormatter(fm)
logger.addHandler(fh)

logger.info('Lunch Utility has started.')

# --------------------------------------------------------------------------------------------------
# Setup Shotgun Connection
# --------------------------------------------------------------------------------------------------
sg = sgapi.Shotgun(config['sg_url'], config['sg_name'], config['sg_key'])
logger.debug('Shotgun is connected.')

# --------------------------------------------------------------------------------------------------
# Connect Time Lord Components
# --------------------------------------------------------------------------------------------------
# setup continuum
tl_time = continuum(sg, config=config, sub='lunch')

# Setup and get users
users = companions(sg, config=config, sub='lunch')
user = users.get_user_from_computer()

# setup shotgun data connection
sg_data = bin.shotgun_collect.sg_data(sg, config=config, sub='lunch')


# --------------------------------------------------------------------------------------------------
# Signal Emitters
# --------------------------------------------------------------------------------------------------
class tardis_signals(QtCore.QObject):
    yes = QtCore.Signal(str)
    no = QtCore.Signal(str)
    timer = QtCore.Signal(str)
    start_time = QtCore.Signal(str)
    end_time = QtCore.Signal(str)
    launch_lunch = QtCore.Signal(str)


# Check the system arguments and append current start and end times if they're missing.
lock_times = True
if len(sys.argv) < 2:
    start = (datetime.now() - timedelta(hours=1)).time()
    end = datetime.now().time()
    sys.argv += ['-s', str(start), '-e', str(end)]
    lock_times = False


class lunch_break(QtGui.QWidget):
    def __init__(self):
        super(lunch_break, self).__init__(parent=None)

        self.signals = tardis_signals()
        self.stay_opened = True
        start_time = None
        end_time = None

        # Get the lunch task ID for creating lunch breaks.
        self.lunch_proj_id = int(config['admin_proj_id'])
        self.lunch_task_name = config['lunch']
        self.lunch_task_id = sg_data.get_lunch_task(lunch_proj_id=self.lunch_proj_id, task_name=self.lunch_task_name)
        if self.lunch_task_id:
            self.lunch_task_id = self.lunch_task_id['id']
        self.entity = config['unpaid_time_off']
        self.entity_id = sg_data.get_entity_id(proj_id=self.lunch_proj_id, entity_name=self.entity)

        arguments = sys.argv[1:]
        options = getopt.getopt(arguments, 's:e:', longopts=['start=', 'end='])
        if options[0]:
            split_options = options[0]
            for opt, arg in split_options:
                if opt in ('-s', '--start'):
                    start_time = QtCore.QTime.fromString(arg)
                elif opt in ('-e', '--end'):
                    end_time = QtCore.QTime.fromString(arg)

        self.ui = tll.Ui_lunch_form()
        self.ui.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
        self.setWindowTitle('The Lunch Line v%s' % __version__)

        self.ui.lunch_message.setText('Hey %s! Were you at lunch at the following times?' % user['name'].split(' ')[0])

        self.ui.ok_btn.clicked.connect(self.take_lunch)
        self.ui.skip_btn.clicked.connect(self.skip_lunch)
        permission = user['permission_rule_set']['name']

        if start_time:
            self.ui.start_time.setTime(start_time)
            if lock_times and permission not in config['permissions']:
                self.ui.start_time.setDisabled(True)
            else:
                self.ui.start_time.setEnabled(True)
        if end_time:
            self.ui.end_time.setTime(end_time)
            if lock_times and permission not in config['permissions']:
                self.ui.end_time.setDisabled(True)
            else:
                self.ui.end_time.setEnabled(True)

    def take_lunch(self, message=None):
        self.signals.yes.emit(message)
        logger.info('Lunch taken... Recording...')
        get_start_time = self.ui.start_time.time().toString()
        get_end_time = self.ui.end_time.time().toString()
        start_time = parser.parse(get_start_time)
        end_time = parser.parse(get_end_time)
        previous_out_time = start_time
        next_start_time = end_time
        current_timesheet = tl_time.get_latest_timesheet(user=user)

        # Clock the user out of the current task at the start of lunch time.
        tl_time.clock_out_time_sheet(timesheet=current_timesheet, clock_out=previous_out_time)

        # Create context and create a lunch entry.
        context = {
            'Project': {
                'id': self.lunch_proj_id,
            },
            'Task': {
                'id': self.lunch_task_id,
                'content': self.lunch_task_name
            }
        }
        tl_time.create_new_timesheet(user=user, context=context, start_time=start_time)
        lunch_timesheet = tl_time.get_latest_timesheet(user=user)
        tl_time.clock_out_time_sheet(timesheet=lunch_timesheet, clock_out=end_time)

        # Build new context and clock the user back in to what they were clocked into before lunch
        context = {
            'Project': {
                'id': current_timesheet['project']['id'],
                'name': current_timesheet['project']['name']
            },
            'Task': {
                'id': current_timesheet['entity']['id'],
                'content': current_timesheet['entity']['name']
            }
        }

        tl_time.create_new_timesheet(user=user, context=context, start_time=next_start_time)
        self.stay_opened = False
        self.close()

    def skip_lunch(self, message=None):
        self.signals.no.emit(message)
        logger.info('Skipping Lunch...')
        self.stay_opened = False
        self.close()

    def closeEvent(self, event, *args, **kwargs):
        if self.stay_opened:
            event.ignore()
            logger.warning('You can\'t close the window this way!')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = lunch_break()
    w.show()
    sys.exit(app.exec_())

