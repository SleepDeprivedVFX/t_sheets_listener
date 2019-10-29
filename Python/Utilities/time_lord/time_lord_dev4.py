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
    req_daily_total = QtCore.Signal(str)
    set_daily_total = QtCore.Signal(float)
    req_weekly_total = QtCore.Signal(str)
    set_weekly_total = QtCore.Signal(float)

    # Update Signals
    update = QtCore.Signal(dict)
    req_project_update = QtCore.Signal(str)
    req_entity_update = QtCore.Signal(int)
    req_task_update = QtCore.Signal(dict)
    send_project_update = QtCore.Signal(dict)
    send_entity_update = QtCore.Signal(dict)
    send_task_update = QtCore.Signal(dict)
    # set_project_dropdown = QtCore.Signal(str)  # Obsolete
    # set_entity_dropdown = QtCore.Signal(str)  # Obsolete
    set_dropdown = QtCore.Signal(tuple)

    # Data Signals
    last_timesheet = QtCore.Signal(dict)
    user_clocked_in = QtCore.Signal(bool)
    send_timesheet = QtCore.Signal(dict)

    # Timesheet Action Signals
    clock_out_user = QtCore.Signal(dict)
    clock_in_user = QtCore.Signal(tuple)
    user_has_clocked_in = QtCore.Signal(dict)
    set_last_timesheet = QtCore.Signal(dict)


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
        self.time_lord = time_lord()

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
        Saves the last EventLogEntry and TimeLog to the time_capsule, allowing for checks of existing timesheets
        and preventing the processing of events more than once.
        :param data: (dict): A collection of 2 values:
                   data =   {
                                'EventLogID': 123,
                                'TimeLogID': 456
                            }
        :return: None
        '''
        if data:
            if os.path.exists(self.db_path):
                fh = open(self.db_path, 'wb')
                pickle.dump(data, fh)
                fh.close()

    def get_new_events(self):
        '''
        This method will collect the latest EventLogEntry from the Shotgun database.
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
                        # logger.debug('Events collected! %s' % events)
                        # print 'New Events Collected!', events
                        return events
                except (sgapi.ProtocolError, sgapi.ResponseError, socket.error) as err:
                    logger.warning('Shotgun API Failure.  Trying again... %s' % err)
                    conn_attempts += 1
                    time.sleep(1)
                    if conn_attempts > 10:
                        print 'can\'t connect to shotgun! %s' % err
                        logger.error('Can\'t connect to shotgun!', err)
                        break
                except Exception as err:
                    logger.warning('Unknown exception!  Trying again. %s' % err)
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
                                logger.debug('NEW RECORD! %s' % event)
                                # TODO: Add UI updater here.
                                print 'NEW RECORD!'
                                print 'event id: %s' % event['entity']['id']
                                print 'event: %s' % event
                                # FIXME: UPDATE_DATA: Apparently, I need data to input here.
                                #       This data would be the timesheet record just created.
                                #       The only thing I'm getting from the event is the following:
                                #       'entity':
                                # 		{
                                # 			'type': 'TimeLog',
                                # 			'id': 1265,
                                # 			'name': 'New Time Log'
                                # 		},
                            #         'project':
                            #             {
                            #                 'type': 'Project',
                            #                 'id': 547,
                            #                 'name': 'Admin'
                            #             },
                            #         'user':
                            #             {
                            #                 'type': 'HumanUser',
                            #                 'id': 41,
                            #                 'name': 'Adam Benson'
                            #             },
                                #       So, really I only get the project and the timesheet with the data I need.
                                #       Thus, I must have a routine that can collect that in formation for me from
                                #       the data provided.
                                timesheet = tl_time.get_timesheet_by_id(tid=event['entity']['id'])
                                ts_entity = sg_data.get_entity_from_task(task_id=timesheet['entity']['id'])

                                ts_data = {
                                    'project': timesheet['project']['name'],
                                    'project_id': timesheet['project']['id'],
                                    'entity': ts_entity['entity']['name'],
                                    'entity_id': ts_entity['entity']['id'],
                                    'task': timesheet['entity']['name'],
                                    'task_id': timesheet['entity']['id']
                                }
                                self.time_lord.time_signal.update.emit(ts_data)
                                self.time_lord.time_signal.last_timesheet.emit(timesheet)

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
        self.last_timesheet = tl_time.get_last_timesheet(user=user)

        # Signal Connections
        self.time_signal.update.connect(self.update_ui)
        self.time_signal.req_project_update.connect(self.send_project_update)
        self.time_signal.req_entity_update.connect(self.send_entity_update)
        self.time_signal.req_task_update.connect(self.send_task_update)

    def set_trt_output(self, trt=None):
        # logger.debug('Set TRT: %s' % trt)
        set_message = 'TRT: %s' % trt
        self.time_signal.trt_output.emit(set_message)

    def send_project_update(self, message=None):
        logger.debug('Collecting projects for return')
        projects = sg_data.get_active_projects()
        self.time_signal.send_project_update.emit(projects)

    def send_entity_update(self, proj_id=None):
        print 'send_entity_update: %s' % proj_id
        if proj_id:
            logger.debug('Project ID received by Entity Update Request: %s' % proj_id)

            asset_entities = sg_data.get_project_assets(proj_id=proj_id)
            logger.debug('Assets collected: %s' % asset_entities)
            # QUERY: I've noticed that it hung up here, between the two. Is this a consistent hangup?
            shot_entities = sg_data.get_project_shots(proj_id=proj_id)
            logger.debug('Shots Collected: %s' % shot_entities)
            entities = asset_entities + shot_entities
            self.time_signal.send_entity_update.emit(entities)

    def send_task_update(self, context=None):
        print 'Send tasks activated! %s' % context
        if context:
            print 'send_task_update context: %s' % context
            logger.debug('Task update requests. Context: %s' % context)

            entity_id = context['entity_id']
            entity_name = context['entity_name']
            proj_id = context['proj_id']
            print 'requesting tasks....'
            tasks = sg_data.get_entity_tasks(entity_id=entity_id, entity_name=entity_name, proj_id=proj_id)
            print 'tasks received: %s' % tasks
            if tasks:
                print 'Sending a signal...'
                self.time_signal.send_task_update.emit(tasks)
                print 'Task signal sent.'
                logger.debug('Tasks emitted: %s' % tasks)

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

    def update_ui(self, data=None):
        '''
        This is the place where heavier processes will be put together and then emitted to the appropriate
        UI slot.
        :param data: (dict) A collection of data from the UI or from the saved data.
        :return:
        '''
        # FIXME: The Update UI requires data FROM the UI.  No way to compare current values if I don't have them
        print 'Update Detected: %s' % data
        logger.debug('Signal Received: %s' % data)
        # Get the last timesheet for local use and emit it for use elsewhere.
        while not self.last_timesheet['project'] and not self.last_timesheet['entity']:
            print 'Timesheet was blank.  Getting it again...'
            self.last_timesheet = tl_time.get_last_timesheet(user=user)
        print 'update ui last_timesheet: %s' % self.last_timesheet
        self.time_signal.last_timesheet.emit(self.last_timesheet)

        # Collect Project/Entity/Task Data from Timesheet
        project = self.last_timesheet['project']['name']
        project_id = self.last_timesheet['project']['id']
        task = self.last_timesheet['entity']['name']
        task_id = self.last_timesheet['entity']['id']

        # Get Entity from task and project IDs
        entity_info = sg_data.get_entity_from_task(task_id=task_id)
        entity = entity_info['entity']['name']
        entity_id = entity_info['entity']['id']

        # Emit update signals.
        send_proj = ('project_dropdown', project)
        send_ent = ('entity_dropdown', entity)
        send_task = ('task_dropdown', task)
        self.time_signal.set_dropdown.emit(send_proj)
        self.time_signal.set_dropdown.emit(send_ent)
        self.time_signal.set_dropdown.emit(send_task)

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
    def __init__(self, parent=None):
        # super(time_lord_ui, self).__init__(parent=None)
        QtGui.QMainWindow.__init__(self, parent)

        # --------------------------------------------------------------------------------------------------------
        # Set the saved settings
        # --------------------------------------------------------------------------------------------------------
        # This saves all the last settings so that they return to their previous state when the program is run again.
        self.settings = QtCore.QSettings('AdamBenson', 'TimeLord')
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
        # Set main user info
        self.ui.artist_label.setText(user['name'])
        # Set the rollers
        # TODO: Make sure the date rollers are pulling from the Time Sheet as well
        now = datetime.now()
        d = now.strftime('%m-%d-%y')
        self.set_start_date_rollers(d=d)
        self.set_end_date_rollers(d=d)

        # Initialize the dropdowns
        self.init_ui()

        # --------------------------------------------------------------------------------------------------------
        # Signal Connections
        # --------------------------------------------------------------------------------------------------------
        # Clock function signals
        self.time_engine.time_signal.main_clock.connect(self.main_clock)
        self.time_engine.time_signal.in_clock.connect(self.set_in_clock)
        self.time_engine.time_signal.out_clock.connect(self.set_out_clock)

        # Update Connections
        self.time_lord.time_signal.send_project_update.connect(self.update_projects_dropdown)
        self.time_lord.time_signal.send_entity_update.connect(self.update_entity_dropdown)
        self.time_lord.time_signal.send_task_update.connect(self.update_task_dropdown)
        self.time_lord.time_signal.last_timesheet.connect(self.update_last_timesheet)
        # self.time_lord.time_signal.set_project_dropdown.connect(self.set_project_dropdown)  # Obsolete
        # self.time_lord.time_signal.set_entity_dropdown.connect(self.set_entity_dropdown)  #Obsolete
        self.time_lord.time_signal.set_dropdown.connect(self.set_dropdown)

        # Dropdown Change Index Connections
        self.ui.project_dropdown.currentIndexChanged.connect(self.req_update_entities)
        # Then change the button color to Yellow, Red or Green
        self.ui.project_dropdown.currentIndexChanged.connect(lambda: self.switch_state(self.last_timesheet))
        self.ui.entity_dropdown.currentIndexChanged.connect(self.req_update_tasks)
        self.ui.entity_dropdown.currentIndexChanged.connect(lambda: self.switch_state(self.last_timesheet))
        self.switch_state(self.last_timesheet)

        # Do First Update
        # FIXME: (Side-note.  I need to start creating issue codes and tagging them here, for example:)
        # FIXME: UPDATE_DATA: Apparently I need to add data here from the UI.
        #       This data would be from the UI.... or from the Saved Data!?
        data = {
            'project': self.saved_project,
            'project_id': self.saved_project_id,
            'entity': self.saved_entity,
            'entity_id': self.saved_entity_id,
            'task': self.saved_task,
            'task_id': self.saved_task_id
        }
        self.time_lord.time_signal.update.emit(data)

        # Start the engines
        self.time_engine.start()
        self.time_machine.start()

    def init_ui(self):
        '''
        This may actually need to pull some data from Shotgun directly.  That's ok, since it only runs
        once at the onset.
        The idea is that this routine will set the initial values from the saved settings.
        :return: None
        '''
        # NOTE: I may have to remove the __init__ call to self.time_lord.time_signal.update.emit()
        projects = sg_data.get_active_projects()
        if projects:
            # Update the dropdown list
            self.update_projects_dropdown(projects)
            proj_id = self.ui.project_dropdown.itemData(self.ui.project_dropdown.currentIndex())

            # Collect Entities
            assets = sg_data.get_project_assets(proj_id=proj_id)
            shots = sg_data.get_project_shots(proj_id=proj_id)
            entities = assets + shots

            # Update the Entities dropdown
            self.update_entity_dropdown(entities=entities)
            entity = self.ui.entity_dropdown.currentText()
            entity_id = self.ui.entity_dropdown.itemData(self.ui.entity_dropdown.currentIndex())

            # Collect Tasks
            tasks = sg_data.get_entity_tasks(entity_id=entity_id, entity_name=entity, proj_id=proj_id)
            self.update_task_dropdown(tasks=tasks)

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
        '''
        First checks to see if the dropdowns match the current timesheet. Set match = False if not.

        :param data: (dict) A timesheet log item
        :return: None
        '''
        print 'Switch States: %s' % data
        logger.debug('Switch state triggered')
        match = True

        selected_proj = self.ui.project_dropdown.currentText()

        # Check that the project matches
        # NOTE: I need a way to make sure the current timesheet and the saved data are always the same
        if selected_proj != self.saved_project:
            logger.debug('Last project name does not match.')
            match = False

        # I get the entity, because it does not come with last_timesheet data
        if self.saved_entity != self.ui.entity_dropdown.currentText():
            logger.debug('The entity does not match the dropdown.')
            match = False

        if self.saved_task != self.ui.task_dropdown.currentText():
            logger.debug('Tasks aren\'t cool.')
            match = False
        logger.debug('Finished with match check: %s' % match)

        if match and self.clocked_in:
            logger.debug('match and timelord clocked in.  Emit 1')
            self.time_lord.time_signal.clock_state.emit(1)
            try:
                self.ui.clock_button.clicked.disconnect(self.start_time)
            except:
                pass
            try:
                self.ui.clock_button.clicked.disconnect(self.switch_time)
            except:
                pass
            self.ui.clock_button.clicked.connect(self.stop_time)
        elif not match and self.clocked_in:
            logger.debug('Not matched and timelord clocked in.  Emit 2')
            self.time_lord.time_signal.clock_state.emit(2)
            try:
                self.ui.clock_button.clicked.disconnect(self.start_time)
            except:
                pass
            try:
                self.ui.clock_button.clicked.disconnect(self.stop_time)
            except:
                pass
            self.ui.clock_button.clicked.connect(self.switch_time)
        elif not self.clocked_in:
            logger.debug('Timelord not clocked in.  Doesn\'t matter if it\'s matched.  Emit 0')
            self.time_lord.time_signal.clock_state.emit(0)
            try:
                self.ui.clock_button.clicked.disconnect(self.stop_time)
            except:
                pass
            try:
                self.ui.clock_button.clicked.disconnect(self.switch_time)
            except:
                pass
            self.ui.clock_button.clicked.connect(self.start_time)
        # self.time_lord.time_signal.set_last_timesheet.emit('Update')

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
        # TODO: Add features that start other processes as well.  Change the button connections, et cetera
        self.time_lord.clocked_in = True
        self.time_lord.kill_it = False
        self.update_saved_settings()
        # TODO: Add check to see if the service is already running first
        # if not self.time_lord.clocked_in:
        #     self.clock_in()
        self.clock_in()
        self.time_lord.start()

    def stop_time(self):
        self.time_lord.clocked_in = False
        self.time_lord.kill_it = True
        self.update_saved_settings()
        self.clock_out()

    def switch_time(self):
        if self.selection_check():
            self.time_lord.clocked_in = False
            self.update_saved_settings()
            self.clock_out()
            self.clock_in()
            if not self.time_machine.isRunning():
                self.time_machine.start()

    def clock_out(self):
        self.time_lord.time_signal.clock_state.emit(0)
        self.time_lord.time_signal.req_daily_total.emit('Update!')
        self.time_lord.time_signal.req_weekly_total.emit('Update!')
        self.time_lord.time_signal.clock_out_user.emit(self.last_timesheet)

    def clock_in(self, message=None):
        # Check to see if the UI settings are valid for a new timesheet.
        if not self.selection_check():
            # The settings are invalid.  Kick it back.
            return False

        # Emit the Steady State green light signal, and update the output monitor.
        self.time_lord.time_signal.clock_state.emit(1)
        # TODO: Turn the lower_output into a stream handler.
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
        if not self.time_machine.isRunning():
            self.time_machine.start()

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

    # def set_project_dropdown(self, proj=None):
    #     '''
    #     Sets the current index of the project dropdown
    #     :param proj:
    #     :return:
    #     '''
    #     if proj:
    #         current = self.ui.project_dropdown.currentText()
    #         if proj != current:
    #             self.ui.project_dropdown.setCurrentIndex(
    #                 self.ui.project_dropdown.findText(proj)
    #             )
    #
    # def set_entity_dropdown(self, entity=None):
    #     if entity:
    #         current = self.ui.entity_dropdown.currentText()
    #         if entity:
    #             pass

    def set_dropdown(self, data=None):
        if data:
            dd_type = data[0]
            dd_value = data[1]
        else:
            dd_value = None
            dd_type = None
        if dd_type and dd_value:
            widge = self.findChild(QtGui.QComboBox, dd_type)
            print('widge found: %s' % widge)
            if widge:
                new_index = widge.findText(dd_value)
                print('widge index: %s' % new_index)
                if new_index:
                    widge.setCurrentIndex(new_index)
                    print('widge set')
            # if widget:
            #     widget.setCurrentText(dd_value)

    # ----------------------------------------------------------------------------------------------------------------
    # UI Events - Close, Update Saved Settings, Update UI Data
    # ----------------------------------------------------------------------------------------------------------------
    def closeEvent(self, *args, **kwargs):
        self.update_saved_settings()
        self.time_machine.kill_it = True
        self.time_engine.kill_it = True
        if self.time_machine.isRunning():
            self.time_machine.kill()
        if self.time_engine.isRunning():
            self.time_engine.kill()

    def update_saved_settings(self):
        '''
        The settings that are saved after the window is closed.
        :return:
        '''
        self.settings.setValue('project', self.ui.project_dropdown.currentText())
        self.settings.setValue('project_id', self.ui.project_dropdown.itemData(self.ui.project_dropdown.currentIndex()))
        self.settings.setValue('entity', self.ui.entity_dropdown.currentText())
        self.settings.setValue('entity_id', self.ui.entity_dropdown.itemData(self.ui.entity_dropdown.currentIndex()))
        self.settings.setValue('task', self.ui.task_dropdown.currentText())
        self.settings.setValue('task_id', self.ui.task_dropdown.itemData(self.ui.task_dropdown.currentIndex()))
        self.settings.setValue('geometry', self.saveGeometry())

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
            print('IS CLOCKED IN: %s' % self.clocked_in)
            print('Testing last timesheet: %s' % self.last_timesheet)

    # ----------------------------------------------------------------------------------------------------------------
    # Timesheet Data Updaters - Set the project, entity and task drop downs.
    # ----------------------------------------------------------------------------------------------------------------
    def update_projects_dropdown(self, projects=None):
        # Clear out the projects so that we are not double adding entries.
        print 'Update projects dropdown...'
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
        print 'triggering tasks dropdown reset...'
        self.update_task_dropdown()

    def req_update_entities(self, message=None):
        '''
        This function will trigger another function that will update_entities.  The reason for this (instead of going
        directly to update_entities) is that update_entities requires more elaborate data than a
        currentIndexChanged.connect() event can support.
        :param message: String trigger.  Does nothing.
        :return:
        '''
        print 'req_update_entities: %s' % message
        proj_id = self.ui.project_dropdown.itemData(self.ui.project_dropdown.currentIndex())
        self.time_lord.time_signal.req_entity_update.emit(proj_id)
        self.update_task_dropdown()

    def update_entity_dropdown(self, entities=None):
        '''
        Processes data from a Shotgun Assets and Shots entity collection.
        :param entities: (dict) A combined dictionary from 2 queries
        :return: None
        '''
        print 'update entity dropdown signal %s' % entities
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
        '''
        This method askes for a regular update from an onChangeEvent with no data
        :param message:
        :return:
        '''
        print 'Request Update Tasks activated.'
        ent_id = self.ui.entity_dropdown.itemData(self.ui.entity_dropdown.currentIndex())
        ent_name = self.ui.entity_dropdown.currentText()
        proj_index = self.ui.project_dropdown.currentIndex()

        context = {
            'entity_id': ent_id,
            'entity_name': ent_name,
            'proj_id': self.ui.project_dropdown.itemData(proj_index)
        }
        print 'sending the req_task_update: %s' % context
        self.time_lord.time_signal.req_task_update.emit(context)
        print 'Done sending task context.'

    def update_task_dropdown(self, tasks=None):
        print 'update_task_dropdown message received: %s' % tasks
        logger.debug('Setting tasks...')
        logger.debug(tasks)
        if tasks:
            self.ui.task_dropdown.clear()
            self.ui.task_dropdown.addItem('Select Task', 0)
            for task in tasks:
                self.ui.task_dropdown.addItem(task['content'], task['id'])
        else:
            self.ui.task_dropdown.clear()
            self.ui.task_dropdown.addItem('Select Task', 0)
        if self.saved_task != self.last_timesheet['entity']['name']:
            self.saved_task = self.last_timesheet['entity']['name']
        task_index = self.ui.task_dropdown.findText(self.saved_task)
        if task_index >= 0:
            self.ui.task_dropdown.setCurrentIndex(task_index)
        # Lastly, connect the Task to an on-change event
        self.ui.task_dropdown.currentIndexChanged.connect(self.switch_state)
        self.switch_tasks()

    def switch_tasks(self):
        # QUERY: DO I need have the __init__ call the switch tasks? Or do I use a different method up there?
        #       The fear is that the saved_task might not accurately reflect what's going on, due to signal and
        #       slot delays.
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
        '''
        Eventually, this should return a user set start time from the UI.  Not sure right off hand yet how to do that.
        :return:
        '''
        return None

    def clock_in_button_state(self, message=None):
        # FIXME: This is getting called twice, one right after another.
        '''
        Takes an integer value between 0 and 2
        :param message: (int) 0 = clocked out, 1 = clocked in, 2 = clock switch
        :return:
        '''
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
            if message == 2:
                try:
                    self.ui.clock_button.clicked.disconnect(self.start_time)
                except Exception:
                    pass
                try:
                    self.ui.clock_button.clicked.disconnect(self.stop_time)
                except Exception:
                    pass
                self.ui.clock_button.clicked.connect(self.switch_time)
            else:
                try:
                    # Disconnect the start time action
                    self.ui.clock_button.clicked.disconnect(self.start_time)
                except Exception:
                    pass
                try:
                    # Disconnect the switch time action
                    self.ui.clock_button.clicked.disconnect(self.switch_time)
                except Exception:
                    pass
                # Connect the Stop Time action.
                self.ui.clock_button.clicked.connect(self.stop_time)

        else:
            # Let the engine know that it is clocked out.
            self.time_lord.clocked_in = False
            try:
                self.ui.clock_button.clicked.disconnect(self.stop_time)
            except Exception:
                pass
            try:
                self.ui.clock_button.clicked.disconnect(self.switch_time)
            except Exception:
                pass
            self.ui.clock_button.clicked.connect(self.start_time)

    def update_last_timesheet(self, timesheet=None):
        print 'updating last timesheet... %s' % timesheet
        if timesheet:
            self.last_timesheet = timesheet


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


