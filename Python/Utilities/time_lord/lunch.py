"""
The lunch pop-up for getting the lunch times.
"""

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.4.9'

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

lunch_proj_id = int(config['admin_proj_id'])
lunch_task_id = sg_data.get_lunch_task(lunch_proj_id=lunch_proj_id, task_name=config['lunch'])
if lunch_task_id:
    lunch_task_id = int(lunch_task_id['id'])

# Check the system arguments and append current start and end times if they're missing.
lock_times = False
lunch_message = 'Hey %s!\nThe system detected you were at lunch during the times below. ' \
                'Did you take your lunch?' % user['name'].split(' ')[0]
skip_button = 'Not Now'
ok_button = 'Yes! I took my lunch'
lock_buttons = False

# Get the current lunch status
todays_lunch = tl_time.get_todays_lunch(user=user, lunch_id=int(lunch_task_id), lunch_proj_id=int(lunch_proj_id))

# Check the incoming arguments and set ui variables
if len(sys.argv) < 2:
    if todays_lunch:
        start = todays_lunch[0]['sg_task_start'].time()
        end = todays_lunch[0]['sg_task_end'].time()
        lunch_message = 'You have already logged a lunch for today.  If you need to make changes, see one of the ' \
                        'supervisors.'
        skip_button = 'Close'
        lock_times = True
        lock_buttons = True
    else:
        start = (datetime.now() - timedelta(hours=1)).time()
        end = datetime.now().time()
        lunch_message = 'Hey %s\n. You have not clocked a lunch today! ' \
                        'Please record your lunch now!' % user['name'].split(' ')[0]
        skip_button = 'I skipped lunch.'
        ok_button = 'Record my lunch!'
        lock_times = False
    sys.argv += ['-s', str(start), '-e', str(end)]


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
    kill_it = QtCore.Signal(bool)


class self_destruct(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.kill_me = False

        # Setup a lunch window open time variable and a close time variable
        self.close_time = datetime.now() + timedelta(hours=3)

        self.signals = tardis_signals()

    def run(self, *args, **kwargs):
        self.check_time()

    def kill(self):
        self.kill_me = True

    def check_time(self):
        while not self.kill_me:
            time.sleep(1)
            print('Looping....')
            if datetime.now() > self.close_time:
                print('SEND CLOSE')
                self.kill_me = True
                self.signals.kill_it.emit(True)


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

        self.ui.lunch_message.setText(lunch_message)
        self.ui.skip_btn.setText(skip_button)

        self.ui.ok_btn.clicked.connect(self.take_lunch)
        self.ui.skip_btn.clicked.connect(self.skip_lunch)
        permission = user['permission_rule_set']['name']

        if lock_buttons:
            self.ui.ok_btn.setText('Already Logged')
            self.ui.ok_btn.setStyleSheet('background-color: rgb(85, 85, 127)')
            self.ui.ok_btn.setDisabled(True)
        else:
            self.ui.ok_btn.setText(ok_button)

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

        # Connect the Kill It Timer
        self.destruct = self_destruct()
        self.destruct.signals.kill_it.connect(self.kill_it)
        self.destruct.start()

    def kill_it(self, death=False):
        if death:
            self.stay_opened = False
            self.close()

    def take_lunch(self, message=None):
        self.signals.yes.emit(message)
        logger.info('Lunch taken... Recording...')
        get_start_time = self.ui.start_time.time().toString()
        get_end_time = self.ui.end_time.time().toString()
        start_time = parser.parse(get_start_time)
        end_time = parser.parse(get_end_time)
        previous_out_time = start_time
        next_start_time = end_time
        latest_timesheet = tl_time.get_latest_timesheet(user=user)
        current_timesheet = tl_time.get_previous_timesheet(user=user, start_time=start_time)
        current_timesheet_out = current_timesheet['sg_task_end']

        # Clock the user out of the current task at the start of lunch time.
        # FIXME: This automatically clocks someone out, but that doesn't work for manually added lunch breaks.
        #       Needs a way to check times against previous entries and next entries.
        #       i.e. User lunch = start: 11:00 end: 12:00.
        #           User adds this at 3:00, but has clocked into 3 other things already since then:
        #           job1 start: 10:30 end: 12:15
        #           job2 start: 12:15 end: 01:30
        #           job3 start: 01:30 end:
        #           Search: User start time: If before current record start, get previous record.  Repeat until current
        #           record starts after other record.  Get that timesheet ID and do the following to that timesheet.
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
        lunch_sheet = tl_time.create_new_timesheet(user=user, context=context, start_time=start_time)
        lunch_timesheet = tl_time.get_timesheet_by_id(tid=lunch_sheet['id'])
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

        if current_timesheet['id'] == latest_timesheet['id']:
            tl_time.create_new_timesheet(user=user, context=context, start_time=next_start_time)
        else:
            next_timesheet = tl_time.get_next_timesheet(user=user, start_time=start_time, tid=current_timesheet['id'])
            next_sheet_start = next_timesheet['sg_task_start']
            next_sheet_start = '%s %s:%s:%s' % (next_sheet_start.date(), next_sheet_start.time().hour,
                                                next_sheet_start.time().minute, next_sheet_start.time().second)
            next_sheet_start = datetime.strptime(next_sheet_start, '%Y-%m-%d %H:%M:%S')
            if next_sheet_start < end_time:
                tl_time.update_current_times(user=user, tid=next_timesheet['id'], start_time=end_time)
            elif next_sheet_start > end_time:
                filler_timesheet = tl_time.create_new_timesheet(user=user, context=context, start_time=end_time)
                if current_timesheet_out:
                    tl_time.clock_out_time_sheet(timesheet=filler_timesheet, clock_out=current_timesheet_out)
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
        if self.destruct.isRunning():
            while self.destruct.isRunning():
                self.destruct.kill_me = True
                self.destruct.quit()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = lunch_break()
    w.show()
    sys.exit(app.exec_())

