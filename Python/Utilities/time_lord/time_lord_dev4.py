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
from ui import time_lord_clock as tlu
import time
import socket

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


class time_signals(QtCore.QObject):
    # Logger Signals
    log = QtCore.Signal(str)
    error = QtCore.Signal(str)
    debug = QtCore.Signal(str)
    # End Thread Signals
    kill_signal = QtCore.Signal(bool)

    # Time Signals / Clock Faces
    main_clock = QtCore.Signal(tuple)
    in_clock = QtCore.Signal(tuple)
    out_clock = QtCore.Signal(tuple)
    in_date = QtCore.Signal(str)
    out_date = QtCore.Signal(str)
    running_clock = QtCore.Signal(str)

    # Monitor Output Signals
    trt_output = QtCore.Signal(str)
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
    update_clock = QtCore.Signal(str)
    req_daily_total = QtCore.Signal(str)
    set_daily_total = QtCore.Signal(float)
    req_weekly_total = QtCore.Signal(str)
    set_weekly_total = QtCore.Signal(float)


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
        self.kill_it = False
        self.kill_signal = self.time_signal.kill_signal.connect(self.kill)
        self.tick = QtCore.QTime.currentTime()

    def kill(self):
        self.kill_it = True

    def run(self, *args, **kwargs):
        self.chronograph()

    def chronograph(self):
        second = int(datetime.now().second)
        minute = datetime.now().minute

        while not self.kill_it:
            if int(datetime.now().second) != second:
                # Set the clocks
                second = int(datetime.now().second)
                self.tick = QtCore.QTime.currentTime()
                hours = (30 * (self.tick.hour() + (self.tick.minute() / 60.0)))
                minutes = (6 * (self.tick.minute() + (self.tick.second() / 60.0)))
                time = (hours, minutes)
                self.time_signal.main_clock.emit(time)
                self.time_signal.in_clock.emit(time)
                self.time_signal.out_clock.emit(time)
                # NOTE: I really probably should put the TRT clock in this mix too. I just don't want it to burden the
                #       normal flow of clock time with a heavy sg_query.

                if datetime.now().minute != minute:
                    daily_total = tl_time.get_daily_total(user=user, lunch_id=int(lunch_task['id']))
                    weekly_total = tl_time.get_weekly_total(user=user, lunch_id=int(lunch_task['id']))
                    minute = datetime.now().minute
                    if daily_total:
                        self.time_signal.daily_total.emit(daily_total)
                    if weekly_total:
                        self.time_signal.weekly_total.emit(weekly_total)


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

    def run(self, *args, **kwargs):
        self.listener()

    def kill(self):
        self.kill_it = True

    def get_time_capsule(self):
        '''
        This will open and collect the current time capsule file.
        :return:
        '''
        if os.path.exists(self.db_path):
            fh = open(self.db_path, 'rb')
            db_file = pickle.load(fh)
            fh.close()
            return db_file

    def save_time_capsule(self, data={}):
        '''
        Do I return a packaged data dictionary, or do I build it here, passing the Event and TimeLog IDs into the
        system?  Or do I collect those values in here, passing nothing?
        :param data: (dict): A collection of 2 values:
                   data =   {
                                'EventLogID': 123,
                                'TimeLogID': 456
                            }
        :return:
        '''
        if data:
            if os.path.exists(self.db_path):
                fh = open(self.db_path, 'wb')
                pickle.dump(data, fh)
                fh.close()

    def get_new_events(self):
        '''
        This method will collect the latest events from the Shotgun database
        :return: A list of new events
        '''
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
                    'direction': 'asc'
                }
            ]

            conn_attempts = 0
            while True:
                # print 'conn_attempts: %s' % conn_attempts
                try:
                    events = sg.find('EventLogEntry', filters, fields, order=order, limit=200)
                    # print 'found events: %s' % events
                    if events:
                        logger.debug('Events collected! %s' % events)
                        # print 'New Events Collected!', events
                    return events
                except (sgapi.ProtocolError, sgapi.ResponseError, socket.error) as err:
                    conn_attempts += 1
                    time.sleep(1)
                    if conn_attempts > 10:
                        print 'can\'t connect to shotgun! %s' % err
                        logger.error('Can\'t connect to shotgun!', err)
                        break
                except Exception as err:
                    conn_attempts += 1
                    time.sleep(1)
                    if conn_attempts > 10:
                        logger.error('Something went wrong! %s' % err)
        return []

    def listener(self):
        '''
        The main loop listener.
        :return:
        '''
        logger.debug('Starting the main event listener loop...')
        print 'Loop Started'
        while not self.kill_it:
            events = self.get_new_events()
            time_capsule = self.get_time_capsule()
            # print 'returned events: %s' % events
            if events:
                for event in events:
                    if event['entity']['id'] >= time_capsule['TimeLogID'] and event['id'] > time_capsule['EventLogID']:
                        entity = event['entity']
                        entity_id = entity['id']
                        timesheet_info = tl_time.get_timesheet_by_id(tid=entity_id)
                        if timesheet_info:
                            user_info = timesheet_info['user']
                            user_id = user_info['id']
                            if user_id == user['id']:
                                # TODO: Add UI updater here.
                                print 'NEW RECORD!'
                                print event['entity']['id']
                                print event

                                data = {
                                    'EventLogID': event['id'],
                                    'TimeLogID': event['entity']['id']
                                }
                                self.save_time_capsule(data)


# ------------------------------------------------------------------------------------------------------
# Primary Tools
# ------------------------------------------------------------------------------------------------------
class time_lord(QtCore.QObject):
    '''
    The Time Lord method is the main set of tools for updating the UI and processing events.
    It is not threaded or timed, but simply runs commands when called.
    Signals will be picked up by this and processes will then emit the needed data back to the UI
    '''
    # TODO: Check through all of this and make sure all the signals work!
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.time_signal = time_signals()
        self.kill_it = False
        self.clocked_in = False
        self.error_state = False
        self.steady_state = True

    def set_trt_output(self, trt=None):
        # logger.debug('Set TRT: %s' % trt)
        set_message = 'TRT: %s' % trt
        self.time_signal.trt_output.emit(set_message)

    def req_start_end_output(self):
        last_timesheet = tl_time.get_last_timesheet(user=user)
        last_in_time = last_timesheet['sg_task_start']
        last_out_time = last_timesheet['sg_task_end']

        start = '%s %s' % (last_in_time.date(), last_in_time.time())
        if last_out_time:
            end = '%s %s' % (last_out_time.date(), last_out_time.time())
        else:
            end = '%s %s' % (datetime.now().date(), datetime.now().time())

        # Take the initial values and set their outputs.
        self.set_start_end_output(start=start, end=end)

    def set_start_end_output(self, start=None, end=None):
        set_message = 'Start: %s\nEnd: %s' % (start, end)
        self.time_signal.start_end_output.emit(set_message)

    def set_user_output(self, user=None):
        if self.clocked_in:
            in_out = 'IN'
        else:
            in_out = 'OUT'
        set_message = '%s CLOCKED %s' % (user['name'], in_out)
        self.time_signal.user_output.emit(set_message)

    def set_daily_output(self, daily=None):
        '''
        Creates a message for the output monitor and emits a signal.
        :param daily: (float) Total of hours currently worked.
        :return: daily_output.emit()
        '''
        set_message = 'Daily Total: %0.2f Hours' % daily
        self.time_signal.daily_output.emit(set_message)

    def set_weekly_output(self, weekly=None):
        set_message = 'Weekly Total: %0.2f Hours' % weekly
        self.time_signal.weekly_output.emit(set_message)

    def update_ui(self, update=None):
        logger.debug('update_ui receives: %s' % update)
        if update:
            ui_task_id = update['task_id']

            try:
                latest_timesheet = tl_time.get_last_timesheet(user=user)
            except TypeError, e:
                latest_timesheet = None
                logger.warning('Timesheet failed to update: %s' % e)
                return False
            if latest_timesheet:
                try:
                    # ts_id = latest_timesheet['id']
                    project = latest_timesheet['project']['name']
                    project_id = latest_timesheet['project']['id']
                    task = latest_timesheet['entity']['name']
                    task_id = latest_timesheet['entity']['id']
                except Exception, e:
                    logger.warning('Failed to get latest timesheet! %s' % e)
                    return None
                if task_id != ui_task_id:
                    logger.debug('Wrong time sheet!!!')
                    # TODO: Send signals that update the UI bits.
                    new_timesheet = {
                        'project': project,
                        'project_id': project_id,
                        'task_id': task_id,
                        'task': task
                    }
                    # Get the entity from the task and append it to the new_timesheet
                    try:
                        get_entity = sg_data.get_entity_from_task(task_id)
                        if get_entity:
                            entity = get_entity['entity']['name']
                            entity_id = get_entity['entity']['id']
                            new_timesheet['entity'] = entity
                            new_timesheet['entity_id'] = entity_id
                            # Send the new_timesheet to the updater.
                            self.time_signal.ui_return.emit(new_timesheet)
                    except KeyError, e:
                        logger.warning('Bad entity: %s' % e)

                else:
                    logger.debug('Timesheet is copacetic')

    def quick_update(self):
        '''
        First function to get called by the UI __init__.
        Updates the current timesheet and emits it back to the UI
        :return: self.time_signal.send_timesheet.emit(new_timesheet)
        '''
        logger.debug('Communication received.  Updating....')
        new_timesheet = tl_time.get_last_timesheet(user=user)
        if new_timesheet:
            logger.debug('Timesheet collected!')
            self.time_signal.send_timesheet.emit(new_timesheet)
            self.last_timesheet = new_timesheet

    def get_active_projects(self, message=None):
        if message:
            logger.debug('Project List Requested!')
            active_projects = sg_data.get_active_projects()
            if active_projects:
                # wait_cond.wakeAll()
                if message == 'initialize':
                    return active_projects
                else:
                    self.time_signal.set_project_list.emit(active_projects)
                    self.quick_update()

    def set_daily_total(self, message=None):
        '''
        Sets and emits the Daily Total function back to the UI
        :param message: A string of any kind to kick start the process and trigger a log
        :return:
        '''
        logger.debug('set daily total: %s' % message)
        daily_total = None
        if message:
            # QUERY: Does this belong here?  Is this what's hanging up the program?
            daily_total = tl_time.get_daily_total(user=user, lunch_id=int(lunch_task['id']))
            if daily_total or daily_total >= 0.0:
                logger.debug('Daily total!: %s' % daily_total)
                self.time_signal.daily_total.emit(daily_total)
                logger.debug('Daily total emitted')
        return daily_total

    def set_weekly_total(self, message=None):
        # Sets and emiits the Weekly Total function back to the UI
        weekly_total = None
        if message:
            weekly_total = tl_time.get_weekly_total(user=user, lunch_id=int(lunch_task['id']))
            if weekly_total or weekly_total >= 0.0:
                self.time_signal.weekly_total.emit(weekly_total)
                logger.debug('Weekly total emitted')
        return weekly_total

    def clock_out_user(self, last_timesheet=None):
        if last_timesheet:
            tl_time.clock_out_time_sheet(timesheet=last_timesheet, clock_out=datetime.now())
            self.time_signal.lower_output.emit('You have clocked out!')
            ts_start = last_timesheet['sg_task_start']
            start_date = ts_start.strftime('%m-%d-%y')
            self.time_signal.in_date.emit(start_date)
            try:
                start = '%s %s' % (last_timesheet['sg_task_start'].date(),
                                   last_timesheet['sg_task_start'].time())
                end = '%s %s' % (last_timesheet['sg_task_end'].date(),
                                 last_timesheet['sg_task_end'].time())
                self.set_start_end_output(start=start, end=end)
            except (AttributeError, KeyError), e:
                logger.warning('Couldn\'t update the start and end times! %s' % e)
            daily_total = self.set_daily_total('Get')
            weekly_total = self.set_weekly_total('Get')
            self.set_trt_output(trt='00:00:00')
            self.set_user_output(user=user)
            self.set_daily_output(daily=daily_total)
            self.set_weekly_output(weekly=weekly_total)
            self.time_signal.update_timesheet.emit('Update')

    def clock_in_user(self, data=None):
        '''
        This may need some addition inputs, but for now... nothing.
        :return:
        '''
        if data:
            self.clocked_in = True
            context = data[0]
            start_time = data[1]
            timesheet = tl_time.create_new_timesheet(user=user, context=context, start_time=start_time)
            self.set_user_output(user=user)
            self.time_signal.user_has_clocked_in.emit(timesheet)

    def get_entities(self, entity_id=None, r=False):
        logger.debug('get_entities activated: entity id: %s' % entity_id)
        if entity_id:
            asset_entities = sg_data.get_project_assets(proj_id=entity_id)
            logger.debug('Assets collected: %s' % asset_entities)
            shot_entities = sg_data.get_project_shots(proj_id=entity_id)
            logger.debug('Shots Collected: %s' % shot_entities)
            entities = asset_entities + shot_entities
            last_timesheet = tl_time.get_last_timesheet(user=user)
            if r:
                return last_timesheet, entities
            else:
                self.time_signal.set_entity_list.emit((last_timesheet, entities))
            logger.debug('get_entities: %s' % entities)

    def get_tasks(self, context=None, r=False):
        logger.debug('get_tasks activated: %s' % context)
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
                logger.debug('Tasks emitted: %s' % tasks)

    def set_last_timesheet(self, message=None):
        if message:
            timesheet = tl_time.get_last_timesheet(user=user)
            self.time_signal.send_timesheet.emit(timesheet)
            time.sleep(0.1)
            self.time_signal.user_has_clocked_in.emit(timesheet)


# ------------------------------------------------------------------------------------------------------
# User Interface
# ------------------------------------------------------------------------------------------------------
class time_lord_ui(QtGui.QMainWindow):
    def __init__(self):
        super(time_lord_ui, self).__init__(parent=None)

        # --------------------------------------------------------------------------------------------------------
        # Set the saved settings
        # --------------------------------------------------------------------------------------------------------
        # This saves all the last settings so that they return to their previous state when the program is run again.
        self.settings = QtCore.QSettings('AdamBenson', 'TimeLord')
        self.last_saved_project = self.settings.value('last_project', '.')
        self.last_saved_entity = self.settings.value('last_entity', '.')
        self.last_saved_task = self.settings.value('last_task', '.')
        self.window_position = self.settings.value('geometry', '')
        self.restoreGeometry(self.window_position)

        # --------------------------------------------------------------------------------------------------------
        # Setup Time Engine
        # --------------------------------------------------------------------------------------------------------
        # Setup and connect the last timesheet.
        # Declare Class Variables
        self.last_timesheet = tl_time.get_last_timesheet(user=user)
        self.clocked_in = True

        # Connect to the threads
        self.time_lord = time_lord()
        self.time_engine = time_engine()
        self.time_machine = time_machine()

        # --------------------------------------------------------------------------------------------------------
        # Setup UI
        # --------------------------------------------------------------------------------------------------------
        self.ui = tlu.Ui_TimeLord()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
        self.window_on_top_tested = False
        self.set_window_on_top()

        # --------------------------------------------------------------------------------------------------------
        # Signal Connections
        # --------------------------------------------------------------------------------------------------------
        # Clock function signals
        self.time_engine.time_signal.main_clock.connect(self.main_clock)
        self.time_engine.time_signal.in_clock.connect(self.set_in_clock)
        self.time_engine.time_signal.out_clock.connect(self.set_out_clock)
        self.time_lord.time_signal.update_clock.connect(self.update_from_ui)

        # Start the engines
        self.time_engine.start()
        self.time_machine.start()

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

    def set_in_clock(self, in_time):
        '''
        This will check if the user is clocked in or not, and then set the clock accordingly.
        If they are clocked in, display clock in time.  Otherwise, display current time.
        Where it gets tricky is introducing a user set time.  i.e. user changes the time.
        TODO: Figure out the user set time interruption.
        :param in_time: (tuple) (hour, minute)
        :return:
        '''
        # NOTE: Occasionally, I'm getting a blank timesheet (randomly).  This is checking for that, but ultimately is
        #       a bandaid for some other issue, and it slows down the system.
        # if not self.last_timesheet['project'] or not self.last_timesheet['entity'] or \
        #         self.last_timesheet['sg_task_start']:
        #     self.last_timesheet = tl_time.get_last_timesheet(user=user)
        # if self.time_lord.clocked_in:
        # FIXME: The following if is a patch for the above shit.
        #       This seems to be what was causing one of the hang ups. Need a signal pass between here and there
        #       to set the self.clocked_in across both systems.
        if self.clocked_in:
            start_time = self.last_timesheet['sg_task_start']
            if start_time:
                hour = start_time.time().hour
                minute = start_time.time().minute
                second = start_time.time().second
                hours = (30 * (hour + (minute / 60.0)))
                minutes = (6 * (minute + (second / 60.0)))
            else:
                print 'Bad Start Time!  Returning False', datetime.now()
                logger.warning('Bad Start Time. Data lost somewhere.  Returning False.')
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
        '''
        This will check if the user is clocked in or not, and then set the clock accordingly.
        If they are clocked in, display clock in time.  Otherwise, display current time.
        Where it gets tricky is introducing a user set time.  i.e. user changes the time.
        TODO: Figure out the user set time interruption.
        :param in_time: (tuple) (hour, minute)
        :return:
        '''
        if not self.clocked_in:
            # self.last_timesheet = tl_time.get_last_timesheet(user=user)
            # self.timesheet_update.time_signal.ui_update.emit('Update!')
            # self.time_lord.time_signal.ui_update.emit()
            try:
                end_time = self.last_timesheet['sg_task_end']
                # NOTE: This is currently partially detecting that the thing is clocked out outside of the UI
                logger.debug('end_time: %s' % end_time)
                hour = end_time.time().hour
                minute = end_time.time().minute
                second = end_time.time().second
                hours = (30 * (hour + (minute / 60.0)))
                minutes = (6 * (minute + (second / 60.0)))
            except Exception, e:
                logger.error('The fit hit the shan: %s' % e)
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
        '''
        Sets the running time clock.
        :param t: (str) - While this is a number value, it must be exactly 6 digits long, thus string to maintain
                            the number of zeros needed for the default.
        :return: Running time.
        '''
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
        '''
        Sets the date rollers.
        :param d: (str) A MM-DD-YY date format string.
        :param which: (str) One of two acceptable values: 'start', 'end'
        :return:
        '''
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
            '''
            Sets the date rollers.
            :param d: (str) A MM-DD-YY date format string.
            :param which: (str) One of two acceptable values: 'start', 'end'
            :return:
            '''
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

    # ----------------------------------------------------------------------------------------------------------------
    # UI Events - Close, Update Saved Settings, Update UI Data
    # ----------------------------------------------------------------------------------------------------------------
    def closeEvent(self, *args, **kwargs):
        self.time_lord.kill_it = True
        self.time_engine.kill_it = True
        geometry = self.saveGeometry()
        self.settings.setValue('geometry', geometry)

    def update_saved_settings(self):
        '''
        The settings that are saved after the window is closed.
        :return:
        '''
        self.settings.setValue('last_project', self.ui.project_dropdown.currentText())
        self.settings.setValue('last_entity', self.ui.entity_dropdown.currentText())
        self.settings.setValue('last_task', self.ui.task_dropdown.currentText())
        self.settings.setValue('last_timesheet_id', self.ui.timesheet_id.text())

    def update_from_ui(self, message=None):
        '''
        This method may/should detect chenages outside of the UI. i.e. Drag-n-drop publisher, or a manual change in
        Shotgun.  Within 1 minute, this should change the UI to match the actual recorded time sheet.  Otherwise, shit
        can go all wrong.
        :param message: SIGNAL message.
        :return:
        '''
        # NOTE: I think, part of the problem is that I'm comparing the saved timesheet to a new timesheet record instead
        #       of comparing the UI values to the latest record.  THAT is what actually needs to happen. This can be
        #       based on the Timesheet ID#
        #       So, Do I even NEED to check the last_timesheet saved in memory?  I don't think so.
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
            print('~' * 60)
            print('IS CLOCKED IN: %s' % self.time_lord.clocked_in)
            print('Testing last timesheet: %s' % self.last_timesheet)


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



'''
The Following is pulled from the Event Listener system.  There's some good simple nuggets in there.  Parsing more...
_______________________________________________________________________________________________________________________
# This loop will trigger calls to new events and save heard calls to a database of some sort. More research needed...
        self.log.debug('Starting the event processing loop.')
        while self._continue:  # self._continue = True from the __init__()
            # Process events
            events = self._getNewEvents()  # This is the money maker.  This self._getNewEvents() gets the info I need
            for event in events:
                for collection in self._pluginCollections:  # This part doesn't apply to me.  Not processing events.
                    collection.process(event)
                self._saveEventIdData()  # This one is interesting.

            # if we're lagging behind Shotgun, we received a full batch of events
            # skip the sleep() call in this case
            if len(events) < self.config.getMaxEventBatchSize():
                try:
                    time.sleep(self._fetch_interval)
                except IOError:
                    time.sleep(5)

            # Reload plugins
            for collection in self._pluginCollections:
                collection.load()
                
            # Make sure that newly loaded events have proper state.
            self._loadEventIdData()

        self.log.debug('Shuting down event processing loop.')
-----------------------------------------------------------------------------------------------------------------------

# The Save Data routine from the loop above:
______________________________________________________________________________________________________________________

    def _saveEventIdData(self):
        """
        Save an event Id to persistant storage.

        Next time the engine is started it will try to read the event id from
        this location to know at which event it should start processing.
        """
        eventIdFile = self.config.getEventIdFile()  # This is the data file that is being saved to.
            # In the eventListener it's the: eventIdFile: C:/shotgun/shotgunEvents/shotgunEventDaemon.id from config
            # They're pickling the data somehow

        if eventIdFile is not None:
            for collection in self._pluginCollections:
                self._eventIdData[collection.path] = collection.getState()

            for colPath, state in self._eventIdData.items():
                if state:
                    try:
                        fh = open(eventIdFile, 'w')
                        pickle.dump(self._eventIdData, fh)
                        fh.close()
                    except OSError, err:
                        self.log.error('Can not write event id data to %s.\n\n%s', eventIdFile, traceback.format_exc(err))
                    break
            else:
                self.log.warning('No state was found. Not saving to disk.')
----------------------------------------------------------------------------------------------------------------------

# This opens and loads the afore mentioned file
______________________________________________________________________________________________________________________

    def _loadEventIdData(self):
        """
        Load the last processed event id from the disk

        If no event has ever been processed or if the eventIdFile has been
        deleted from disk, no id will be recoverable. In this case, we will try
        contacting Shotgun to get the latest event's id and we'll start
        processing from there.
        """
        eventIdFile = self.config.getEventIdFile()

        if eventIdFile and os.path.exists(eventIdFile):
            try:
                fh = open(eventIdFile)
                try:
                    self._eventIdData = pickle.load(fh)

                    # Provide event id info to the plugin collections. Once
                    # they've figured out what to do with it, ask them for their
                    # last processed id.
                    noStateCollections = []
                    for collection in self._pluginCollections:
                        state = self._eventIdData.get(collection.path)
                        if state:
                            collection.setState(state)
                        else:
                            noStateCollections.append(collection)

                    # If we don't have a state it means there's no match
                    # in the id file. First we'll search to see the latest id a
                    # matching plugin name has elsewhere in the id file. We do
                    # this as a fallback in case the plugins directory has been
                    # moved. If there's no match, use the latest event id 
                    # in Shotgun.
                    if noStateCollections:
                        maxPluginStates = {}
                        for collection in self._eventIdData.values():
                            for pluginName, pluginState in collection.items():
                                if pluginName in maxPluginStates.keys():
                                    if pluginState[0] > maxPluginStates[pluginName][0]:
                                        maxPluginStates[pluginName] = pluginState
                                else:
                                    maxPluginStates[pluginName] = pluginState

                        lastEventId = self._getLastEventIdFromDatabase()
                        for collection in noStateCollections:
                            state = collection.getState()
                            for pluginName in state.keys():
                                if pluginName in maxPluginStates.keys():
                                    state[pluginName] = maxPluginStates[pluginName]
                                else:
                                    state[pluginName] = lastEventId
                            collection.setState(state)

                except pickle.UnpicklingError:
                    fh.close()

                    # Backwards compatibility:
                    # Reopen the file to try to read an old-style int
                    fh = open(eventIdFile)
                    line = fh.readline().strip()
                    if line.isdigit():
                        # The _loadEventIdData got an old-style id file containing a single
                        # int which is the last id properly processed.
                        lastEventId = int(line)
                        self.log.debug('Read last event id (%d) from file.', lastEventId)
                        for collection in self._pluginCollections:
                            collection.setState(lastEventId)
                fh.close()
            except OSError, err:
                raise EventDaemonError('Could not load event id from file.\n\n%s' % traceback.format_exc(err))
        else:
            # No id file?
            # Get the event data from the database.
            lastEventId = self._getLastEventIdFromDatabase()
            if lastEventId:
                for collection in self._pluginCollections:
                    collection.setState(lastEventId)

            self._saveEventIdData()
'''

# db_path = os.path.join(sys.path[0], 'data_io/time_capsule.tld')  # .tld for time lord data
# if not os.path.exists(db_path):
#     os.makedirs(db_path)
# if os.path.exists(db_path):
#     data = {}
#     # Print out what's in the pickled file
#     db_file = open(db_path, 'rb')
#     print 'open file: %s' % db_file
#     # try:
#     test_db = pickle.load(db_file)
#     db_file.close()
#     print 'test_db returns: %s' % test_db
#
#     # The following takes existing data and adds it back into the pickled file.
#     # for k, v in test_db.items():
#     #     data[k] = v
#     db_file = open(db_path, 'wb')
#     data['EventLogID'] = 8184655
#     data['TimeLogID'] = 1149
#     pickle.dump(data, db_file)
#     db_file.close()



