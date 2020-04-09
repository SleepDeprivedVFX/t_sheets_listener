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
import json
import queue

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

# Setup the Time Queue
q = queue.Queue(maxsize=0)

# -------------------------------------------------------------------------------------------------------------------
# Stream Handler
# -------------------------------------------------------------------------------------------------------------------
# NOTE: Do I actually need the stream handler?  Can I get by (or be better off) with more practical messages being
#       posted to the UI?


# ------------------------------------------------------------------------------------------------------
# Signal Emitters
# ------------------------------------------------------------------------------------------------------
# NOTE: Might be best to create these as needed, rather than copying the existing ones.
class time_signals(QtCore.QObject):
    # Logger Signals

    # Timesheet Signals
    get_timesheet = QtCore.Signal(dict)
    set_timesheet = QtCore.Signal(dict)
    set_daily_total_needle = QtCore.Signal(float)
    set_weekly_total_needle = QtCore.Signal(float)
    set_daily_total = QtCore.Signal(float)
    set_weekly_total = QtCore.Signal(float)
    set_trt_output = QtCore.Signal(dict)
    set_trt_runtime = QtCore.Signal(str)
    set_start_date_rollers = QtCore.Signal(str)
    set_end_date_rollers = QtCore.Signal(str)
    set_in_clock = QtCore.Signal(tuple)
    set_out_clock = QtCore.Signal(tuple)
    set_main_clock = QtCore.Signal(float, float)
    set_user_start = QtCore.Signal(tuple)
    set_user_end = QtCore.Signal(tuple)
    set_button_state = QtCore.Signal(int)
    clock_button_press = QtCore.Signal(object)
    update_drop_downs = QtCore.Signal(object)
    clocked_in = QtCore.Signal(bool)


# -------------------------------------------------------------------------------------------------------------------
# Clocks Engine
# -------------------------------------------------------------------------------------------------------------------
# NOTE: The clock engines will continue to run the UI clocks.
class time_engine(QtCore.QThread):
    """
    This runs the clocks and continuous time calculations
    """
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.tick = None
        self.kill_it = False
        self.latest_timesheet = None
        self.today = datetime.now().date().strftime('%m-%d-%y')
        self.button_state = 0

        # Connect Signals
        self.time_signal = time_signals()
        self.time_machine = time_machine()
        self.time_queue = time_queue()

        # Signal Connections
        self.update_timesheet(self.latest_timesheet)
        self.time_machine.time_signal.get_timesheet.connect(self.update_timesheet)
        self.time_signal.clock_button_press.connect(self.big_button_pressed)
        self.time_machine.time_signal.update_drop_downs.connect(self.set_up_dropdowns)

        self.daily_total = tl_time.get_daily_total(user=user, lunch_id=lunch_task)
        self.weekly_total = tl_time.get_weekly_total(user=user, lunch_id=lunch_task)
        self.dropdowns = sg_data.get_all_project_dropdowns(user=user)
        self.clocked_in = tl_time.is_user_clocked_in(user=user)

    def update_timesheet(self, timesheet=None):
        print('Updating timesheet...')
        if not timesheet:
            self.latest_timesheet = tl_time.get_latest_timesheet(user=user)
            timesheet = self.latest_timesheet
        else:
            self.latest_timesheet = timesheet
        self.clocked_in = tl_time.is_user_clocked_in(user=user)
        self.time_signal.clocked_in.emit(self.clocked_in)
        self.time_signal.set_timesheet.emit(timesheet)

    def update_entity_dropdown(self):
        proj = self.project_dropdown.currentText()
        proj_id = self.project_dropdown.currentIndex()
        if proj_id and proj_id != 0 and proj != '':
            entities = list(self.dropdowns[proj].keys())
            self.entity_dropdown.clear()
            self.entity_dropdown.addItem('Select Entity', 0)
            if proj_id != 0:
                for entity in entities:
                    if entity != '__specs__':
                        self.entity_dropdown.addItem(entity, self.dropdowns[proj][entity]['__specs__']['id'])
            self.update_task_dropdown()

    def update_task_dropdown(self):
        proj = self.project_dropdown.currentText()
        ent = self.entity_dropdown.currentText()
        ent_id = self.entity_dropdown.currentIndex()
        self.task_dropdown.clear()
        self.task_dropdown.addItem('Select Task', 0)
        if ent_id != 0 and ent:
            tasks = list(self.dropdowns[proj][ent].keys())
            for task in tasks:
                if task != '__specs__':
                    self.task_dropdown.addItem(task, self.dropdowns[proj][ent]['__specs__']['id'])

    def set_up_dropdowns(self):
        # Set current project details:
        proj = self.latest_timesheet['project']['name']
        proj_id = self.latest_timesheet['project']['id']
        ent = self.latest_timesheet['entity.Task.entity']['name']
        ent_id = self.latest_timesheet['entity.Task.entity']['id']
        tsk = self.latest_timesheet['entity']['name']
        tsk_id = self.latest_timesheet['entity']['id']

        try:
            self.dropdowns = sg_data.get_all_project_dropdowns(user=user)
            projects = list(self.dropdowns.keys())
            entities = list(self.dropdowns[proj].keys())
            tasks = list(self.dropdowns[proj][ent].keys())

            self.project_dropdown.clear()
            self.entity_dropdown.clear()
            self.task_dropdown.clear()

            self.project_dropdown.addItem('Select Project', 0)
            for project in projects:
                self.project_dropdown.addItem(project, self.dropdowns[project]['__specs__']['id'])
            self.project_dropdown.setCurrentIndex(self.project_dropdown.findText(proj))

            self.entity_dropdown.addItem('Select Entity', 0)
            for entity in entities:
                if entity != '__specs__':
                    self.entity_dropdown.addItem(entity, self.dropdowns[proj][entity]['__specs__']['id'])
            self.entity_dropdown.setCurrentIndex(self.entity_dropdown.findText(ent))

            self.task_dropdown.addItem('Select Task', 0)
            for task in tasks:
                if task != '__specs__':
                    self.task_dropdown.addItem(task, self.dropdowns[proj][ent][task]['__specs__']['id'])
            self.task_dropdown.setCurrentIndex(self.task_dropdown.findText(tsk))

            self.project_dropdown.currentIndexChanged.connect(self.update_entity_dropdown)
            self.project_dropdown.currentIndexChanged.connect(self.button_status)
            self.entity_dropdown.currentIndexChanged.connect(self.update_task_dropdown)
            self.entity_dropdown.currentIndexChanged.connect(self.button_status)
            self.task_dropdown.currentIndexChanged.connect(self.button_status)
        except KeyError as e:
            logger.error('Failed to build menus... trying again...')
            logger.error(e)
            time.sleep(1)
            self.set_up_dropdowns()

    def big_button_pressed(self, button):
        prj = self.project_dropdown.currentText()
        prj_id = self.project_dropdown.itemData(self.project_dropdown.currentIndex())
        ent = self.entity_dropdown.currentText()
        ent_id = self.entity_dropdown.itemData(self.entity_dropdown.currentIndex())
        tsk = self.task_dropdown.currentText()
        tsk_id = self.task_dropdown.itemData(self.task_dropdown.currentIndex())
        ts_id = self.latest_timesheet['id']

        # TODO: Add the user start/end time feature to this
        start_time = datetime.now()
        end_time = datetime.now()

        data = {
            'context': {
                'Project': {
                    'name': prj,
                    'id': prj_id
                },
                'Entity': {
                    'name': ent,
                    'id': ent_id
                },
                'Task': {
                    'name': tsk,
                    'id': tsk_id
                }
            },
            'id': ts_id,
            'start_time': start_time,
            'end_time': end_time,
            'timesheet': self.latest_timesheet,
            'reason': None,
        }

        if self.button_state == 0:
            print('Clock in')
            data['type'] = 'clock_in'
            q.put(data)
            q.join()
        elif self.button_state == 1:
            print('Clock Out')
            data['type'] = 'clock_out'
            q.put(data)
            q.join()
        elif self.button_state == 2:
            data['type'] = 'switch'
            print('Switch Time')
            q.put(data)
            q.join()
        data['type'] = 'cleanup'
        q.put(data)
        q.join()

    def button_status(self):
        match = True
        self.clocked_in = tl_time.is_user_clocked_in(user=user)
        prj = self.latest_timesheet['project']['name']
        ent = self.latest_timesheet['entity.Task.entity']['name']
        tsk = self.latest_timesheet['entity']['name']
        try:
            if prj != self.project_dropdown.currentText():
                match = False
            if ent != self.entity_dropdown.currentText():
                match = False
            if tsk != self.task_dropdown.currentText():
                match = False
            if match and self.clocked_in:
                self.button_state = 1
            elif not match and self.clocked_in:
                self.button_state = 2
            elif not self.clocked_in:
                self.button_state = 0
            self.time_signal.set_button_state.emit(self.button_state)
        except AttributeError as e:
            logger.error('Button tried to call too early.  Passing')
            logger.error(e)
            print('Button tried to call too early.  Passing')
            print(e)

    def run(self):
        self.chronograph()

    def kill(self):
        self.kill_it = True
        if self.time_machine.isRunning():
            self.time_machine.kill()
            self.time_machine.quit()

        if self.time_queue.isRunning():
            self.time_queue.kill()
            self.time_queue.quit()

        if self.isRunning():
            self.quit()

    def chronograph(self):
        # Start the Time Machine
        print('time_engine > chronograph has started...')
        self.time_machine.start()
        self.time_queue.start()
        sub_timer = 0

        # Run the clock loop
        while not self.kill_it:
            # Setup a clock system: creates the time tick and then calculates the rotations
            # of the hands of the clocks
            self.tick = QtCore.QTime.currentTime()
            hour = (30.0 * (self.tick.hour() + (self.tick.minute() / 60.0)))
            minute = (6.0 * (self.tick.minute() + (self.tick.second() / 60.0)))
            # Make an alternate tuple for passing both at once where needed
            _time_ = (hour, minute)

            # Create the main clock hands and compute rotations
            self.time_signal.set_main_clock.emit(hour, minute)

            # Set the User Clock in time

            # Start a sub timer for heavier processes that don't need updates every second
            if (sub_timer % 60) == 0:
                sub_timer = 1
                # Collect the Daily Total digital and needle outputs
                self.daily_total = tl_time.get_daily_total(user=user, lunch_id=lunch_task['id'])
                self.weekly_total = tl_time.get_weekly_total(user=user, lunch_id=lunch_task['id'])
                self.time_signal.set_daily_total_needle.emit(self.daily_total)
                self.time_signal.set_weekly_total_needle.emit(self.weekly_total)
                self.time_signal.set_daily_total.emit(self.daily_total)
                self.time_signal.set_weekly_total.emit(self.weekly_total)
            else:
                sub_timer += 1

            # Set up the total running time calculations and outputs
            trt = tl_time.get_running_time(timesheet=self.latest_timesheet)
            self.time_signal.set_trt_output.emit(trt)
            self.time_signal.set_trt_runtime.emit(trt['rt'])

            # Set up the short date calculations for converting to the date rollers
            if 'sg_task_start' in self.latest_timesheet.keys() \
                    and hasattr(self.latest_timesheet['sg_task_start'], 'date'):
                timesheet_start_date = self.latest_timesheet['sg_task_start'].date()
                short_start_date = timesheet_start_date.strftime('%m-%d-%y')
            else:
                short_start_date = self.today
            if 'sg_task_end' in self.latest_timesheet.keys() and hasattr(self.latest_timesheet['sg_task_end'], 'date'):
                timesheet_end_date = self.latest_timesheet['sg_task_end'].date()
                short_end_date = timesheet_end_date.strftime('%m-%d-%y')
            else:
                short_end_date = self.today
            # Find the right conditions and set the date rollers
            if short_start_date != self.today:
                self.time_signal.set_start_date_rollers.emit(str(short_start_date))
            else:
                self.time_signal.set_start_date_rollers.emit(str(self.today))
            if short_end_date != self.today:
                self.time_signal.set_end_date_rollers.emit(str(short_end_date))
            else:
                self.time_signal.set_end_date_rollers.emit(str(str(self.today)))

            # Set the Start and End time Clocks
            if self.clocked_in:
                get_start_hour = self.latest_timesheet['sg_task_start'].time().hour
                end_hour = hour
                get_start_minute = self.latest_timesheet['sg_task_start'].time().minute
                start_second = self.latest_timesheet['sg_task_start'].time().second
                end_minute = minute
                start_hour = (30.0 * (get_start_hour + (get_start_minute / 60.0)))
                start_minute = (6.0 * (get_start_minute + (start_second / 60.0)))
            else:
                start_hour = hour
                start_minute = minute
                if self.latest_timesheet['sg_task_end']:
                    get_end_hour = self.latest_timesheet['sg_task_end'].time().hour
                    get_end_minute = self.latest_timesheet['sg_task_end'].time().minute
                    end_second = self.latest_timesheet['sg_task_end'].time().second
                    end_hour = (30.0 * (get_end_hour + (get_end_minute / 60.0)))
                    end_minute = (6.0 * (get_end_minute + (end_second / 60.0)))
                else:
                    end_hour = hour
                    end_minute = minute

            # Set the Start and End clocks
            start_time = (start_hour, start_minute)
            end_time = (end_hour, end_minute)
            self.time_signal.set_in_clock.emit(start_time)
            self.time_signal.set_out_clock.emit(end_time)

            # Update the Clock button to show either red, green or yellow.
            self.button_status()

            # Hold the clock for one second
            time.sleep(1)


# ------------------------------------------------------------------------------------------------------
# Primary Engine
# ------------------------------------------------------------------------------------------------------
# NOTE: time_machine will continue to run services, an/or be the outside event listener.
#       Or, it will be integrated into the clock? No. Probably not. I want time features to continue
class time_machine(QtCore.QThread):
    """
    The time_machine is the event listening engine that looks for new time sheets and updates the UI
    to match.  It will essentially check for new time sheets and emit that data to the appropriate routines
    for further processing.
    """
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        # Get the TLD Time Capsule File
        self.db_path = os.path.join(sys.path[0], 'data_io/time_capsule.tld')
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)

        # Setup The main variables
        self.kill_it = False

        # Setup the streams
        self.time_signal = time_signals()
        # self.set_timesheet = QtCore.Signal(object)
        logger.info('Time Machine Started')

    def run(self):
        self.listener()

    def kill(self):
        if self.isRunning():
            self.quit()
        self.kill_it = True

    def get_time_capsule(self):
        """
        This will open and collect the current time capsule file.
        :return:
        """
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as fh:
                db_file = json.load(fh)
            return db_file

    def save_time_capsule(self, data={}):
        """
        Saves the last EventLogEntry and TimeLog to the time_capsule, allowing for checks of existing timesheets
        and preventing the processing of events more than once.
        :param data: (dict): A collection of 2 values:
                   data =   {
                                'EventLogID': 123,
                                'TimeLogID': 456
                            }
        :return: None
        """
        if data:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'w') as fh:
                    data = json.dumps(data, indent=4)
                    fh.write(data)

    def get_new_events(self):
        """
        This method will collect the latest EventLogEntry from the Shotgun database.
        :return: A list of new events
        """
        # print 'Getting new events'
        next_event_id = None
        time_capsule = self.get_time_capsule()
        new_event_id = time_capsule['EventLogID']
        if new_event_id and (next_event_id is None or new_event_id < next_event_id):
            # print 'Setting next_event_id to %s' % new_event_id
            next_event_id = new_event_id

        if next_event_id:
            # print 'next_event_id: %s' % next_event_id
            filters = [
                ['id', 'greater_than', next_event_id - 1],
                {
                    'filter_operator': 'any',
                    'filters': [
                        ['event_type', 'is', 'Shotgun_TimeLog_New'],
                        ['event_type', 'is', 'Shotgun_TimeLog_Change']
                    ]
                }
            ]
            fields = [
                'id',
                'event_type',
                'attribute_name',
                'meta',
                'entity',
                'user',
                'project',
                'session_uuid',
                'created_at'
            ]
            order = [
                {
                    'column': 'id',
                    'direction': 'desc'
                }
            ]

            conn_attempts = 0
            while True:
                try:
                    events = sg.find('EventLogEntry', filters, fields, order=order, limit=100)
                    # print 'found events: %s' % events
                    if events:
                        logger.debug('Events collected! %s' % events)
                        # print 'New Events Collected!', events
                        return events
                except (sgapi.ProtocolError, sgapi.ResponseError, socket.error) as err:
                    logger.warning('Shotgun API Failure.  Trying again... %s' % err)
                    conn_attempts += 1
                    time.sleep(5)
                    if conn_attempts > 10:
                        logger.error('Can\'t connect to shotgun!', err)
                        break
                except Exception as err:
                    logger.debug('Unknown exception!  Trying again. %s' % err)
                    conn_attempts += 1
                    time.sleep(5)
                    if conn_attempts > 10:
                        logger.error('Something went wrong! %s' % err)
                        error = '%s:\n%s | %s\n%s | %s' % (err, inspect.stack()[0][2], inspect.stack()[0][3],
                                                           inspect.stack()[1][2], inspect.stack()[1][3])
                        comm.send_error_alert(user=user, error=error)
                        break
        return []

    def listener(self):
        """
        The main listener loop.  Checks for new time sheets and updates the other services.
        :return:
        """
        print('Time_machine > listener() has started...')
        while not self.kill_it:
            # Collect the events
            events = self.get_new_events()
            if events:
                for event in events:
                    time_capsule = self.get_time_capsule()
                    event_id = time_capsule['EventLogID']
                    timelog_id = time_capsule['TimeLogID']
                    current = time_capsule['current']

                    if not event['entity']:
                        continue
                    if event['entity']['id'] >= time_capsule['TimeLogID'] and event['id'] > time_capsule['EventLogID']:
                        entity = event['entity']
                        if entity:
                            entity_id = entity['id']
                            timesheet_info = tl_time.get_timesheet_by_id(tid=entity_id)
                        else:
                            continue
                        if timesheet_info:
                            user_info = timesheet_info['user']
                            user_id = user_info['id']
                            if user_id == user['id']:
                                if timesheet_info['sg_task_end'] and time_capsule['current'] and \
                                        event['entity']['id'] == time_capsule['TimeLogID']:
                                    # At this point, there is a timestamp in the out time, and the time capsule reads it
                                    # as the latest (current) timesheet, and both the event ID and the capsule id match

                                    # Collect the entity
                                    ts_entity = timesheet_info['entity.Task.entity']

                                    self.time_signal.get_timesheet.emit(timesheet_info)
                                    self.time_signal.update_drop_downs.emit('Do it')
                                    print('get_timesheet emits: %s' % timesheet_info)
                                    event_id = event['id']
                                    timelog_id = event['entity']['id']
                                    current = False

                                elif not timesheet_info['sg_task_end'] and not time_capsule['current'] or \
                                        event['entity']['id'] > time_capsule['TimeLogID']:
                                    # Now, the timesheet has an opened end time (still clocked in) and the capsule
                                    # is not listed as the current one, suggesting a new timesheet OR
                                    # the event ID is higher that the one in the capsule.

                                    # Collect the entity
                                    ts_entity = timesheet_info['entity.Task.entity']
                                    logger.debug('NEW RECORD! %s' % event['id'])
                                    print('TS INFO', timesheet_info)
                                    self.time_signal.get_timesheet.emit(timesheet_info)
                                    print('ts_data emitted.')
                                    event_id = event['id']
                                    timelog_id = event['entity']['id']
                                    current = True
                                else:
                                    logger.debug('Event Skipped')
                                    event_id = event['id']
                                    timelog_id = timesheet_info['id']
                                    current = time_capsule['current']
                        elif event['entity']['id'] != time_capsule['TimeLogID'] \
                                and event['id'] > time_capsule['EventLogID']:
                            event_id = event['id']
                            timelog_id = time_capsule['TimeLogID']
                            current = time_capsule['current']

                    data = {
                        'EventLogID': event_id,
                        'TimeLogID': timelog_id,
                        'current': current
                    }
                    try:
                        self.save_time_capsule(data)
                        logger.debug('Time Capsule saved!')
                    except IOError as e:
                        logger.warning('Failed to save the file.  Trying again in a few '
                                       'seconds... %s' % e)
                        print('IOError... failed.  Trying again...: %s' % e)
                        time.sleep(0.35)
                        self.save_time_capsule(data)
                        # continue

            time.sleep(1)


# ------------------------------------------------------------------------------------------------------
# Primary Tools
# ------------------------------------------------------------------------------------------------------
# NOTE: time_queue currently does most of the processing
class time_queue(QtCore.QThread):
    """
    The Time Lord is the main functional tool kit for the UI
    """
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.kill_it = False

    def run(self):
        self.run_queue()

    def run_queue(self):
        while not self.kill_it:
            package = q.get(block=True)
            print('package:')
            print(package)
            type = package['type']
            context = package['context']
            ts_id = package['id']
            start_time = package['start_time']
            end_time = package['end_time']
            timesheet = package['timesheet']

            new_timesheet = None
            old_timesheeet = None
            cleanup = None
            consistency = None
            update = None

            if type == 'clock_in':
                new_timesheet = tl_time.create_new_timesheet(user=user, context=context, start_time=start_time,
                                                             entry='Time Lord UI')
            elif type == 'clock_out':
                old_timesheeet = tl_time.clock_out_time_sheet(timesheet=timesheet, clock_out=end_time)
            elif type == 'switch':
                old_timesheeet = tl_time.clock_out_time_sheet(timesheet=timesheet, clock_out=end_time)
                new_timesheet = tl_time.create_new_timesheet(user=user, context=context, start_time=start_time,
                                                             entry='Time Lord UI')
            elif type == 'cleanup':
                cleanup = tl_time.timesheet_cleanup(user=user)
                consistency = tl_time.timesheet_consistency_cleanup(user=user)
            elif type == 'update':
                update = tl_time.update_current_times(user=user, tid=ts_id, start_time=start_time, end_time=end_time,
                                                      proj_id=context['Project']['id'], task_id=context['Task']['id'],
                                                      reason=context['reason'])

            q.task_done()
            print('old: %s' % old_timesheeet)
            print('new: %s' % new_timesheet)
            print('cleanup: %s' % cleanup)
            print('update: %s' % update)
            print('consistency: %s' % consistency)

    def kill(self):
        self.kill_it = True


# ------------------------------------------------------------------------------------------------------
# User Interface
# ------------------------------------------------------------------------------------------------------
# NOTE: time_lord_ui needs to only be display and buttons. NO PROCESSES!!!
class time_lord_ui(QtWidgets.QMainWindow):
    """
    The main Time Lord UI.
    """
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # Scope variables
        self.user_start = None
        self.user_end = None
        self.clocked_in = False
        self.latest_timesheet = None

        # --------------------------------------------------------------------------------------------------------
        # Set the saved settings
        # --------------------------------------------------------------------------------------------------------
        # This saves all the last settings so that they return to their previous state when the program is run again.
        self.settings = QtCore.QSettings(__author__, 'TimeLord')
        self.saved_project = self.settings.value('project', '.')
        self.saved_project_id = self.settings.value('project_id', '.')
        self.saved_entity = self.settings.value('entity', '.')
        self.saved_entity_id = self.settings.value('entity_id', '.')
        self.saved_task = self.settings.value('task', '.')
        self.saved_task_id = self.settings.value('task_id', '.')
        self.saved_window_position = self.settings.value('geometry')
        self.restoreGeometry(self.saved_window_position)

        # Connect to threads
        self.time_queue = time_queue()
        self.time_engine = time_engine()

        # --------------------------------------------------------------------------------------------------------
        # Setup UI
        # --------------------------------------------------------------------------------------------------------
        self.ui = tlu.Ui_TimeLord()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
        self.setWindowTitle("Time Lord v%s" % __version__)
        self.window_on_top_tested = False
        # self.set_window_on_top()

        # Setup UI editor threads
        # Timesheet Elements
        self.time_engine.project_dropdown = self.ui.project_dropdown
        self.time_engine.entity_dropdown = self.ui.entity_dropdown
        self.time_engine.task_dropdown = self.ui.task_dropdown
        self.time_engine.set_up_dropdowns()
        # self.time_engine.button_status()
        # Clock Elements
        self.time_engine.time_hour = self.ui.time_hour
        self.time_engine.time_minute = self.ui.time_minute
        self.time_engine.day_meter = self.ui.day_meter
        self.time_engine.week_meter = self.ui.week_meter
        # Start/End Time Elements
        self.time_engine.start_clock_hour = self.ui.start_clock_hour
        self.time_engine.start_clock_minute = self.ui.start_clock_minute
        self.time_engine.end_clock_hour = self.ui.end_clock_hour
        self.time_engine.end_clock_minute = self.ui.end_clock_minute

        # Signal Connections
        self.time_engine.time_signal.set_daily_total_needle.connect(self.set_daily_total_needle)
        self.time_engine.time_signal.set_weekly_total_needle.connect(self.set_weekly_total_needle)
        self.time_engine.time_signal.set_daily_total.connect(self.daily_output)
        self.time_engine.time_signal.set_weekly_total.connect(self.weekly_output)
        self.time_engine.time_signal.set_trt_output.connect(self.trt_output)
        self.time_engine.time_signal.set_trt_runtime.connect(self.set_runtime_clock)
        self.time_engine.time_signal.set_start_date_rollers.connect(self.set_start_date_rollers)
        self.time_engine.time_signal.set_end_date_rollers.connect(self.set_end_date_rollers)
        self.time_engine.time_signal.set_main_clock.connect(self.set_main_clock)
        self.time_engine.time_signal.set_in_clock.connect(self.set_in_clock)
        self.time_engine.time_signal.set_out_clock.connect(self.set_out_clock)
        self.time_engine.time_signal.set_user_start.connect(self.update_user_start)
        self.time_engine.time_signal.set_timesheet.connect(self.update_timesheet)
        self.time_engine.time_signal.clocked_in.connect(self.update_clocked_in)
        self.time_engine.time_signal.set_button_state.connect(self.update_button_state)

        # UI Connections
        self.ui.clock_button.clicked.connect(self.big_clock_button)
        self.ui.start_date_button.clicked.connect(self.get_user_start_time)
        self.ui.end_date_button.clicked.connect(self.get_user_end_time)
        self.ui.clock_button.hide()
        self.ui.red_light.hide()

        # Set main user info
        self.ui.artist_label.setText(user['name'])

        # Start your engines
        # self.time_queue.start()
        self.time_engine.start()

    def update_clocked_in(self, clocked_in):
        self.clocked_in = clocked_in

    def update_timesheet(self, timesheet=None):
        if timesheet:
            self.latest_timesheet = timesheet
            self.saved_project = self.latest_timesheet['project']['name']
            self.saved_project_id = self.latest_timesheet['project']['id']
            self.saved_entity = self.latest_timesheet['entity.Task.entity']['name']
            self.saved_entity_id = self.latest_timesheet['entity.Task.entity']['id']
            self.saved_task = self.latest_timesheet['entity']['name']
            self.saved_task_id = self.latest_timesheet['entity']['id']
        else:
            self.latest_timesheet = tl_time.get_latest_timesheet(user=user)

    def update_button_state(self, state=0):
        # A value of None for message means that there is not clock-out time and the sheet is still active.
        self.ui.clock_button.setStyleSheet('background-image: url(:/lights buttons/elements/'
                                           'clock_button_%i.png);'
                                           'background-repeat: none;'
                                           'background-color: rgba(0, 0, 0, 0);'
                                           'border-color: rgba(0, 0, 0, 0);' % state)
        self.ui.clock_button.show()

    def daily_output(self, message=None):
        total = 'Daily Total: %0.2f' % message
        self.ui.output_daily.setPlainText(str(total))

    def weekly_output(self, message=None):
        total = 'Weekly Total: %0.2f' % message
        self.ui.output_weekly.setPlainText(str(total))

    def set_daily_total_needle(self, total):
        '''
        Set this to adjust the needs and the output monitor values simultaneously.
        :param total: A total value of the daily total hours minus lunch and breaks
        :return:
        '''
        if total:
            # self.daily_output(total)
            # Adjust the total down by a value known from the graphics?
            total -= 4.0
            angle = ((total / (float(config['ot_hours']) * 2.0)) * 100.00) - 25.00  # I know my graphic spans 100 dgrs.

            if angle < -50.0:
                angle = -50.0
            elif angle > 50.0:
                angle = 50.0
            meter_needle = QtGui.QPixmap(":/dial hands/elements/meter_1_needle.png")
            needle_rot = QtGui.QTransform()

            needle_rot.rotate(angle)
            meter_needle_rot = meter_needle.transformed(needle_rot)

            self.ui.day_meter.setPixmap(meter_needle_rot)
            self.ui.day_meter.update()

    def set_weekly_total_needle(self, total):
        if total:
            # self.weekly_output(total)
            angle = ((100 / (float(config['ot_hours']) * 10.0)) * total) - 50
            if angle < -50.0:
                angle = -50.0
            elif angle > 50.0:
                angle = 50.0
            meter_needle = QtGui.QPixmap(":/dial hands/elements/meter_1_needle.png")
            needle_rot = QtGui.QTransform()

            needle_rot.rotate(angle)
            meter_needle_rot = meter_needle.transformed(needle_rot)

            self.ui.week_meter.setPixmap(meter_needle_rot)
            self.ui.week_meter.update()

    def trt_output(self, message=None):
        if message:
            trt = 'TRT: %s:%s:%s' % (message['h'], message['m'], message['s'])
        else:
            trt = 'TRT: 00:00:00'
        self.ui.output_trt.setPlainText(trt)

    def set_runtime_clock(self, t='000000'):
        """
        Sets the running time clock.
        :param t: (str) - While this is a number value, it must be exactly 6 digits long, thus string to maintain
                            the number of zeros needed for the default.
        :return: Running time.
        """
        if len(t) == 6:
            self.ui.run_hour_ten.setStyleSheet('background-image: url(:/vaccuum_tube_numbers/elements/vt_%s.png);'
                                               'background-repeat: none;background-color: rgba(0, 0, 0, 0);' % t[0])
            self.ui.run_hour_one.setStyleSheet('background-image: url(:/vaccuum_tube_numbers/elements/vt_%s.png);'
                                               'background-repeat: none;background-color: rgba(0, 0, 0, 0);' % t[1])
            self.ui.run_minute_ten.setStyleSheet('background-image: url(:/vaccuum_tube_numbers/elements/vt_%s.png);'
                                                 'background-repeat: none;background-color: rgba(0, 0, 0, 0);' % t[2])
            self.ui.run_minute_one.setStyleSheet('background-image: url(:/vaccuum_tube_numbers/elements/vt_%s.png);'
                                                 'background-repeat: none;background-color: rgba(0, 0, 0, 0);' % t[3])
            self.ui.run_second_ten.setStyleSheet('background-image: url(:/vaccuum_tube_numbers/elements/vt_%s.png);'
                                                 'background-repeat: none;background-color: rgba(0, 0, 0, 0);' % t[4])
            self.ui.run_second_one.setStyleSheet('background-image: url(:/vaccuum_tube_numbers/elements/vt_%s.png);'
                                                 'background-repeat: none;background-color: rgba(0, 0, 0, 0);' % t[5])

    def set_start_date_rollers(self, d='00-00-00'):
        """
        Sets the date rollers.
        :param d: (str) A MM-DD-YY date format string.
        :param which: (str) One of two acceptable values: 'start', 'end'
        :return:
        """
        # set the start date roller
        if d and d != '00-00-00':

            split_date = d.split('-')
            m = split_date[0]
            d = split_date[1]
            y = split_date[2]

            m_tens = int(m[0])
            m_ones = int(m[1])
            d_tens = int(d[0])
            d_ones = int(d[1])
            y_tens = int(y[0])
            y_ones = int(y[1])

            self.ui.start_tens_month.setStyleSheet('background-image: url(:/roller_numbers/elements/'
                                                   'start_m_tens_%s.png);' % m_tens)
            self.ui.start_ones_month.setStyleSheet('background-image: url(:/roller_numbers/elements/'
                                                   'start_m_ones_%s.png);' % m_ones)
            self.ui.start_tens_day.setStyleSheet('background-image: url(:/roller_numbers/elements/'
                                                 'start_d_tens_%s.png);' % d_tens)
            self.ui.start_ones_day.setStyleSheet('background-image: url(:/roller_numbers/elements/'
                                                 'start_d_ones_%s.png);' % d_ones)
            self.ui.start_tens_year.setStyleSheet('background-image: url(:/roller_numbers/elements/'
                                                  'start_y_tens_%s.png);' % y_tens)
            self.ui.start_ones_year.setStyleSheet('background-image: url(:/roller_numbers/elements/'
                                                  'start_y_ones_%s.png);' % y_ones)

    def set_end_date_rollers(self, d='00-00-00'):
        """
        Sets the date rollers.
        :param d: (str) A MM-DD-YY date format string.
        :return:
        """
        # set the end date roller
        if d and d != '00-00-00':

            split_date = d.split('-')
            m = split_date[0]
            d = split_date[1]
            y = split_date[2]

            m_tens = int(m[0])
            m_ones = int(m[1])
            d_tens = int(d[0])
            d_ones = int(d[1])
            y_tens = int(y[0])
            y_ones = int(y[1])

            self.ui.end_tens_month.setStyleSheet('background-image: url(:/roller_numbers/elements/'
                                                 'end_m_tens_%s.png);' % m_tens)
            self.ui.end_ones_month.setStyleSheet('background-image: url(:/roller_numbers/elements/'
                                                 'end_m_ones_%s.png);' % m_ones)
            self.ui.end_tens_day.setStyleSheet('background-image: url(:/roller_numbers/elements/'
                                               'end_d_tens_%s.png);' % d_tens)
            self.ui.end_ones_day.setStyleSheet('background-image: url(:/roller_numbers/elements/'
                                               'end_d_ones_%s.png);' % d_ones)
            self.ui.end_tens_year.setStyleSheet('background-image: url(:/roller_numbers/elements/'
                                                'end_y_tens_%s.png);' % y_tens)
            self.ui.end_ones_year.setStyleSheet('background-image: url(:/roller_numbers/elements/'
                                                'end_y_ones_%s.png);' % y_ones)

    def set_main_clock(self, hour, minute):
        # Create the main clock hands and compute rotations
        hour_rot = QtGui.QTransform()
        minute_rot = QtGui.QTransform()
        hour_rot.rotate(hour)
        minute_rot.rotate(minute)

        # Rotate the main clock images
        hour_hand = QtGui.QPixmap(":/dial hands/elements/clock_1_hour.png")
        minute_hand = QtGui.QPixmap(":/dial hands/elements/clock_1_minute.png")
        hour_hand_rot = hour_hand.transformed(hour_rot)
        minute_hand_rot = minute_hand.transformed(minute_rot)

        # Set the main clock time
        self.ui.time_hour.setPixmap(hour_hand_rot)
        self.ui.time_minute.setPixmap(minute_hand_rot)
        self.ui.time_hour.update()
        self.ui.time_minute.update()

    def set_in_clock(self, in_time):
        """
        This will check if the user is clocked in or not, and then set the clock accordingly.
        If they are clocked in, display clock in time.  Otherwise, display current time.
        Where it gets tricky is introducing a user set time.  i.e. user changes the time.
        TODO: Figure out the user set time interruption.
        :param in_time: (tuple) (hour, minute)
        :return:
        """
        if self.clocked_in:
            if self.user_start:
                start_time = self.user_start
            else:
                start_time = self.latest_timesheet['sg_task_start']
            if start_time:
                hour = start_time.time().hour
                minute = start_time.time().minute
                second = start_time.time().second
                hours = (30 * (hour + (minute / 60.0)))
                minutes = (6 * (minute + (second / 60.0)))
            else:
                logger.warning('Bad Start Time!  Returning False')
                return False
        else:
            hours = in_time[0]
            minutes = in_time[1]

        hour_rot = QtGui.QTransform()
        minute_rot = QtGui.QTransform()
        hour_rot.rotate(hours)
        minute_rot.rotate(minutes)

        hour_hand = QtGui.QPixmap(":/dial hands/elements/clock_2_hour.png")
        minute_hand = QtGui.QPixmap(":/dial hands/elements/clock_2_minute.png")
        hour_hand_rot = hour_hand.transformed(hour_rot)
        minute_hand_rot = minute_hand.transformed(minute_rot)

        self.ui.start_clock_hour.setPixmap(hour_hand_rot)
        self.ui.start_clock_minute.setPixmap(minute_hand_rot)
        self.ui.start_clock_hour.update()
        self.ui.start_clock_minute.update()

    def set_out_clock(self, in_time):
        """
        This will check if the user is clocked in or not, and then set the clock accordingly.
        If they are clocked in, display clock in time.  Otherwise, display current time.
        Where it gets tricky is introducing a user set time.  i.e. user changes the time.
        TODO: Figure out the user set time interruption.
        :param in_time: (tuple) (hour, minute)
        :return:
        """
        if not self.clocked_in:
            if not self.latest_timesheet:
                self.latest_timesheet = tl_time.get_latest_timesheet(user=user)
                # self.timesheet_update.time_signal.ui_update.emit('Update!')
                # self.time_queue.time_signal.ui_update.emit()
            try:
                if self.user_end:
                    end_time = self.user_end
                else:
                    end_time = self.latest_timesheet['sg_task_end']
                if end_time:
                    logger.debug('end_time: %s' % end_time)
                    hour = end_time.time().hour
                    minute = end_time.time().minute
                    second = end_time.time().second
                    hours = (30 * (hour + (minute / 60.0)))
                    minutes = (6 * (minute + (second / 60.0)))
                else:
                    end_time = datetime.now().time()
                    logger.debug('The Proper end time was not sent. Using current time.')
                    hour = end_time.hour
                    minute = end_time.minute
                    second = end_time.second
                    hours = (30 * (hour + (minute / 60.0)))
                    minutes = (6 * (minute + (second / 60.0)))
            except Exception as e:
                logger.error('The fit hit the shan: %s' % e)
                error = '%s:\n%s | %s\n%s | %s' % (e, inspect.stack()[0][2], inspect.stack()[0][3],
                                                   inspect.stack()[1][2], inspect.stack()[1][3])
                comm.send_error_alert(user=user, error=error)
                return False
        else:
            hours = in_time[0]
            minutes = in_time[1]

        hour_rot = QtGui.QTransform()
        minute_rot = QtGui.QTransform()
        hour_rot.rotate(hours)
        minute_rot.rotate(minutes)

        hour_hand = QtGui.QPixmap(":/dial hands/elements/clock_3_hour.png")
        minute_hand = QtGui.QPixmap(":/dial hands/elements/clock_3_minute.png")
        hour_hand_rot = hour_hand.transformed(hour_rot)
        minute_hand_rot = minute_hand.transformed(minute_rot)

        self.ui.end_clock_hour.setPixmap(hour_hand_rot)
        self.ui.end_clock_minute.setPixmap(minute_hand_rot)
        self.ui.end_clock_hour.update()
        self.ui.end_clock_minute.update()

    def update_user_start(self, user_start=None):
        self.user_start = user_start

    def big_clock_button(self):
        self.ui.clock_button.hide()
        self.time_engine.time_signal.clock_button_press.emit(('Hello', 'There'))

    def get_user_start_time(self, user_start=None):
        """
        Eventually, this should return a user set start time from the UI.  Not sure right off hand yet how to do that.
        :return:
        """
        # if user_start:
        #     self.user_start = user_start
        if self.clocked_in:
            start_time = self.latest_timesheet['sg_task_start']
        else:
            start_time = datetime.now()
        t, ok = DateDialog.getDateTime(_time=start_time.time())
        print('get_user_start_time: ok: %s' % ok)
        if ok:
            print('ok: %s' % ok)
            self.user_start = parser.parse(
                '%s %s:%s:%s' % (datetime.now().date(), t.hour(), t.minute(), t.second()))
            logger.debug('Setting the user start: %s' % self.user_start)
            self.time_engine.user_start = self.user_start

            self.clocked_in = tl_time.is_user_clocked_in(user=user)
            if self.clocked_in:
                update_question = QtWidgets.QMessageBox(self)
                update_question.setWindowTitle('Update Start Time?')
                update_question.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
                update_question.setStyleSheet("background-color: rgb(100, 100, 100);\n"
                                              "color: rgb(230, 230, 230);")
                update_question.setText('Are you sure you want to update the current start time?')
                update_question.addButton('Yes! Update', QtWidgets.QMessageBox.AcceptRole)
                update_question.addButton('No!', QtWidgets.QMessageBox.RejectRole)
                ask = update_question.exec_()

                if ask == QtWidgets.QMessageBox.AcceptRole:
                    print(self.latest_timesheet)
                    logger.debug('Send the Timesheet update signal')
                    data = {
                        'context': {
                            'Project': {
                                'name': self.ui.project_dropdown.currentText(),
                                'id': self.ui.project_dropdown.findData(self.ui.project_dropdown.currentIndex())
                            },
                            'Entity': {
                                'name': self.ui.entity_dropdown.currentText(),
                                'id': self.ui.entity_dropdown.findData(self.ui.entity_dropdown.currentIndex())
                            },
                            'Task': {
                                'name': self.ui.task_dropdown.currentText(),
                                'id': self.ui.task_dropdown.findData(self.ui.task_dropdown.currentIndex())
                            }
                        },
                        'id': self.latest_timesheet['id'],
                        'start_time': self.user_start,
                        'end_time': self.user_end,
                        'timesheet': self.latest_timesheet,
                        'type': 'update',
                        'reason': 'Changed start time from the UI'
                    }
                    q.put(data)
                    q.join()

                self.user_start = None
                self.time_engine.user_start = None

    def get_user_end_time(self):
        """
        Eventually, this should return a user set end time from the UI.  Same as above
        :return:
        """
        t, ok = DateDialog.getDateTime()
        print('get_user_end_time: ok: %s' % ok)
        if ok:
            print('ok: %s' % ok)
            self.user_end = parser.parse('%s %s:%s:%s' % (datetime.now().date(), t.hour(), t.minute(), t.second()))
            logger.debug('Setting the user end: %s' % self.user_end)
            self.time_engine.user_end = self.user_end

            self.clocked_in = tl_time.is_user_clocked_in(user=user)
            if self.clocked_in:
                print('clocked in')
                update_question = QtWidgets.QMessageBox(self)
                update_question.setWindowTitle('Clock Out At Specific Time?')
                update_question.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
                update_question.setStyleSheet("background-color: rgb(100, 100, 100);\n"
                                              "color: rgb(230, 230, 230);")
                update_question.setText('Setting an Out Time while clocked in will clock you out.\n'
                                        'Go ahead and clock out?')
                update_question.addButton('Yes! Clock Out', QtWidgets.QMessageBox.AcceptRole)
                update_question.addButton('No!', QtWidgets.QMessageBox.RejectRole)
                ask = update_question.exec_()

                if ask == QtWidgets.QMessageBox.AcceptRole:
                    logger.debug('Send the Timesheet update signal')
                    data = {
                        'context': {
                            'Project': {
                                'name': self.ui.project_dropdown.currentText(),
                                'id': self.ui.project_dropdown.findData(self.ui.project_dropdown.currentIndex())
                            },
                            'Entity': {
                                'name': self.ui.entity_dropdown.currentText(),
                                'id': self.ui.entity_dropdown.findData(self.ui.entity_dropdown.currentIndex())
                            },
                            'Task': {
                                'name': self.ui.task_dropdown.currentText(),
                                'id': self.ui.task_dropdown.findData(self.ui.task_dropdown.currentIndex())
                            }
                        },
                        'id': self.latest_timesheet['id'],
                        'start_time': self.latest_timesheet['sg_task_start'],
                        'end_time': self.user_end,
                        'timesheet': self.latest_timesheet,
                        'type': 'clock_out',
                        'reason': None
                    }
                    q.put(data)
                    q.join()

                self.user_start = None
                self.time_engine.user_start = None

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.update_saved_settings()
        if self.time_engine.isRunning():
            self.time_engine.kill()
            self.time_engine.quit()

    def update_saved_settings(self):
        """
        The settings that are saved after the window is closed.
        :return:
        """
        self.settings.setValue('project', self.ui.project_dropdown.currentText())
        self.settings.setValue('project_id', self.ui.project_dropdown.itemData(self.ui.project_dropdown.currentIndex()))
        self.settings.setValue('entity', self.ui.entity_dropdown.currentText())
        self.settings.setValue('entity_id', self.ui.entity_dropdown.itemData(self.ui.entity_dropdown.currentIndex()))
        self.settings.setValue('task', self.ui.task_dropdown.currentText())
        self.settings.setValue('task_id', self.ui.task_dropdown.itemData(self.ui.task_dropdown.currentIndex()))
        self.settings.setValue('geometry', self.saveGeometry())
        self.saved_project = self.ui.project_dropdown.currentText()
        self.saved_project_id = self.ui.project_dropdown.itemData(self.ui.project_dropdown.currentIndex())
        self.saved_entity = self.ui.entity_dropdown.currentText()
        self.saved_entity_id = self.ui.entity_dropdown.itemData(self.ui.entity_dropdown.currentIndex())
        self.saved_task = self.ui.task_dropdown.currentText()
        self.saved_task_id = self.ui.task_dropdown.itemData(self.ui.task_dropdown.currentIndex())


class DateDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, _time=None):
        super(DateDialog, self).__init__(parent)

        if not _time:
            _time = datetime.now()

        layout = QtWidgets.QVBoxLayout(self)

        # nice widget for editing the time
        self.set_time = QtWidgets.QTimeEdit(self)
        if type(_time) == datetime:
            convert_time = _time.strftime('%h:%m:%S')
            _time = QtCore.QTime.fromString(convert_time)
        self.set_time.setTime(_time)
        layout.addWidget(self.set_time)

        self.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")

        self.setWindowTitle('DateTime Lord')
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

        # OK and Cancel buttons
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # get current date and time from the dialog
    def dateTime(self):
        return self.set_time.time()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getDateTime(parent=None, _time=None):
        dialog = DateDialog(parent, _time=_time)
        result = dialog.exec_()
        sTime = dialog.set_time
        return sTime.time(), result == QtWidgets.QDialog.Accepted


if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    # app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app.setOrganizationName('AdamBenson')
    app.setOrganizationDomain('adamdbenson.com')
    app.setApplicationName('TimeLord')
    splash_pix = QtGui.QPixmap('ui/resources/Time_Lord_Logo.png')
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    window = time_lord_ui()
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())
