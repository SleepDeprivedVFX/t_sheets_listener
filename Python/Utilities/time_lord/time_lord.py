"""
This is a partial start-over for the time_lord.  I feel like the original system may have inadvertently become too
cumbersome to make work, and was ending up being one patch after another, not really solving any of the problems, but
covering them up with ever more inhibiting drives to collect data.

SYSTEM NEEDS:
1. Needs a time system that runs the clocks
    a. Main clocks and start and end clocks should always keep running
    b. TRT (Total Running Time) clocks should be able to get new data from the most recent time-sheets, but keep running
2. Needs a time-based triggering system for updating data from outside of the application
    a. Get and implement changes to Daily/Weekly totals.
    b. Drag-n-Drop publishes or manual time changes.
3. Needs a broader tool kit for processing changes that doesn't lock up the clocks or user interface.
4. A signal system with clear ins and outs for all the main points of data, and it needs a unified point of data for
    all features.  No doubling up or redundant tasks.
5. Needs a global logger stream to handle logs across all tools!

WISH LIST:
1. Shotgun Listening system.
    a. Listens for Shotgun_TimeLog_New or Shotgun_TimeLog_Change events.
        This would remove the need for most of the data calls, as the data calls would be triggered by the events.
        One problem that may arise is that our own events will trigger the changes, thus:
            i. I collect the new UI created timesheet ID immediately, and if the emitted signal contains that ID, it is
                ignored
            ii. A timer might get introduced to minimize the number of calls; only 1 call allowed in a 2 second period.
                Because some of the routines create multiple entries in quick succession, and I wouldn't want to process
                multiple hits within a few microseconds.
"""
# FIXME: I may have to upgrade this system to PySide2 to solve some of the screen scaling issues.  Probably for
#       the best, but still a major pain in the ass.  Consider it sooner than later.

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.4.6'

import shotgun_api3 as sgapi
import os
import sys
from PySide import QtGui, QtCore
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import cPickle as pickle

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


# -------------------------------------------------------------------------------------------------------------------
# Stream Handler
# -------------------------------------------------------------------------------------------------------------------
class time_stream(logging.StreamHandler):
    """
    Stream handler for the output window
    """
    def emit(self, record):
        level = record.levelname
        message = record.message
        # Colorize the Monitor Log Output. (Error messages, Debug logging, and Warnings)
        info = QtGui.QColor(130, 231, 130)
        error = QtGui.QColor(255, 0, 0)
        debug = QtGui.QColor(113, 113, 0)
        warning = QtGui.QColor(218, 145, 0)
        formatter = QtGui.QTextCharFormat()
        if level == 'ERROR':
            print('::ERROR: %s' % message)
            formatter.setForeground(error)
        elif level == 'DEBUG':
            print('::DEBUG: %s' % message)
            formatter.setForeground(debug)
        elif level == 'WARNING':
            print('::WARN: %s' % message)
            formatter.setForeground(warning)
        else:
            print('::INFO: %s' % message)
            formatter.setForeground(info)
        self.edit.setCurrentCharFormat(formatter)

        # Set the cursor to the top
        cursor = QtGui.QTextCursor(self.edit.document())
        cursor.setPosition(0)
        self.edit.setTextCursor(cursor)
        # #
        # # # Insert Log
        # print('Log Message: %s' % message)
        self.edit.insertPlainText('%s\n' % message)
        current_text = self.edit.toPlainText()
        if len(current_text) > 300:
            self.edit.clear()
        # self.edit.appendPlainText('%s\n' % message)
        del info
        del error
        del debug
        del warning
        del formatter
        # del cursor


# ------------------------------------------------------------------------------------------------------
# Signal Emitters
# ------------------------------------------------------------------------------------------------------
class time_signals(QtCore.QObject):
    # Logger Signals
    log = QtCore.Signal(str)
    error = QtCore.Signal(str)
    debug = QtCore.Signal(str)
    warning = QtCore.Signal(str)
    # End Thread Signals
    kill_signal = QtCore.Signal(bool)
    auto_close = QtCore.Signal(bool)

    # Time Signals / Clock Faces
    main_clock = QtCore.Signal(tuple)
    in_clock = QtCore.Signal(tuple)
    out_clock = QtCore.Signal(tuple)
    in_date = QtCore.Signal(str)
    out_date = QtCore.Signal(str)
    running_clock = QtCore.Signal(str)
    get_running_clock = QtCore.Signal(dict)

    # Monitor Output Signals
    trt_output = QtCore.Signal(str)
    req_start_end_output = QtCore.Signal(str)
    start_end_output = QtCore.Signal(str)
    user_output = QtCore.Signal(str)
    daily_output = QtCore.Signal(str)
    weekly_output = QtCore.Signal(str)
    lower_output = QtCore.Signal(str)

    # State Signals
    error_state = QtCore.Signal(bool)
    steady_state = QtCore.Signal(bool)
    clock_state = QtCore.Signal(int)
    button_state = QtCore.Signal(str)

    # Calculation Signals
    daily_total = QtCore.Signal(float)
    weekly_total = QtCore.Signal(float)
    req_daily_total = QtCore.Signal(str)
    set_daily_total = QtCore.Signal(float)
    req_weekly_total = QtCore.Signal(str)
    set_weekly_total = QtCore.Signal(float)

    # Update Signals
    update = QtCore.Signal(dict)
    update_ui = QtCore.Signal(dict)
    req_project_update = QtCore.Signal(str)
    req_entity_update = QtCore.Signal(int)
    req_task_update = QtCore.Signal(dict)
    send_project_update = QtCore.Signal(dict)
    send_entity_update = QtCore.Signal(dict)
    send_task_update = QtCore.Signal(dict)
    set_dropdown = QtCore.Signal(dict)
    self_destruct = QtCore.Signal(str)

    # Data Signals
    latest_timesheet = QtCore.Signal(dict)
    user_clocked_in = QtCore.Signal(bool)
    send_timesheet = QtCore.Signal(dict)

    # Timesheet Action Signals
    clock_out_user = QtCore.Signal(dict)
    clock_in_user = QtCore.Signal(tuple)
    user_has_clocked_in = QtCore.Signal(dict)
    set_latest_timesheet = QtCore.Signal(dict)

    # MUTEX & WAIT CONDITIONS
    mutex_1 = QtCore.QMutex()
    mutex_2 = QtCore.QMutex()
    mutex_3 = QtCore.QMutex()
    mutex_4 = QtCore.QMutex()
    wait_cond_1 = QtCore.QWaitCondition()
    wait_cond_2 = QtCore.QWaitCondition()
    wait_cond_3 = QtCore.QWaitCondition()
    wait_cond_4 = QtCore.QWaitCondition()


# -------------------------------------------------------------------------------------------------------------------
# Clocks Engine
# -------------------------------------------------------------------------------------------------------------------
class time_engine(QtCore.QThread):
    # This bit is trial and error.  It may have to go into the main UI, but my fear is that
    # the process will hang up the UI.
    '''
    This engine runs the clock faces
    '''
    def __init__(self, parent=None):
        super(time_engine, self).__init__(parent)

        self.time_signal = time_signals()
        self.time_machine = time_machine()
        self.latest_timesheet = tl_time.get_latest_timesheet(user=user)
        self.kill_it = False
        self.kill_signal = self.time_signal.kill_signal.connect(self.kill)
        self.tick = QtCore.QTime.currentTime()

        self.time_signal.get_running_clock.connect(self.set_latest_timesheet)
        self.time_signal.log.emit('Time Engine Started.')

    def kill(self):
        self.kill_it = True

    def set_latest_timesheet(self, ts=None):
        self.time_signal.log.emit('Updating Engine Timesheet...')
        self.time_signal.debug.emit('time_engine: Last Timesheet Updated: %s' % ts)
        if ts:
            self.latest_timesheet = ts
            self.time_signal.log.emit('Engine Timesheet Updated.')

    def run(self, *args, **kwargs):
        self.chronograph()

    def set_trt_output(self, trt=None):
        # logger.debug('Set TRT: %s' % trt)
        set_message = 'TRT: %s' % trt
        self.time_signal.trt_output.emit(set_message)

    def set_start_end_output(self):
        latest_timesheet = self.latest_timesheet
        last_in_time = latest_timesheet['sg_task_start']
        last_out_time = latest_timesheet['sg_task_end']
        if not last_in_time:
            self.latest_timesheet = tl_time.get_latest_timesheet(user=user)
            latest_timesheet = self.latest_timesheet
            last_in_time = latest_timesheet['sg_task_start']
            last_out_time = latest_timesheet['sg_task_end']

        try:
            if last_out_time:
                start = '%s %02d:%02d:%02d' % (datetime.now().date(), datetime.now().time().hour,
                                               datetime.now().time().minute, datetime.now().time().second)
                end = '%s %02d:%02d:%02d' % (last_out_time.date(), last_out_time.time().hour,
                                             last_out_time.time().minute, last_out_time.time().second)
            else:
                start = '%s %02d:%02d:%02d' % (last_in_time.date(), last_in_time.time().hour,
                                               last_in_time.time().minute, last_in_time.time().second)
                end = '%s %02d:%02d:%02d' % (datetime.now().date(), datetime.now().time().hour,
                                             datetime.now().time().minute, datetime.now().time().second)

            # Take the initial values and set their outputs.
            set_message = 'Start: %s\nEnd: %s' % (start, end)
            self.time_signal.start_end_output.emit(set_message)
        except Exception as e:
            self.time_signal.error.emit('Failed to update: %s' % e)

    def set_user_output(self, user=None):
        if self.latest_timesheet['sg_task_end']:
            in_out = 'OUT'
        else:
            in_out = 'IN'
        set_message = '%s CLOCKED %s' % (user['name'], in_out)
        self.time_signal.user_output.emit(set_message)

    def chronograph(self):
        self.time_signal.log.emit('Time Engine Chronograph has started.')
        second = int(datetime.now().second)
        day = datetime.now().day

        while not self.kill_it:
            midnight = datetime.combine(datetime.date(datetime.now()), datetime.min.time())
            if datetime.now() == midnight:
                self.time_signal.self_destruct.emit('Die!')
            if int(datetime.now().second) != second:
                # Set the clocks
                second = int(datetime.now().second)
                self.tick = QtCore.QTime.currentTime()
                hours = (30 * (self.tick.hour() + (self.tick.minute() / 60.0)))
                minutes = (6 * (self.tick.minute() + (self.tick.second() / 60.0)))
                time = (hours, minutes)

                # Send the time to the clocks.
                self.time_signal.main_clock.emit(time)
                self.time_signal.in_clock.emit(time)
                self.time_signal.out_clock.emit(time)

                # Setting the TRT
                rt = tl_time.get_running_time(timesheet=self.latest_timesheet)
                running_time = rt['rt']

                # Here we take the running time and emit it to the display.
                self.time_signal.running_clock.emit(running_time)
                trt = '%s:%s:%s' % (rt['h'], rt['m'], rt['s'])

                # Set the running time in the UI
                self.set_trt_output(trt=trt)
                self.set_start_end_output()
                self.set_user_output(user=user)

                if (second % 10) == 0:
                    last_timesheet = self.latest_timesheet
                    self.latest_timesheet = tl_time.get_latest_timesheet(user=user)
                    if last_timesheet != self.latest_timesheet:
                        self.time_signal.log.emit('Time Engine Timesheets don\'t match.  Updating Timesheet...')
                        self.time_signal.latest_timesheet.emit(self.latest_timesheet)
                    daily_total = tl_time.get_daily_total(user=user, lunch_id=int(lunch_task['id']))
                    weekly_total = tl_time.get_weekly_total(user=user, lunch_id=int(lunch_task['id']))
                    if daily_total:
                        self.time_signal.daily_total.emit(daily_total)
                    if weekly_total:
                        self.time_signal.weekly_total.emit(weekly_total)
                if datetime.now().day != day:
                    print('Auto Close At Midnight')
                    self.time_signal.auto_close.emit(True)


# ------------------------------------------------------------------------------------------------------
# Primary Engine
# ------------------------------------------------------------------------------------------------------
class time_machine(QtCore.QThread):
    """
    The Time Machine is the Event Listener that checks for New or Changed User Timesheets and then triggers
    events that will keep the UI up to date.
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
        self.time_lord = time_lord()
        self.time_signal.log.emit('Time Machine Started.')

    def run(self, *args, **kwargs):
        self.listener()

    def kill(self):
        self.kill_it = True

    def get_time_capsule(self):
        """
        This will open and collect the current time capsule file.
        :return:
        """
        if os.path.exists(self.db_path):
            fh = open(self.db_path, 'rb')
            db_file = pickle.load(fh)
            fh.close()
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
                fh = open(self.db_path, 'wb')
                pickle.dump(data, fh)
                fh.close()

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
                        self.time_signal.debug.emit('Events collected! %s' % events)
                        # print 'New Events Collected!', events
                        return events
                except (sgapi.ProtocolError, sgapi.ResponseError, socket.error) as err:
                    self.time_signal.warning.emit('Shotgun API Failure.  Trying again... %s' % err)
                    conn_attempts += 1
                    time.sleep(5)
                    if conn_attempts > 10:
                        self.time_signal.error.emit('Can\'t connect to shotgun!', err)
                        break
                except Exception as err:
                    self.time_signal.debug.emit('Unknown exception!  Trying again. %s' % err)
                    conn_attempts += 1
                    time.sleep(5)
                    if conn_attempts > 10:
                        self.time_signal.error.emit('Something went wrong! %s' % err)
                        error = '%s:\n%s | %s\n%s | %s' % (err, inspect.stack()[0][2], inspect.stack()[0][3],
                                                           inspect.stack()[1][2], inspect.stack()[1][3])
                        comm.send_error_alert(user=user, error=error)
                        break
        return []

    def listener(self):
        """
        The main loop listener.  This is listening for Shotgun events, and specifically TimeLog events.
        :return:
        """
        self.time_signal.debug.emit('Starting the main event listener loop...')
        self.time_signal.log.emit('Listener Loop Started')
        while not self.kill_it:
            # Adding a sleep timer to better minimize the data load
            time.sleep(1)
            events = self.get_new_events()
            if events:
                for event in events:
                    time_capsule = self.get_time_capsule()
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
                                    # This is the first time the timesheet has been clocked out.

                                    # Collect the entity
                                    ts_entity = sg_data.get_entity_from_task(task_id=timesheet_info['entity']['id'])

                                    self.time_signal.debug.emit('CLOCK OUT RECORD! %s' % event)

                                    self.time_signal.log.emit('Sending UI Update signal')
                                    self.time_signal.debug.emit('Timesheet update emitted.')

                                    # Update the time_lord ui
                                    self.time_signal.update_ui.emit(timesheet_info)

                                    data = {
                                        'EventLogID': event['id'],
                                        'TimeLogID': event['entity']['id'],
                                        'current': False
                                    }
                                    try:
                                        self.save_time_capsule(data)
                                        self.time_signal.debug.emit('Time Capsule saved!')
                                    except IOError as e:
                                        self.time_signal.warning.emit('Failed to save the file.  Trying again in a few '
                                                       'seconds... %s' % e)
                                        time.sleep(2)
                                        self.save_time_capsule(data)
                                elif not timesheet_info['sg_task_end'] and not time_capsule['current'] or \
                                        event['entity']['id'] > time_capsule['TimeLogID']:

                                    # Collect the entity
                                    ts_entity = sg_data.get_entity_from_task(task_id=timesheet_info['entity']['id'])

                                    self.time_signal.debug.emit('NEW RECORD! %s' % event['id'])
                                    ts_data = {
                                        'project': timesheet_info['project']['name'],
                                        'project_id': timesheet_info['project']['id'],
                                        'entity': ts_entity['entity']['name'],
                                        'entity_id': ts_entity['entity']['id'],
                                        'task': timesheet_info['entity']['name'],
                                        'task_id': timesheet_info['entity']['id']
                                    }
                                    self.time_lord.time_signal.update.emit(ts_data)
                                    self.time_lord.time_signal.wait_cond_1.wait(self.time_lord.time_signal.mutex_1)
                                    new_timesheet = tl_time.get_latest_timesheet(user=user)
                                    # self.time_lord.time_signal.latest_timesheet.emit(new_timesheet)
                                    self.time_signal.latest_timesheet.emit(new_timesheet)

                                    data = {
                                        'EventLogID': event['id'],
                                        'TimeLogID': event['entity']['id'],
                                        'current': True
                                    }
                                    try:
                                        self.save_time_capsule(data)
                                    except IOError as e:
                                        self.time_signal.warning.emit('Failed to save the file.  Trying again in a few '
                                                       'seconds... %s' % e)
                                        time.sleep(2)
                                        self.save_time_capsule(data)
                                else:
                                    self.time_signal.debug.emit('Event skipped.  Updating...')
                                    data = {
                                        'EventLogID': event['id'],
                                        'TimeLogID': timesheet_info['id'],
                                        'current': time_capsule['current']
                                    }
                                    try:
                                        self.save_time_capsule(data)
                                    except IOError as e:
                                        self.time_signal.warning.emit('Failed to save the file.  Trying again in a few '
                                                       'seconds... %s' % e)
                                        time.sleep(2)
                                        self.save_time_capsule(data)

                            else:
                                data = {
                                    'EventLogID': event['id'],
                                    'TimeLogID': time_capsule['TimeLogID'],
                                    'current': time_capsule['current']
                                }
                                try:
                                    self.save_time_capsule(data)
                                except IOError as e:
                                    self.time_signal.warning.emit('Failed to save the file.  Trying again in a few '
                                                   'seconds... %s' % e)
                                    time.sleep(2)
                                    self.save_time_capsule(data)
                    elif event['entity']['id'] != time_capsule['TimeLogID'] \
                            and event['id'] > time_capsule['EventLogID']:
                        data = {
                            'EventLogID': event['id'],
                            'TimeLogID': time_capsule['TimeLogID'],
                            'current': time_capsule['current']
                        }
                        try:
                            self.save_time_capsule(data)
                        except IOError as e:
                            self.time_signal.warning.emit('Failed to save the file.  Trying again in a few '
                                                          'seconds... %s' % e)
                            time.sleep(2)
                            self.save_time_capsule(data)


# ------------------------------------------------------------------------------------------------------
# Primary Tools
# ------------------------------------------------------------------------------------------------------
class time_lord(QtCore.QThread):
    """
    The Time Lord method is the main set of tools for updating the UI and processing events.
    It is not threaded or timed, but simply runs commands when called.
    Signals will be picked up by this and processes will then emit the needed data back to the UI
    """
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.time_signal = time_signals()
        self.kill_it = False
        self.clocked_in = tl_time.is_user_clocked_in(user=user)
        self.error_state = False
        self.steady_state = True
        self.latest_timesheet = tl_time.get_latest_timesheet(user=user)

        # Signal Connections
        self.time_signal.update.connect(self.update_ui)
        self.time_signal.req_project_update.connect(self.send_project_update)
        self.time_signal.req_entity_update.connect(self.send_entity_update)
        self.time_signal.req_task_update.connect(self.send_task_update)
        self.time_signal.clock_in_user.connect(self.clock_in_user)
        self.time_signal.clock_out_user.connect(self.clock_out_user)
        self.time_signal.user_clocked_in.connect(self.set_user_status)
        self.time_signal.log.emit('Time Lord Started.')

    def set_trt_output(self, trt=None):
        # logger.debug('Set TRT: %s' % trt)
        set_message = 'TRT: %s' % trt
        self.time_signal.trt_output.emit(set_message)

    def send_project_update(self, message=None):
        self.time_signal.debug.emit('Collecting projects for return')
        projects = sg_data.get_active_projects(user=user)
        self.time_signal.send_project_update.emit(projects)
        return projects

    def send_entity_update(self, proj_id=None):
        self.time_signal.debug.emit('send_entity_update: %s' % proj_id)
        if proj_id:
            self.time_signal.debug.emit('Project ID received by Entity Update Request: %s' % proj_id)

            asset_entities = sg_data.get_project_assets(proj_id=proj_id)
            self.time_signal.debug.emit('Assets collected: %s' % asset_entities)

            shot_entities = sg_data.get_project_shots(proj_id=proj_id)
            self.time_signal.debug.emit('Shots Collected: %s' % shot_entities)
            entities = asset_entities + shot_entities
            self.time_signal.send_entity_update.emit(entities)

    def send_task_update(self, context=None):
        self.time_signal.debug.emit('Send tasks activated! %s' % context)
        if context:
            self.time_signal.debug.emit('send_task_update context: %s' % context)
            self.time_signal.debug.emit('Task update requests. Context: %s' % context)

            entity_id = context['entity_id']
            entity_name = context['entity_name']
            proj_id = context['proj_id']
            self.time_signal.debug.emit('requesting tasks....')
            tasks = sg_data.get_entity_tasks(entity_id=entity_id, entity_name=entity_name, proj_id=proj_id)
            self.time_signal.debug.emit('tasks received: %s' % tasks)
            if tasks:
                self.time_signal.debug.emit('Sending a signal...')
                self.time_signal.send_task_update.emit(tasks)
                self.time_signal.debug.emit('Task signal sent.')
                self.time_signal.debug.emit('Tasks emitted: %s' % tasks)

    def req_start_end_output(self):
        latest_timesheet = tl_time.get_latest_timesheet(user=user)
        last_in_time = latest_timesheet['sg_task_start']
        last_out_time = latest_timesheet['sg_task_end']

        try:
            start = '%s %s' % (last_in_time.date(), last_in_time.time())
            if last_out_time:
                end = '%s %s' % (last_out_time.date(), last_out_time.time())
            else:
                end = '%s %s' % (datetime.now().date(), datetime.now().time())

            # Take the initial values and set their outputs.
            self.set_start_end_output(start=start, end=end)
        except Exception as e:
            self.time_signal.error.emit('Failed to update: %s' % e)
            error = '%s:\n%s | %s\n%s | %s' % (e, inspect.stack()[0][2], inspect.stack()[0][3],
                                               inspect.stack()[1][2], inspect.stack()[1][3])
            comm.send_error_alert(user=user, error=error)

    def set_start_end_output(self, start=None, end=None):
        set_message = 'Start: %s\nEnd: %s' % (start, end)
        self.time_signal.start_end_output.emit(set_message)

    def set_user_status(self, clocked_in=True):
        self.time_signal.debug.emit('User Status: User Clocked In: %s' % clocked_in)
        self.clocked_in = clocked_in

    def set_daily_output(self, daily=None):
        """
        Creates a message for the output monitor and emits a signal.
        :param daily: (float) Total of hours currently worked.
        :return: daily_output.emit()
        """
        set_message = 'Daily Total: %0.2f Hours' % daily
        self.time_signal.daily_output.emit(set_message)

    def set_weekly_output(self, weekly=None):
        set_message = 'Weekly Total: %0.2f Hours' % weekly
        self.time_signal.weekly_output.emit(set_message)

    def update_ui(self, data=None):
        """
        This is the place where heavier processes will be put together and then emitted to the appropriate
        UI slot.
        :param data: (dict) A collection of data from the UI or from the saved data.
        :return:
        """
        mutex = QtCore.QMutexLocker(self.time_signal.mutex_1)
        self.time_signal.debug.emit('Update Detected: %s' % data)
        # print('update_ui:', inspect.stack()[0][2], inspect.stack()[0][3], inspect.stack()[1][2],
        #       inspect.stack()[1][3])
        self.time_signal.debug.emit('Signal Received: %s' % data)
        # Get the last timesheet for local use and emit it for use elsewhere.
        self.latest_timesheet = {'project': None, 'entity': None}
        tries = 0
        while not self.latest_timesheet['project'] and not self.latest_timesheet['entity'] and tries <= 10:
            self.time_signal.debug.emit('Timesheet was blank.  Getting it again...')
            self.latest_timesheet = tl_time.get_latest_timesheet(user=user)
            time.sleep(2)
            tries += 1
        if not self.latest_timesheet['project']:
            self.time_signal.wait_cond_1.wakeAll()
            return False
        self.time_signal.debug.emit('update ui latest_timesheet: %s' % self.latest_timesheet)
        # self.time_signal.latest_timesheet.emit(self.latest_timesheet)

        # Collect Project/Entity/Task Data from Timesheet
        project = self.latest_timesheet['project']['name']
        project_id = self.latest_timesheet['project']['id']
        task = self.latest_timesheet['entity']['name']
        task_id = self.latest_timesheet['entity']['id']

        # Get Entity from task and project IDs
        entity_info = sg_data.get_entity_from_task(task_id=task_id)
        entity = entity_info['entity']['name']
        entity_id = entity_info['entity']['id']

        # Emit update signals.
        send_proj = {'type': 'project_dropdown',
                     'name': project}
        send_ent = {'type': 'entity_dropdown',
                    'name': entity}
        send_task = {'type': 'task_dropdown',
                     'name': task}
        self.time_signal.log.emit('About to send signals for update...')
        self.time_signal.update_ui.emit(self.latest_timesheet)
        # self.time_signal.wait_cond_1.wakeAll()
        # self.send_project_update()
        # self.time_signal.set_dropdown.emit(send_proj)
        # self.time_signal.set_dropdown.emit(send_ent)
        # self.time_signal.set_dropdown.emit(send_task)
        # projects = self.send_project_update(message='Update Projects')
        # self.time_signal.send_project_update.emit(projects)
        self.time_signal.log.emit('==> SEND PROJ: %s' % send_proj['name'])
        self.time_signal.log.emit('==> SEND ENT: %s' % send_ent['name'])
        self.time_signal.log.emit('==> SEND TASK: %s' % send_task['name'])
        self.time_signal.log.emit('Three signals sent.')

    def quick_update(self):
        """
        First function to get called by the UI __init__.
        Updates the current timesheet and emits it back to the UI
        :return: self.time_signal.send_timesheet.emit(new_timesheet)
        """
        self.time_signal.debug.emit('Communication received.  Updating....')
        new_timesheet = tl_time.get_latest_timesheet(user=user)
        if new_timesheet:
            self.time_signal.debug.emit('Timesheet collected!')
            self.time_signal.send_timesheet.emit(new_timesheet)
            self.latest_timesheet = new_timesheet

    def get_active_projects(self, message=None):
        if message:
            self.time_signal.debug.emit('Project List Requested!')
            active_projects = sg_data.get_active_projects(user=user)
            if active_projects:
                # wait_cond.wakeAll()
                if message == 'initialize':
                    return active_projects
                else:
                    self.time_signal.set_project_list.emit(active_projects)
                    self.quick_update()

    def set_daily_total(self, message=None):
        """
        Sets and emits the Daily Total function back to the UI
        :param message: A string of any kind to kick start the process and trigger a log
        :return:
        """
        self.time_signal.debug.emit('set daily total: %s' % message)
        daily_total = None
        if message:
            daily_total = tl_time.get_daily_total(user=user, lunch_id=int(lunch_task['id']))
            if daily_total or daily_total >= 0.0:
                self.time_signal.debug.emit('Daily total!: %s' % daily_total)
                self.time_signal.daily_total.emit(daily_total)
                self.time_signal.debug.emit('Daily total emitted')
        return daily_total

    def set_weekly_total(self, message=None):
        # Sets and emiits the Weekly Total function back to the UI
        weekly_total = None
        if message:
            weekly_total = tl_time.get_weekly_total(user=user, lunch_id=int(lunch_task['id']))
            if weekly_total or weekly_total >= 0.0:
                self.time_signal.weekly_total.emit(weekly_total)
                self.time_signal.debug.emit('Weekly total emitted')
        return weekly_total

    def clock_out_user(self, latest_timesheet=None):
        if latest_timesheet:
            self.time_signal.mutex_1.lock()
            self.time_signal.log.emit('Clocking out...')
            clocked_out = tl_time.clock_out_time_sheet(timesheet=latest_timesheet, clock_out=datetime.now())
            self.time_signal.log.emit('Clocked out at %s' % clocked_out['sg_task_end'])
            latest_timesheet = tl_time.get_timesheet_by_id(tid=latest_timesheet['id'])
            self.time_signal.mutex_1.unlock()
            self.time_signal.wait_cond_1.wakeAll()
            self.time_signal.lower_output.emit('You have clocked out!')
            ts_start = latest_timesheet['sg_task_start']
            start_date = ts_start.strftime('%m-%d-%y')
            self.time_signal.in_date.emit(start_date)
            try:
                start = '%s %s' % (latest_timesheet['sg_task_start'].date(),
                                   latest_timesheet['sg_task_start'].time())
                end = '%s %s' % (latest_timesheet['sg_task_end'].date(),
                                 latest_timesheet['sg_task_end'].time())
                self.set_start_end_output(start=start, end=end)
            except (AttributeError, KeyError) as e:
                self.time_signal.warning.emit('Couldn\'t update the start and end times! %s' % e)
            daily_total = self.set_daily_total('Get')
            weekly_total = self.set_weekly_total('Get')
            self.set_trt_output(trt='00:00:00')
            self.set_user_output(user=user)
            self.set_daily_output(daily=daily_total)
            self.set_weekly_output(weekly=weekly_total)
            self.time_signal.log.emit('Requesting Cleanup Process...')
            self.do_cleanup()
            # self.time_signal.update_timesheet.emit('Update')

    def clock_in_user(self, data=None):
        """
        This may need some addition inputs, but for now... nothing.
        :return:
        """
        # print('clock_in_user:', inspect.stack()[0][2], inspect.stack()[0][3], inspect.stack()[1][2],
        #       inspect.stack()[1][3])
        if data:
            self.clocked_in = True
            self.time_signal.log.emit('Clocking in...')
            context = data[0]
            start_time = data[1]
            self.time_signal.mutex_1.lock()
            timesheet = tl_time.create_new_timesheet(user=user, context=context, start_time=start_time)
            self.time_signal.log.emit('New Timesheet: %s' % timesheet['id'])
            self.time_signal.mutex_1.unlock()
            self.set_user_output(user=user)
            self.time_signal.user_has_clocked_in.emit(timesheet)

    def set_user_output(self, user=None):
        if self.clocked_in:
            in_out = 'IN'
        else:
            in_out = 'OUT'
        set_message = '%s CLOCKED %s' % (user['name'], in_out)
        self.time_signal.user_output.emit(set_message)

    def get_entities(self, entity_id=None, r=False):
        self.time_signal.debug.emit('get_entities activated: entity id: %s' % entity_id)
        if entity_id:
            asset_entities = sg_data.get_project_assets(proj_id=entity_id)
            self.time_signal.debug.emit('Assets collected: %s' % asset_entities)
            shot_entities = sg_data.get_project_shots(proj_id=entity_id)
            self.time_signal.debug.emit('Shots Collected: %s' % shot_entities)
            entities = asset_entities + shot_entities
            latest_timesheet = tl_time.get_latest_timesheet(user=user)
            if r:
                return latest_timesheet, entities
            else:
                self.time_signal.set_entity_list.emit((latest_timesheet, entities))
            self.time_signal.debug.emit('get_entities: %s' % entities)

    def get_tasks(self, context=None, r=False):
        self.time_signal.debug.emit('get_tasks activated: %s' % context)
        if context:
            entity_id = context['entity_id']
            entity_name = context['entity_name']
            proj_id = context['proj_id']
            tasks = sg_data.get_entity_tasks(entity_id=entity_id, entity_name=entity_name, proj_id=proj_id)
            if tasks:
                if r:
                    return tasks
                else:
                    self.time_signal.set_task_list.emit(tasks)
                self.time_signal.debug.emit('Tasks emitted: %s' % tasks)

    def set_latest_timesheet(self, message=None):
        if message:
            timesheet = tl_time.get_latest_timesheet(user=user)
            self.time_signal.send_timesheet.emit(timesheet)
            time.sleep(0.1)
            self.time_signal.user_has_clocked_in.emit(timesheet)

    def do_cleanup(self):
        """
        This method checks older timesheets and makes sure they are all properly clocked in and out.
        :return: True or False
        """
        cleanup = tl_time.timesheet_cleanup(user=user)
        if cleanup:
            self.time_signal.debug.emit('CLEANUP: %s' % cleanup)
            self.time_signal.debug.emit('Cleanup processing... %s' % cleanup)
        consistency_check = tl_time.timesheet_consistency_cleanup(user=user, clock_out=True)
        if consistency_check:
            self.time_signal.debug.emit('Timesheet consistency check finished: %s' % consistency_check)
            self.time_signal.debug.emit('Consistency check: %s' % consistency_check)


# ------------------------------------------------------------------------------------------------------
# User Interface
# ------------------------------------------------------------------------------------------------------
class time_lord_ui(QtGui.QMainWindow):
    def __init__(self, parent=None):
        # super(time_lord_ui, self).__init__(parent=None)
        QtGui.QMainWindow.__init__(self, parent)

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
        self.saved_window_position = self.settings.value('geometry', '')
        self.restoreGeometry(self.saved_window_position)

        # --------------------------------------------------------------------------------------------------------
        # Setup Time Engine
        # --------------------------------------------------------------------------------------------------------
        # Setup and connect the last timesheet.
        # Declare Class Variables
        self.latest_timesheet = tl_time.get_latest_timesheet(user=user)
        if not self.latest_timesheet['project'] and not self.latest_timesheet['entity'] \
                and not self.latest_timesheet['date'] and not self.latest_timesheet['sg_task_start']:
            project_id = int(config['admin_proj_id'])
            task_id = int(config['admin_task_id'])
            entity_id = sg_data.get_entity_from_task(task_id=task_id)
            context = {
                'Project': {
                    'id': project_id
                },
                'Task': {
                    'id': task_id
                },
                'Entity': {
                    'id': entity_id,
                }
            }
            start_time = datetime.now()
            first_sheet = tl_time.create_new_timesheet(user=user, context=context, start_time=start_time)
            if first_sheet:
                tl_time.clock_out_time_sheet(timesheet=first_sheet, clock_out=start_time)

        self.clocked_in = tl_time.is_user_clocked_in(user=user)

        # Connect to the threads
        self.time_lord = time_lord()
        self.time_engine = time_engine()
        self.time_machine = time_machine()
        self.time_signal = time_signals()

        # --------------------------------------------------------------------------------------------------------
        # Setup UI
        # --------------------------------------------------------------------------------------------------------
        self.ui = tlu.Ui_TimeLord()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
        self.setWindowTitle("Time Lord v%s" % __version__)
        self.window_on_top_tested = False
        self.set_window_on_top()
        # Set main user info
        self.ui.artist_label.setText(user['name'])
        # Set the rollers
        # TODO: Make sure the date rollers are pulling from the Time Sheet as well
        now = datetime.now()
        d = now.strftime('%m-%d-%y')
        self.set_start_date_rollers(d=d)
        self.set_end_date_rollers(d=d)

        # --------------------------------------------------------------------------------------------------------
        # Setup Stream Handler
        # --------------------------------------------------------------------------------------------------------
        self.time_stream = time_stream()
        self.ui.lower_output.setMaximumBlockCount(10)
        self.time_stream.edit = self.ui.lower_output
        logger.addHandler(self.time_stream)

        # Connect the logging output.
        self.time_machine.time_signal.log.connect(self.log)
        self.time_engine.time_signal.log.connect(self.log)
        self.time_lord.time_signal.log.connect(self.log)
        self.time_engine.time_signal.debug.connect(self.debug)
        self.time_lord.time_signal.debug.connect(self.debug)
        self.time_machine.time_signal.debug.connect(self.debug)
        self.time_engine.time_signal.error.connect(self.error)
        self.time_lord.time_signal.error.connect(self.error)
        self.time_machine.time_signal.error.connect(self.error)
        self.time_engine.time_signal.warning.connect(self.warning)
        self.time_lord.time_signal.warning.connect(self.warning)
        self.time_machine.time_signal.warning.connect(self.warning)

        # --------------------------------------------------------------------------------------------------------
        # Signal Connections
        # --------------------------------------------------------------------------------------------------------
        # Clock function signals
        self.time_engine.time_signal.main_clock.connect(self.main_clock)
        self.time_engine.time_signal.in_clock.connect(self.set_in_clock)
        self.time_engine.time_signal.out_clock.connect(self.set_out_clock)
        self.time_engine.time_signal.running_clock.connect(self.set_runtime_clock)
        self.time_engine.time_signal.daily_total.connect(self.set_daily_total_needle)
        self.time_lord.time_signal.daily_total.connect(self.set_daily_total_needle)
        self.time_engine.time_signal.weekly_total.connect(self.set_weekly_total_needle)
        self.time_lord.time_signal.weekly_total.connect(self.set_weekly_total_needle)

        # Update Connections
        self.time_lord.time_signal.send_project_update.connect(self.update_projects_dropdown)
        self.time_lord.time_signal.send_entity_update.connect(self.update_entity_dropdown)
        self.time_lord.time_signal.send_task_update.connect(self.update_task_dropdown)
        self.time_lord.time_signal.update_ui.connect(self.init_ui)
        self.time_machine.time_signal.update_ui.connect(self.init_ui)
        self.time_engine.time_signal.update_ui.connect(self.init_ui)
        self.time_signal.update_ui.connect(self.init_ui)
        self.time_machine.time_signal.latest_timesheet.connect(self.update_latest_timesheet)
        self.time_engine.time_signal.latest_timesheet.connect(self.update_latest_timesheet)
        self.time_lord.time_signal.latest_timesheet.connect(self.update_latest_timesheet)
        self.time_signal.latest_timesheet.connect(self.update_latest_timesheet)
        self.time_engine.time_signal.trt_output.connect(self.trt_output)
        self.time_engine.time_signal.start_end_output.connect(self.start_end_output)
        self.time_engine.time_signal.user_output.connect(self.user_output)
        self.time_engine.time_signal.self_destruct.connect(self.close)

        # Dropdown Change Index Connections
        self.time_lord.time_signal.set_dropdown.connect(self.set_dropdown)
        self.ui.project_dropdown.currentIndexChanged.connect(self.req_update_entities)
        # Then change the button color to Yellow, Red or Green
        self.ui.project_dropdown.currentIndexChanged.connect(lambda: self.switch_state(self.latest_timesheet))
        self.ui.entity_dropdown.currentIndexChanged.connect(self.req_update_tasks)
        self.ui.entity_dropdown.currentIndexChanged.connect(lambda: self.switch_state(self.latest_timesheet))
        self.switch_state(self.latest_timesheet)

        # Kill Signal
        self.time_engine.time_signal.auto_close.connect(self.close)

        # Do First Update
        data = {
            'project': self.saved_project,
            'project_id': self.saved_project_id,
            'entity': self.saved_entity,
            'entity_id': self.saved_entity_id,
            'task': self.saved_task,
            'task_id': self.saved_task_id
        }
        # self.time_lord.time_signal.update.emit(data)

        # Initialize the dropdowns
        self.init_ui()

        # Start the engines
        self.time_engine.start()
        self.time_machine.start()
        self.time_lord.start()

    def init_ui(self, received_timesheet=None):
        """
        This may actually need to pull some data from Shotgun directly.  That's ok, since it only runs
        once at the onset.
        The idea is that this routine will set the initial values from the saved settings.
        :return: None
        """
        if received_timesheet:
            logger.info('CLEARING UI...')
            self.ui.project_dropdown.clear()
            self.ui.entity_dropdown.clear()
            self.ui.task_dropdown.clear()
            self.latest_timesheet = received_timesheet
        logger.info('INITIALIZING UI...')
        projects = sg_data.get_active_projects(user=user)
        if projects:
            # Check the saved project against the current timesheet
            try:
                if self.saved_project != self.latest_timesheet['project']['name']:
                    self.saved_project = self.latest_timesheet['project']['name']
                    self.saved_project_id = self.latest_timesheet['project']['id']
            except TypeError as e:
                logger.error('Couldn\'t compare latest timesheet: %s ' % e)
                error = '%s:\n%s | %s\n%s | %s' % (e, inspect.stack()[0][2], inspect.stack()[0][3],
                                                   inspect.stack()[1][2], inspect.stack()[1][3])
                comm.send_error_alert(user=user, error=error)

            # Update the dropdown list
            self.update_projects_dropdown(projects)
            proj_id = self.ui.project_dropdown.itemData(self.ui.project_dropdown.currentIndex())

            # Collect Entities
            assets = sg_data.get_project_assets(proj_id=proj_id)
            shots = sg_data.get_project_shots(proj_id=proj_id)
            entities = assets + shots

            # Get the timesheet entity and compare it to the saved entity
            try:
                ts_task_id = self.latest_timesheet['entity']['id']
                get_current_entity = sg_data.get_entity_from_task(task_id=ts_task_id)
                current_entity = get_current_entity['entity']['name']
                current_entity_id = get_current_entity['entity']['id']
                if self.saved_entity != current_entity:
                    self.saved_entity = current_entity
                    self.saved_entity_id = current_entity_id

                if self.saved_task != self.latest_timesheet['entity']['name']:
                    self.saved_task = self.latest_timesheet['entity']['name']
                    self.saved_task_id = self.latest_timesheet['entity']['id']
            except TypeError as e:
                logger.error('Can\'t compare timesheets. Most likely there was no previous timesheet:'
                             '%s' % e)
                error = '%s:\n%s | %s\n%s | %s' % (e, inspect.stack()[0][2], inspect.stack()[0][3],
                                                   inspect.stack()[1][2], inspect.stack()[1][3])
                comm.send_error_alert(user=user, error=error)

            # Update the Entities dropdown
            self.update_entity_dropdown(entities=entities)
            entity = self.ui.entity_dropdown.currentText()
            entity_id = self.ui.entity_dropdown.itemData(self.ui.entity_dropdown.currentIndex())

            # Collect Tasks
            tasks = sg_data.get_entity_tasks(entity_id=entity_id, entity_name=entity, proj_id=proj_id)
            self.update_task_dropdown(tasks=tasks)

            if tl_time.is_user_clocked_in(user=user):
                logger.info('Setting button to "Clocked In"')
                self.clock_in_button_state(1)
            else:
                logger.info('Setting button to "Clocked Out"')
                self.clock_in_button_state(0)

            daily_total = tl_time.get_daily_total(user=user, lunch_id=int(lunch_task['id']))
            weekly_total = tl_time.get_weekly_total(user=user, lunch_id=int(lunch_task['id']))
            if daily_total:
                self.set_daily_total_needle(daily_total)
            if weekly_total:
                self.set_weekly_total_needle(weekly_total)

    # ----------------------------------------------------------------------------------------------------------------
    # Status lights and button states.
    # ----------------------------------------------------------------------------------------------------------------
    def error_state(self, message=None):
        # This method turns on or off the red error state light
        if message:
            self.ui.red_light.setVisible(True)
        else:
            self.ui.red_light.setVisible(False)

    def steady_state(self, message=None):
        # This method turns on or off the green steady state light.?
        if message:
            self.ui.green_light.setVisible(True)
        else:
            self.ui.green_light.setVisible(False)

    def switch_state(self, data=None):
        """
        First checks to see if the dropdowns match the current timesheet. Set match = False if not.

        :param data: (dict) A timesheet log item
        :return: None
        """
        logger.debug('Switch States: %s' % data)
        logger.debug('Checking state shit:')
        logger.debug('Switch state triggered')
        match = True

        selected_proj = self.ui.project_dropdown.currentText()
        logger.debug('selected_proj: %s' % selected_proj)
        logger.debug('selected_entity: %s' % self.ui.entity_dropdown.currentText())
        logger.debug('selected_task: %s' % self.ui.task_dropdown.currentText())

        # Check that the project matches
        if selected_proj != self.saved_project:
            logger.debug('Last project name does not match.')
            match = False

        # I get the entity, because it does not come with latest_timesheet data
        if self.saved_entity != self.ui.entity_dropdown.currentText():
            logger.debug('The entity does not match the dropdown.')
            match = False

        if self.saved_task != self.ui.task_dropdown.currentText():
            logger.debug('Tasks aren\'t cool.')
            match = False
        logger.debug('Finished with match check: %s' % match)

        if match and self.clocked_in:
            logger.debug('Matched and Clocked In.  Emit 1')
            logger.debug('match and timelord clocked in.  Emit 1')
            self.clock_in_button_state(1)
        elif not match and self.clocked_in:
            logger.debug('NOT Matched! And Clocked In.  Emit 2')
            logger.debug('Not matched and timelord clocked in.  Emit 2')
            self.clock_in_button_state(2)
        elif not self.clocked_in:
            logger.debug('NOT CLOCKED IN!!!  Emit 0')
            logger.debug('Timelord not clocked in.  Doesn\'t matter if it\'s matched.  Emit 0')
            self.clock_in_button_state(0)

    def set_window_on_top(self):
        if not self.window_on_top_tested:
            if tl_time.is_user_clocked_in(user=user):
                self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
                self.window_on_top_tested = True
                self.show()
            else:
                self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)

    # ----------------------------------------------------------------------------------------------------------------
    # Runtime Clocks - Main, TRT, Start Datetime, End Datetime
    # ----------------------------------------------------------------------------------------------------------------
    def main_clock(self, in_time):
        # Function that automatically updates UI when triggered by a signal
        # self.ui.test_counter.setText(in_time)
        hour = in_time[0]
        minute = in_time[1]
        hour_rot = QtGui.QTransform()
        minute_rot = QtGui.QTransform()
        hour_rot.rotate(hour)
        minute_rot.rotate(minute)

        hour_hand = QtGui.QPixmap(":/dial hands/elements/clock_1_hour.png")
        minute_hand = QtGui.QPixmap(":/dial hands/elements/clock_1_minute.png")
        hour_hand_rot = hour_hand.transformed(hour_rot)
        minute_hand_rot = minute_hand.transformed(minute_rot)

        self.ui.time_hour.setPixmap(hour_hand_rot)
        self.ui.time_minute.setPixmap(minute_hand_rot)
        self.ui.time_hour.update()
        self.ui.time_minute.update()

    def start_time(self):
        logger.debug('start_time activated!')
        if not self.time_lord.isRunning():
            self.time_lord.start()
        self.time_lord.clocked_in = True
        self.time_lord.kill_it = False
        logger.debug('update_saved_settings sent!')

        logger.debug('Sending to clock_in()')
        self.clock_in()
        self.update_saved_settings()
        logger.debug('clock_in() completed.')

    def stop_time(self):
        self.time_lord.clocked_in = False
        self.time_lord.kill_it = True
        self.clock_out()
        logger.debug('stop_time: clock_out() routing run')
        self.update_saved_settings()
        logger.debug('saved settings updated.')

    def switch_time(self):
        if self.selection_check():
            self.time_lord.clocked_in = False
            self.clock_out()
            self.clock_in()
            self.update_saved_settings()
            if not self.time_machine.isRunning():
                self.time_machine.start()

    def clock_out(self):
        self.clock_in_button_state(0)
        self.time_lord.time_signal.req_daily_total.emit('Update!')
        self.time_lord.time_signal.req_weekly_total.emit('Update!')
        self.time_lord.time_signal.clock_out_user.emit(self.latest_timesheet)
        logger.debug('clock_out has set state and emitted update requests')

    def clock_in(self, message=None):
        # Check to see if the UI settings are valid for a new timesheet.
        logger.debug('Clock in requested.  Checking selection')
        if not self.selection_check():
            logger.debug('The selections are invalid!')
            # The settings are invalid.  Kick it back.
            return False
        logger.debug('selection passed!')

        # Emit the Steady State green light signal, and update the output monitor.
        self.clock_in_button_state(1)

        self.time_lord.time_signal.lower_output.emit('New Timesheet created!')

        # Create context
        project_selection = self.ui.project_dropdown.currentText()
        project_id = self.ui.project_dropdown.itemData(self.ui.project_dropdown.currentIndex())
        project_name = project_selection
        entity_id = self.ui.entity_dropdown.itemData(self.ui.entity_dropdown.currentIndex())
        task_id = self.ui.task_dropdown.itemData(self.ui.task_dropdown.currentIndex())
        context = {
            'Project': {
                'id': project_id,
                'name': project_name,
            },
            'Task': {
                'id': task_id,
                'content': self.ui.task_dropdown.currentText()
            },
            'Entity': {
                'id': entity_id,
                'code': self.ui.entity_dropdown.currentText()
            }
        }

        # NOTE: This is a future feature that currently does nothing
        start_time = self.get_user_start_time()
        # Set the start time
        if not start_time:
            start_time = datetime.now()

        data = (context, start_time)
        self.time_lord.time_signal.clock_in_user.emit(data)
        self.set_window_on_top()
        self.clocked_in = tl_time.is_user_clocked_in(user=user)
        if not self.time_machine.isRunning():
            self.time_machine.start()

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
            start_time = self.latest_timesheet['sg_task_start']
            if start_time:
                hour = start_time.time().hour
                minute = start_time.time().minute
                second = start_time.time().second
                hours = (30 * (hour + (minute / 60.0)))
                minutes = (6 * (minute + (second / 60.0)))
            else:
                logger.warning('Bad Start Time!  Returning False', datetime.now())
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
            # self.latest_timesheet = tl_time.get_latest_timesheet(user=user)
            # self.timesheet_update.time_signal.ui_update.emit('Update!')
            # self.time_lord.time_signal.ui_update.emit()
            try:
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
        :param which: (str) One of two acceptable values: 'start', 'end'
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

    def set_dropdown(self, data=None):
        logger.debug('+++Update Signal received: %s | %s' % (data['type'], data['name']))
        # self.time_lord.time_signal.mutex_2.lock()
        if data:
            dd_type = data['type']
            dd_value = data['name']
        else:
            dd_value = None
            dd_type = None
        if dd_type and dd_value:
            widge = self.findChild(QtGui.QComboBox, dd_type)
            logger.debug('widge found: %s' % widge)
            if widge:
                new_index = widge.findText(dd_value)
                logger.debug('widge index: %s' % new_index)
                if new_index:
                    widge.setCurrentIndex(new_index)
                    logger.debug('widge set')
        # self.time_lord.time_signal.mutex_2.unlock()
        # self.time_lord.time_signal.wait_cond_2.wakeAll()

    # ----------------------------------------------------------------------------------------------------------------
    # OUTPUT MONITORS
    # ----------------------------------------------------------------------------------------------------------------
    def trt_output(self, message=None):
        self.ui.output_trt.setPlainText(message)

    def start_end_output(self, message=None):
        self.ui.output_start_end.setPlainText(message)

    def set_daily_total_needle(self, total):
        '''
        Set this to adjust the needs and the output monitor values simultaneously.
        :param total: A total value of the daily total hours minus lunch and breaks
        :return:
        '''
        if total:
            self.daily_output(total)
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
            self.weekly_output(total)
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

    def user_output(self, message=None):
        self.ui.output_user.setPlainText(message)

    def daily_output(self, message=None):
        total = 'Daily Total: %0.2f' % message
        self.ui.output_daily.setPlainText(str(total))

    def weekly_output(self, message=None):
        total = 'Weekly Total: %0.2f' % message
        self.ui.output_weekly.setPlainText(str(total))

    def lower_output(self, message=None):
        self.ui.lower_output.setPlainText(message)

    # ----------------------------------------------------------------------------------------------------------------
    # UI Events - Close, Update Saved Settings, Update UI Data
    # ----------------------------------------------------------------------------------------------------------------
    def closeEvent(self, *args, **kwargs):
        self.update_saved_settings()
        if self.time_engine.isRunning():
            self.time_engine.kill()
        if self.time_machine.isRunning():
            self.time_machine.kill()
        self.time_engine.kill_it = True
        self.time_machine.kill_it = True

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

    def update_from_ui(self, message=None):
        """
        This method may/should detect chenages outside of the UI. i.e. Drag-n-drop publisher, or a manual change in
        Shotgun.  Within 1 minute, this should change the UI to match the actual recorded time sheet.  Otherwise, shit
        can go all wrong.
        :param message: SIGNAL message.
        :return:
        """
        # Get the values from the UI
        project = self.ui.project_dropdown.currentText()
        project_id = self.ui.project_dropdown.itemData(self.ui.project_dropdown.currentIndex())
        entity = self.ui.entity_dropdown.currentText()
        entity_id = self.ui.entity_dropdown.itemData(self.ui.entity_dropdown.currentIndex())
        task = self.ui.task_dropdown.currentText()
        task_id = self.ui.task_dropdown.itemData(self.ui.task_dropdown.currentIndex())
        update = {
            'id': id,
            'project': project,
            'project_id': project_id,
            'entity': entity,
            'entity_id': entity_id,
            'task': task,
            'task_id': task_id
        }
        self.time_lord.time_signal.ui_update.emit(update)
        logger.debug('Emitted: %s' % update)

    def update_from_timesheet(self, message=None):
        logger.debug('Updating the UI with... %s' % message)
        if message:
            task = message['task']
            tast_id = message['task_id']
            proj = message['project']
            proj_id = message['project_id']
            entity = message['entity']
            entity_id = message['entity_id']

            proj_index = self.ui.project_dropdown.findText(proj)

            if proj_index >= 0:
                logger.debug('Updating project')
                self.ui.project_dropdown.setCurrentIndex(proj_index)
            self.request_entities()

            ent_index = self.ui.entity_dropdown.findText(entity)
            if ent_index >= 0:
                logger.debug('Updating entity...')
                self.ui.entity_dropdown.setCurrentIndex(ent_index)

            task_index = self.ui.task_dropdown.findText(task)
            if task_index >= 0:
                logger.debug('Updating Tasks...')
                self.ui.task_dropdown.setCurrentIndex(task_index)

            # Send a signal to update the local timesheet.
            logger.debug('~' * 60)
            logger.debug('IS CLOCKED IN: %s' % self.clocked_in)
            logger.debug('Testing last timesheet: %s' % self.latest_timesheet)

    # ----------------------------------------------------------------------------------------------------------------
    # Timesheet Data Updaters - Set the project, entity and task drop downs.
    # ----------------------------------------------------------------------------------------------------------------
    def update_projects_dropdown(self, projects=None):
        # Clear out the projects so that we are not double adding entries.
        logger.debug('Update projects dropdown...')
        self.ui.project_dropdown.clear()
        # Iterate through the list and add all the active projects to the dropdown
        if projects:
            for project in projects:
                self.ui.project_dropdown.addItem('%s' % project['name'], project['id'])
        logger.debug('Getting default selection from settings.')
        # Get the index of the last project as listed in the UI
        proj_index = self.ui.project_dropdown.findData(self.saved_project_id)
        # Select the current project.
        if proj_index >= 0:
            logger.debug('Setting project to last project listed.')
            self.ui.project_dropdown.setCurrentIndex(proj_index)
        logger.debug('triggering tasks dropdown reset...')
        self.update_task_dropdown()

    def req_update_entities(self, message=None):
        """
        This function will trigger another function that will update_entities.  The reason for this (instead of going
        directly to update_entities) is that update_entities requires more elaborate data than a
        currentIndexChanged.connect() event can support.
        :param message: String trigger.  Does nothing.
        :return:
        """
        logger.debug('req_update_entities: %s' % message)
        proj_id = self.ui.project_dropdown.itemData(self.ui.project_dropdown.currentIndex())
        self.time_lord.time_signal.req_entity_update.emit(proj_id)
        self.update_task_dropdown()

    def update_entity_dropdown(self, entities=None):
        """
        Processes data from a Shotgun Assets and Shots entity collection.
        :param entities: (dict) A combined dictionary from 2 queries
        :return: None
        """
        logger.debug('update entity dropdown signal %s' % entities)
        logger.debug(entities)
        if entities:
            # Put in the Assets first... Oh!  Use the categories and Sequences?
            self.ui.entity_dropdown.clear()
            self.ui.entity_dropdown.addItem('Select Asset/Shot', 0)
            for entity in entities:
                self.ui.entity_dropdown.addItem(entity['code'], entity['id'])
            self.ui.entity_dropdown.update()
        else:
            self.time_lord.time_signal.lower_output.emit('Project Dump: %s' % entities)
            self.time_lord.time_signal.error_state.emit(True)
            self.time_lord.time_signal.steady_state.emit(False)
        entity_index = self.ui.entity_dropdown.findData(self.saved_entity_id)
        if entity_index >= 0:
            logger.debug('Setting entity to last saved entity')
            self.ui.entity_dropdown.setCurrentIndex(entity_index)
        # TODO: Trigger a tasks update

    def req_update_tasks(self, message=None):
        """
        This method askes for a regular update from an onChangeEvent with no data
        :param message:
        :return:
        """
        logger.debug('Request Update Tasks activated.')
        ent_id = self.ui.entity_dropdown.itemData(self.ui.entity_dropdown.currentIndex())
        ent_name = self.ui.entity_dropdown.currentText()
        proj_index = self.ui.project_dropdown.currentIndex()

        if ent_id:
            context = {
                'entity_id': ent_id,
                'entity_name': ent_name,
                'proj_id': self.ui.project_dropdown.itemData(proj_index)
            }
            logger.debug('sending the req_task_update: %s' % context)
            self.time_lord.time_signal.req_task_update.emit(context)
            logger.debug('Done sending task context.')

    def update_task_dropdown(self, tasks=None):
        logger.debug('update_task_dropdown message received: %s' % tasks)
        logger.debug('Setting tasks...')
        logger.debug(tasks)
        if tasks:
            self.ui.task_dropdown.clear()
            self.ui.task_dropdown.addItem('Select Task', 0)
            for task in tasks:
                self.ui.task_dropdown.addItem(task['content'], task['id'])
            if self.saved_task != self.latest_timesheet['entity']['name']:
                self.saved_task = self.latest_timesheet['entity']['name']
            task_index = self.ui.task_dropdown.findText(self.saved_task)
            if task_index >= 0:
                self.ui.task_dropdown.setCurrentIndex(task_index)
            # Lastly, connect the Task to an on-change event
            self.ui.task_dropdown.currentIndexChanged.connect(lambda: self.switch_state(self.latest_timesheet))
            self.switch_tasks()
        else:
            self.ui.task_dropdown.clear()
            self.ui.task_dropdown.addItem('Select Task', 0)

    def switch_tasks(self):
        logger.debug('Switching tasks...')
        if self.saved_task != self.ui.task_dropdown.currentText() and self.clocked_in:
            self.time_lord.time_signal.clock_state.emit(2)
        else:
            if self.clocked_in:
                self.time_lord.time_signal.clock_state.emit(1)
            else:
                self.time_lord.time_signal.clock_state.emit(0)

    def selection_check(self):
        # Sets the Status Lights and adds Error Messages to the output monitor
        if self.ui.project_dropdown.currentText() == 'Select Project' or self.ui.project_dropdown.currentIndex() == 0:
            self.time_lord.time_signal.error_state.emit(True)
            self.time_lord.time_signal.steady_state.emit(False)
            self.time_lord.time_signal.lower_output.emit('You must select a Project!')
            # self.clocked_in = False
            return False
        else:
            self.time_lord.time_signal.error_state.emit(False)
            self.time_lord.time_signal.steady_state.emit(True)
        if self.ui.entity_dropdown.currentText() == 'Select Asset/Shot' or self.ui.entity_dropdown.currentIndex() == 0:
            self.time_lord.time_signal.error_state.emit(True)
            self.time_lord.time_signal.steady_state.emit(False)
            self.time_lord.time_signal.lower_output.emit('You must select an entity!')
            # self.clocked_in = False
            return False
        else:
            self.time_lord.time_signal.error_state.emit(False)
            self.time_lord.time_signal.steady_state.emit(True)
        if self.ui.task_dropdown.currentText() == 'Select Task' or self.ui.task_dropdown.currentIndex() == 0:
            self.time_lord.time_signal.error_state.emit(True)
            self.time_lord.time_signal.steady_state.emit(False)
            self.time_lord.time_signal.lower_output.emit('You must select a Task!')
            # self.clocked_in = False
            return False
        else:
            self.time_lord.time_signal.error_state.emit(False)
            self.time_lord.time_signal.steady_state.emit(True)
        return True

    def get_user_start_time(self):
        """
        Eventually, this should return a user set start time from the UI.  Not sure right off hand yet how to do that.
        :return:
        """
        return None

    def clock_in_button_state(self, message=None):
        """
        Takes an integer value between 0 and 2
        :param message: (int) 0 = clocked out, 1 = clocked in, 2 = clock switch
        :return:
        """
        logger.debug('clock_in_button_state message: %s' % message)
        # A value of None for message means that there is not clock-out time and the sheet is still active.
        self.ui.clock_button.setStyleSheet('background-image: url(:/lights buttons/elements/'
                                           'clock_button_%i.png);'
                                           'background-repeat: none;'
                                           'background-color: rgba(0, 0, 0, 0);'
                                           'border-color: rgba(0, 0, 0, 0);' % message)
        if message >= 1:
            # Let the engine know that it is clocked in.
            # FIXME: Add an emit here as well, to let the engine know it's clocked in.
            self.clocked_in = True
            self.time_lord.time_signal.user_clocked_in.emit(True)
            if message == 2:
                # message == 2, UI does not match timesheet
                try:
                    self.ui.clock_button.clicked.disconnect()
                except Exception:
                    pass
                self.ui.clock_button.clicked.connect(self.switch_time)
            else:
                # User is clocked in and the UI matches the Timesheet
                try:
                    self.ui.clock_button.clicked.disconnect()
                except Exception:
                    pass
                # Connect the Stop Time action.
                self.ui.clock_button.clicked.connect(self.stop_time)

        else:
            # Let the engine know that it is clocked out.
            self.clocked_in = False
            self.time_lord.time_signal.user_clocked_in.emit(False)
            try:
                self.ui.clock_button.clicked.disconnect()
            except Exception:
                pass
            logger.debug('Start Time being connected to the button...')
            self.ui.clock_button.clicked.connect(self.start_time)
            logger.debug('Button connected.')

    def update_latest_timesheet(self, timesheet=None):
        logger.info('Updating UI timesheet...')
        logger.debug('timesheet data... %s' % timesheet)
        if timesheet:
            # NOTE: The following changes got the updater to work... a little too much... perhaps.
            if type(timesheet) == dict and 'id' in timesheet.keys():
                if timesheet != self.latest_timesheet:
                    # Reinitialize the UI
                    logger.info('Reinitializing UI with updated timesheet...')
                    self.init_ui(received_timesheet=timesheet)
                    logger.info('Finishing local timesheet update...')
                    self.latest_timesheet = timesheet
                    logger.info('Timesheet updated! %s' % timesheet['id'])
                    logger.info('Updating runtime clock...')
                    self.time_engine.time_signal.get_running_clock.emit(timesheet)

    # --------------------------------------------------------------------------------------------------
    # Log handlers
    # --------------------------------------------------------------------------------------------------
    def log(self, message=None):
        if message:
            # print('LOG MESSAGE RECEIVED: %s' % message)
            logger.info(message)

    def debug(self, message=None):
        if message:
            # print('DEBUG MESSAGE RECEIVED: %s' % message)
            logger.debug(message)

    def error(self, message=None):
        if message:
            # print('ERROR MESSAGE RECEIVED: %s' % message)
            logger.error(message)

    def warning(self, message=None):
        if message:
            # print('WARNING MESSAGE RECEIVED: %s' % message)
            logger.warning(message)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('AdamBenson')
    app.setOrganizationDomain('adamdbenson.com')
    app.setApplicationName('TimeLord')
    splash_pix = QtGui.QPixmap('ui/resources/Time_Lord_Logo.png')
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()
    window = time_lord_ui()
    window.show()
    splash.finish(window)
    # sys.excepthook()  # TODO: Get this to work.
    sys.exit(app.exec_())


