"""
TIME LORD

Design and implementation are based around the Doctor Who character.  Everything
will be named accordingly.

This system is being designed to interact with Shotgun and any number of DCCs.
Here is a list of it's basic requirements:

    1. Replace T-Sheets with a user interface that allows artists to clock in and out of tasks in the same way.
    2. Integrate into Shotgun DCCs.  Detect files that are not currently clocked in, and (possibly) automatically
        update the time sheet with the data at hand.
    3. Be able to detect files put into an IAP (Internal Auto Publisher) and retroactively check time sheets against
        what the artist was clocked into.  For example:
            Artist drops a file into the system at 12:30.  The were not clocked in. System assumes a 10 am start time
            and clocks them in at 10 and continues counting forward or clocks out.
            Artist drops a a file into the system at 3:30.  The last file was at 12:30.  The system adjusts the clock
            to make the new file clock in at 12:30 and out at 3:30.
Without the need for doubling up the database in T-Sheets the new system should actually be much lighter, since it will
only be running simple shotgun commands on things.

NOTES:
    1. The user is always the main entry point.  No user, no time log.  Thus:
        a. The main UI running on someone's computer will take their login account to get the user
        b. The IAP account will get it's user data from the server upon drag-n-drop

REQUIREMENTS:
    1. This tool will most likely require ActiveState python to be installed on everyone's systems.

TODO:
    1. Have the thing auto-clock out if it detects a timesheet from the day before. aint_today()
        a. Get the latest time from the previous timesheet and add maybe 10 minutes?  (if the start time is before 7)
    3. Create a date-picker to set the start and end time clocks.
        a. If the thing is not clocked in
        b. If the user sets start and end times
        c. Make the button yellow
        d. Add a completed time sheet.  Append create_new_timesheet() to include an end_time parameter
    4. Setup a live stream feed for limited data to the lower output.  Like Bullgozer and Rollout Machine
    5. Fix drop down appearance.
    6. Figure out how to make this into an exe file, or some kind of other "run" function that hides the python
    8. Build in a rolling log file
    9. Have the start and end clocks do the following:
        a. If not clocked in...  hmmm. wait... I was going to say, if not clocked in, have it mirror the main time,
            but, perhaps it should only reflect the last in and out times?  Thus, those clocks don't usually move.
            However... if we want a user to clock in "now" then it should run the current time.  But, if the user
            pre-sets the time using the "set date-time" button, then that start time would hold (unless it conflicted
            with a previous entry.  Which brings about item...
    10. Have the clock in process ensure that the recorded in time is not prior to a previous out time.
    11. Setup A window hint for un-clocked in users.  Force on time while not clocked in.
"""

import shotgun_api3 as sgapi
import os
import sys
from PySide import QtGui, QtCore
import logging
from datetime import datetime

# Time Lord Libraries
from bin.time_continuum import continuum
from bin.companions import companions
from bin import configuration
from bin import shotgun_collect
from ui import time_lord_clock as tlu
import time

import inspect

config = configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
# TODO: Replace the following with a rolling timelog system.
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
fh = logging.FileHandler(filename=log_path)
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
tl_time = continuum(sg)

# Setup and get users
users = companions(sg)
user = users.get_user_from_computer()

# setup shotgun data connection
sg_data = shotgun_collect.sg_data(sg)

lunch_task = sg_data.get_lunch_task(lunch_proj_id=int(config['admin_proj_id']),
                                    task_name=config['lunch'])

# -----------------------------------------------------------------------------------------------------
# Setup WaitConditions and Mutex
# -----------------------------------------------------------------------------------------------------
wait_cond = QtCore.QWaitCondition()
mutex = QtCore.QMutex()


# ------------------------------------------------------------------------------------------------------
# Signal Emitters
# ------------------------------------------------------------------------------------------------------
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

    # Update Signals
    ui_update = QtCore.Signal(dict)
    ui_return = QtCore.Signal(dict)
    update_timesheet = QtCore.Signal(str)
    send_timesheet = QtCore.Signal(dict)

    # Timesheet Action Signals
    clock_out_user = QtCore.Signal(dict)
    clock_in_user = QtCore.Signal(tuple)
    user_has_clocked_in = QtCore.Signal(dict)
    set_last_timesheet = QtCore.Signal(dict)

    # UI Dropdown Signals
    req_project_list = QtCore.Signal(str)
    set_project_list = QtCore.Signal(dict)
    req_entity_list = QtCore.Signal(int)
    req_update_entities = QtCore.Signal(str)
    set_entity_list = QtCore.Signal(tuple)
    req_update_tasks = QtCore.Signal(str)
    req_task_list = QtCore.Signal(dict)
    set_task_list = QtCore.Signal(dict)


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

        # FIXME: The following block colorizes the output. It totally works, and then suddenly it
        #       locks up the memory and kills the machine.  I'm leaving the code here for the future.
        #       Error: Process finished with exit code -1073741819 (0xC0000005)
        # Colorize the Monitor Log Output. (Error messages, Debug logging, and Warnings)
        info = QtGui.QColor(130, 231, 130)
        error = QtGui.QColor(255, 0, 0)
        debug = QtGui.QColor(113, 113, 0)
        warning = QtGui.QColor(218, 145, 0)
        formatter = QtGui.QTextCharFormat()
        if level == 'ERROR':
            formatter.setForeground(error)
        elif level == 'DEBUG':
            formatter.setForeground(debug)
        elif level == 'WARNING':
            formatter.setForeground(warning)
        else:
            formatter.setForeground(info)
        self.edit.setCurrentCharFormat(formatter)

        # FIXME: Ok, the thing that sets up the stream handler to keep the latest entry first, either
        #       or also crashes the memory.
        #       Error: Process finished with exit code -1073741819 (0xC0000005)
        # Set the cursor to the top
        # cursor = QtGui.QTextCursor(self.edit.document())
        # cursor.setPosition(0)
        # self.edit.setTextCursor(cursor)
        # #
        # # # Insert Log
        # self.edit.insertPlainText('%s\n' % message)
        self.edit.appendPlainText('%s\n' % message)
        del formatter
        # del cursor


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
                    weekly_total = tl_time.get_weekly_total(user=user)
                    minute = datetime.now().minute
                    if daily_total:
                        self.time_signal.daily_total.emit(daily_total)
                    if weekly_total:
                        self.time_signal.weekly_total.emit(weekly_total)


# ------------------------------------------------------------------------------------------------------
# Primary Engine
# ------------------------------------------------------------------------------------------------------
class time_lord(QtCore.QThread):
    '''
    This engine runs most of the UI minus the clocks
    It sets TRT clocks, the Daily and Weekly output monitors and the Start & End output monitors.
    '''
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.time_signal = time_signals()
        self.kill_it = False
        self.clocked_in = False
        self.error_state = False
        self.steady_state = True
        self.kill_signal = self.time_signal.kill_signal.connect(self.kill)
        self.time_signal.ui_update.connect(self.update_ui)
        self.last_timesheet = tl_time.get_last_timesheet(user=user)
        self.time_signal.update_timesheet.connect(self.quick_update)

        # Update UI Signals
        self.time_signal.req_project_list.connect(self.get_active_projects)
        self.time_signal.req_daily_total.connect(self.set_daily_total)
        self.time_signal.req_weekly_total.connect(self.set_weekly_total)
        self.time_signal.req_entity_list.connect(self.get_entities)
        self.time_signal.req_task_list.connect(self.get_tasks)

        # Action Signals
        self.time_signal.clock_out_user.connect(self.clock_out_user)
        self.time_signal.clock_in_user.connect(self.clock_in_user)
        self.time_signal.set_last_timesheet.connect(self.set_last_timesheet)

    def kill(self):
        self.kill_it = True

    def run(self, *args, **kwargs):
        self.run_the_clock()

    def run_the_clock(self):
        # QUERY: Can I move all of this to the time engine, leaving only the functions below?
        # Start with getting the current minute and second.
        self.clocked_in = tl_time.is_user_clocked_in(user=user)

        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'self.clocked_in: %s' % self.clocked_in)
        second = int(datetime.now().second)
        minute = int(datetime.now().minute)
        # NOTE: The following 'while self.clocked_in' may be causing the issue where it doesn't update while not clocked
        #       in.  Do I need it?
        while self.clocked_in and not self.kill_it:
            # Make sure the loop only functions on a whole second
            if int(datetime.now().second) != second:
                second = int(datetime.now().second)
                # Features that function on whole minute intervals
                if int(datetime.now().minute) != minute:
                    # Send update to the last_timesheet in the UI
                    # NOTE: This new_timesheet system could probably be moved to the time_engine.
                    #       Unless the tl_time.get_last_timesheet() takes a long time to respond.
                    logger.info(datetime.now())
                    self.time_signal.lower_output.emit('Checking status...')
                    new_timesheet = tl_time.get_last_timesheet(user=user)
                    if new_timesheet:
                        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                              'Emitting new timesheet: %s' % new_timesheet)
                        self.time_signal.send_timesheet.emit(new_timesheet)
                        # TEST: Holding for 3 seconds
                        time.sleep(3)
                        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                              'Sent...')

                    # Send a signal to the Updater which will check that the UI currently matches the database
                    self.time_signal.update_clock.emit('Update')

                    # Test if the Latest Timesheet shows the user as clocked in, and set the global varianle accordingly
                    if not tl_time.is_user_clocked_in(user=user):
                        self.clocked_in = False
                    # set the current minute counter
                    minute = int(datetime.now().minute)

                # If the User is listed as "Clocked IN" by the latest timesheet...
                if self.clocked_in:
                    # Collect the current running time
                    rt = tl_time.get_running_time(timesheet=self.last_timesheet)
                    running_time = rt['rt']
                    # Here we take the running time and emit it to the display.
                    # QUERY: Should this move to the time_engine?
                    self.time_signal.running_clock.emit(running_time)
                    trt = '%s:%s:%s' % (rt['h'], rt['m'], rt['s'])
                    # Set the running time in the UI
                    self.set_trt_output(trt=trt)
                    start_time = self.last_timesheet['sg_task_start']
                    start = '%s' % (start_time.strftime('%Y-%m-%d %H:%M:%S'))
                    end = '%s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    self.set_start_end_output(start=start, end=end)

                    # Set the start time date rollers:
                    ts_start = self.last_timesheet['sg_task_start']
                    start_date = ts_start.strftime('%m-%d-%y')
                    self.time_signal.in_date.emit(start_date)
                else:
                    # NOTE: I feel like this should probably be doing way more things.
                    self.set_trt_output(trt='00:00:00')
                    break

    def set_trt_output(self, trt=None):
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
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'update_ui receives: %s' % update)
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
                except KeyError, e:
                    logger.warning('Failed to get latest timesheet! %s' % e)
                    return None
                # FIXME: I need to remove all of these time sheet ID bits and replace them with task ID
                if task_id != ui_task_id:
                    print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                          'Wrong time sheet!!!')
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
                    print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                          'Timesheet is copacetic')

    def quick_update(self):
        '''
        First function to get called by the UI __init__.
        Updates the current timesheet and emits it back to the UI
        :return: self.time_signal.send_timesheet.emit(new_timesheet)
        '''
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'Communication received.  Updating....')
        new_timesheet = tl_time.get_last_timesheet(user=user)
        if new_timesheet:
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'Timesheet collected!')
            self.time_signal.send_timesheet.emit(new_timesheet)
            self.last_timesheet = new_timesheet

    def get_active_projects(self, message=None):
        if message:
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'Project List Requested!')
            active_projects = sg_data.get_active_projects()
            if active_projects:
                wait_cond.wakeAll()
                self.time_signal.set_project_list.emit(active_projects)
                self.quick_update()

    def set_daily_total(self, message=None):
        '''
        Sets and emits the Daily Total function back to the UI
        :param message: A string of any kind to kick start the process and trigger a log
        :return:
        '''
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'set daily total: %s' % message)
        daily_total = None
        if message:
            # QUERY: Does this belong here?  Is this what's hanging up the program?
            daily_total = tl_time.get_daily_total(user=user, lunch_id=int(lunch_task['id']))
            if daily_total or daily_total >= 0.0:
                print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                      'Daily total!: %s' % daily_total)
                self.time_signal.daily_total.emit(daily_total)
                print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                      'Daily total emitted')
        return daily_total

    def set_weekly_total(self, message=None):
        # Sets and emiits the Weekly Total function back to the UI
        weekly_total = None
        if message:
            weekly_total = tl_time.get_weekly_total(user=user)
            if weekly_total or weekly_total >= 0.0:
                self.time_signal.weekly_total.emit(weekly_total)
                print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                      'Weekly total emitted')
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

    def get_entities(self, entity_id=None):
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'get_entities activated: entity id: %s' % entity_id)
        if entity_id:
            asset_entities = sg_data.get_project_assets(proj_id=entity_id)
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'Assets collected: %s' % asset_entities)
            shot_entities = sg_data.get_project_shots(proj_id=entity_id)
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'Shots Collected: %s' % shot_entities)
            entities = asset_entities + shot_entities
            last_timesheet = tl_time.get_last_timesheet(user=user)
            self.time_signal.set_entity_list.emit((last_timesheet, entities))
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'get_entities: %s' % entities)

    def get_tasks(self, context=None):
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'get_tasks activated: %s' % context)
        if context:
            entity_id = context['entity_id']
            entity_name = context['entity_name']
            proj_id = context['proj_id']
            tasks = sg_data.get_entity_tasks(entity_id=entity_id, entity_name=entity_name, proj_id=proj_id)
            if tasks:
                self.time_signal.set_task_list.emit(tasks)
                print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                      'Tasks emitted: %s' % tasks)

    def set_last_timesheet(self, message=None):
        if message:
            timesheet = tl_time.get_last_timesheet(user=user)
            self.time_signal.send_timesheet.emit(timesheet)
            time.sleep(0.1)
            self.time_signal.user_has_clocked_in.emit(timesheet)


class time_lord_ui(QtGui.QMainWindow):
    def __init__(self):
        '''
        Run the user interface.
        '''
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
        self.last_timesheet = None
        self.last_out_time = None
        self.last_in_time = None
        self.last_task_id = None
        self.last_project_name = None
        self.last_project_id = None
        self.last_entity_type = None
        self.last_entity_id = None

        # This connects to the two main threads plus the signals
        self.time_lord = time_lord()
        self.time_engine = time_engine()
        self.time_lord.start()
        self.time_engine.start()

        # Run the set_last_timesheet to populate the variables with the last timesheet for a given user.
        # This is the first emitted call
        self.time_lord.time_signal.update_timesheet.emit('Update')

        # --------------------------------------------------------------------------------------------------------
        # Setup UI
        # --------------------------------------------------------------------------------------------------------
        self.ui = tlu.Ui_TimeLord()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
        self.window_on_top_tested = False
        self.set_window_on_top()

        # --------------------------------------------------------------------------------------------------------
        # Setup Stream Handler
        # --------------------------------------------------------------------------------------------------------
        self.time_stream = time_stream()
        self.time_stream.edit = self.ui.lower_output
        logger.addHandler(self.time_stream)

        # --------------------------------------------------------------------------------------------------------
        # Signal Connections
        # --------------------------------------------------------------------------------------------------------
        # Timesheet signals
        self.time_lord.time_signal.send_timesheet.connect(self.update_last_timesheet)
        self.time_lord.time_signal.user_has_clocked_in.connect(self.set_last_timesheet)
        self.time_lord.time_signal.ui_return.connect(self.update_from_timesheet)

        # Clock function signals
        self.time_engine.time_signal.main_clock.connect(self.main_clock)
        self.time_engine.time_signal.in_clock.connect(self.set_in_clock)
        self.time_engine.time_signal.out_clock.connect(self.set_out_clock)
        self.time_lord.time_signal.update_clock.connect(self.update_from_ui)

        # Cumulative totals signals
        self.time_engine.time_signal.daily_total.connect(self.set_daily_total_needle)
        self.time_engine.time_signal.weekly_total.connect(self.set_weekly_total_needle)
        self.time_lord.time_signal.daily_output.connect(self.daily_output)
        self.time_lord.time_signal.weekly_output.connect(self.weekly_output)
        self.time_lord.time_signal.trt_output.connect(self.trt_output)
        self.time_lord.time_signal.running_clock.connect(self.set_runtime_clock)
        # This set daily total is on demand
        # self.time_lord.time_signal.set_daily_total.connect(self.set_daily_total_needle)

        # In and Out signals
        self.time_lord.time_signal.start_end_output.connect(self.start_end_output)
        self.time_lord.time_signal.in_date.connect(self.set_start_date_rollers)

        # Output Monitor Signals & State Buttons
        self.time_lord.time_signal.user_output.connect(self.user_output)
        self.time_lord.time_signal.lower_output.connect(self.lower_output)
        self.time_lord.time_signal.error_state.connect(self.error_state)
        self.time_lord.time_signal.steady_state.connect(self.steady_state)
        self.time_lord.time_signal.clock_state.connect(self.clock_in_button_state)

        # Drop Down Signals
        self.time_lord.time_signal.set_project_list.connect(self.set_project_list)
        self.time_lord.time_signal.set_entity_list.connect(self.update_entities)
        self.time_lord.time_signal.set_task_list.connect(self.update_tasks)

        # Button Signals
        self.time_lord.time_signal.button_state.connect(self.switch_state)

        # ------------------------------------------------------------------------------------------------------
        # Start up UI
        # ------------------------------------------------------------------------------------------------------
        self.time_lord.time_signal.req_project_list.emit('Update Projects!')
        # mutex.lock()
        # wait_cond.wait(mutex)
        # mutex.unlock()
        # First update the Entities: Assets and Shots
        # FIXME: The follwoing line needs to send the timesheet and list of entities as a tuple.  Needs to do something
        #       else with this.
        self.ui.project_dropdown.currentIndexChanged.connect(self.req_update_entities)
        # Then change the button color to Yellow, Red or Green
        self.ui.project_dropdown.currentIndexChanged.connect(self.switch_state)
        # Change the selection highlight to none
        self.ui.project_dropdown.setFocus()

        proj_index = self.ui.project_dropdown.currentIndex()
        self.time_lord.time_signal.req_entity_list.emit(self.ui.project_dropdown.itemData(proj_index))
        # Then connect the Entity drop-down to an on-change event
        self.ui.entity_dropdown.currentIndexChanged.connect(self.req_update_tasks)
        self.ui.entity_dropdown.currentIndexChanged.connect(self.switch_state)

        entity_index = self.ui.entity_dropdown.currentIndex()
        entity_id = self.ui.entity_dropdown.itemData(entity_index)
        entity_name = self.ui.entity_dropdown.currentText()

        self.last_saved_task = self.last_timesheet['entity']['name']
        context = {
            'entity_id': entity_id,
            'entity_name': entity_name,
            'proj_id': self.ui.project_dropdown.itemData(proj_index)
        }
        self.time_lord.time_signal.req_task_list.emit(context)

        # QUERY: Why am I setting time_lord variables in the UI?
        self.time_lord.set_trt_output(trt='00:00:00')
        self.time_lord.set_user_output(user=user)

        # # Set initial daily and weekly totals.
        self.time_lord.time_signal.req_daily_total.emit('Update')
        self.time_lord.time_signal.req_weekly_total.emit('Update')
    #
        # Set state buttons (The error and steady red and green lights.)
        if self.time_lord.error_state:
            self.error_state(True)
        else:
            self.error_state(False)

        if self.time_lord.steady_state:
            self.steady_state(True)
        else:
            self.steady_state(False)
    #
        # Set the rollers
        now = datetime.now()
        d = now.strftime('%m-%d-%y')
        self.set_start_date_rollers(d=d)
        self.set_end_date_rollers(d=d)

        # emit initial button
        self.time_lord.time_signal.button_state.emit('Update buttons')

        # Set main user info
        self.ui.artist_label.setText(user['name'])
        self.time_lord.time_signal.lower_output.emit('Startup complete!')

    # -----------------------------------------------------------------------------------------------------------------
    # Timesheet Data
    # -----------------------------------------------------------------------------------------------------------------
    def update_last_timesheet(self, update=None):
        """
        This function updates all of the last_* variables that hold the most recent data.  These variables can then be
        used elsewhere to make sure their own data is up-to-date.
        :param update: (dict) A timesheet object.
        :return: None - Saves global variables with new data.
        """
        if update:
            self.last_timesheet = update
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'UPDATE: %s' % update)
            self.last_project_name = self.last_timesheet['project']['name']
            self.last_saved_task = self.last_timesheet['entity']['name']
            self.last_task_id = self.last_timesheet['entity']['id']
            self.last_project_id = self.last_timesheet['project']['id']
            # NOTE: DIRECT CALL but takes less than a second, so I'm leaving it.
            last_entity_details = sg_data.get_entity_links(self.last_timesheet['entity']['type'],
                                                           self.last_saved_task,
                                                           self.last_timesheet['entity']['id'],
                                                           self.last_project_id)
            if last_entity_details:
                self.last_entity_type = last_entity_details['entity']['type']
                self.last_entity_id = last_entity_details['entity']['id']
                self.last_saved_entity = last_entity_details['entity']['name']

    def set_last_timesheet(self, timesheet=None):
        # --------------------------------------------------------------------------------------------------------
        # Find a current time-sheet and use it for defaults or, use the last saved information
        # --------------------------------------------------------------------------------------------------------
        # Get the last timesheet
        if timesheet:
            self.last_timesheet = timesheet

        if self.last_timesheet:
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'LAST TIMESHEET: %s' % self.last_timesheet)

            # Get last start and end times
            try:
                self.last_out_time = self.last_timesheet['sg_task_end']
            except KeyError, e:
                print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                      'No sg_task_end set. Returned null. Setting to None...')
                self.last_out_time = None
            self.last_in_time = self.last_timesheet['sg_task_start']

            if not self.last_out_time:
                # The timesheet is still clocked in.
                # TODO: Perhaps this is where I check the aint_today() feature to make sure that it's not an old
                #  timesheet.
                # NOTE: isn't there a local self.clocked_in variable?  Need to find that and set it here maybe.
                self.time_lord.clocked_in = True
                self.last_project_name = self.last_timesheet['project']['name']
                last_project_details = None
                tries = 0
                while not last_project_details and tries < 10:
                    try:
                        last_project_details = sg_data.get_project_details_by_name(self.last_project_name)
                    except Exception, e:
                        logger.error('Failure!  Passing.  %s' % e)
                    time.sleep(5)
                    tries += 1
                print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                      'last_project_details: %s' % last_project_details)
                self.last_project_id = last_project_details['id']
                self.last_saved_project = '%s' % self.last_project_name
                self.last_saved_task = self.last_timesheet['entity']['name']
                self.last_task_id = self.last_timesheet['entity']['id']
                last_entity_details = sg_data.get_entity_links(self.last_timesheet['entity']['type'],
                                                               self.last_saved_task,
                                                               self.last_timesheet['entity']['id'],
                                                               self.last_project_id)
                if last_entity_details:
                    self.last_entity_type = last_entity_details['entity']['type']
                    self.last_entity_id = last_entity_details['entity']['id']
                    self.last_saved_entity = last_entity_details['entity']['name']
                    # NOTE: Redundant?  Disabling it until I'm sure
                    # self.last_project = '%s' % self.last_project_name
            else:
                self.time_lord.clocked_in = False
                self.last_project_name = self.last_saved_project
                find_last_proj_id = sg_data.get_project_details_by_name(self.last_project_name)
                if find_last_proj_id and 'id' in find_last_proj_id.keys():
                    self.last_project_id = find_last_proj_id['id']
                    last_entity_details = sg_data.get_entity_links(self.last_timesheet['entity']['type'],
                                                                   self.last_timesheet['entity']['name'],
                                                                   self.last_timesheet['entity']['id'],
                                                                   self.last_project_id)
                else:
                    self.last_project_id = None
                    last_entity_details = None

                if last_entity_details:
                    self.last_entity_type = last_entity_details['entity']['type']
                    self.last_entity_id = last_entity_details['entity']['id']
                else:
                    self.last_entity_type = None
                    self.last_entity_id = None

    # -----------------------------------------------------------------------------------------------------------------
    # Needles and Monitor Output
    # -----------------------------------------------------------------------------------------------------------------
    def set_daily_total_needle(self, total):
        '''
        Set this to adjust the needs and the output monitor values simultaneously.
        :param total: A total value of the daily total hours minus lunch and breaks
        :return:
        '''
        if total:
            # set the needle to the daily total and also trigger a set_daily_output monitor event
            self.time_lord.set_daily_output(total)
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
        self.time_lord.set_weekly_output(total)
        if total:
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
        self.ui.output_trt.setPlainText(message)

    def start_end_output(self, message=None):
        self.ui.output_start_end.setPlainText(message)

    def user_output(self, message=None):
        self.ui.output_user.setPlainText(message)

    def daily_output(self, message=None):
        self.ui.output_daily.setPlainText(message)

    def weekly_output(self, message=None):
        self.ui.output_weekly.setPlainText(message)

    def lower_output(self, message=None):
        self.ui.lower_output.setPlainText(message)

    def get_user_start_time(self):
        '''
        Eventually, this should return a user set start time from the UI.  Not sure right off hand yet how to do that.
        :return:
        '''
        return None

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
            self.time_lord.start()

    def clock_out(self):
        try:
            self.ui.clock_button.clicked.disconnect(self.stop_time)
        except:
            pass
        try:
            self.ui.clock_button.clicked.disconnect(self.switch_time)
        except:
            pass
        self.ui.clock_button.clicked.connect(self.start_time)
        self.time_lord.clocked_in = False
        self.time_lord.time_signal.clock_state.emit(0)
        self.time_lord.time_signal.req_daily_total.emit('Update!')
        self.time_lord.time_signal.req_weekly_total.emit('Update!')
        self.time_lord.time_signal.clock_out_user.emit(self.last_timesheet)

    def clock_in(self, message=None):
        # Check to see if the UI settings are valid for a new timesheet.
        if not self.selection_check():
            # The settings are invalid.  Kick it back.
            return False
        try:
            # Disconnect the start time action
            self.ui.clock_button.clicked.disconnect(self.start_time)
        except:
            pass
        try:
            # Disconnect the switch time action
            self.ui.clock_button.clicked.disconnect(self.switch_time)
        except:
            pass

        # Connect the Stop Time action.
        self.ui.clock_button.clicked.connect(self.stop_time)
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

    def selection_check(self):
        # Sets the Status Lights and adds Error Messages to the output monitor
        if self.ui.project_dropdown.currentText() == 'Select Project' or self.ui.project_dropdown.currentIndex() == 0:
            self.time_lord.time_signal.error_state.emit(True)
            self.time_lord.time_signal.steady_state.emit(False)
            self.time_lord.time_signal.lower_output.emit('You must select a Project!')
            # self.time_lord.clocked_in = False
            return False
        else:
            self.time_lord.time_signal.error_state.emit(False)
            self.time_lord.time_signal.steady_state.emit(True)
        if self.ui.entity_dropdown.currentText() == 'Select Asset/Shot' or self.ui.entity_dropdown.currentIndex() == 0:
            self.time_lord.time_signal.error_state.emit(True)
            self.time_lord.time_signal.steady_state.emit(False)
            self.time_lord.time_signal.lower_output.emit('You must select an entity!')
            # self.time_lord.clocked_in = False
            return False
        else:
            self.time_lord.time_signal.error_state.emit(False)
            self.time_lord.time_signal.steady_state.emit(True)
        if self.ui.task_dropdown.currentText() == 'Select Task' or self.ui.task_dropdown.currentIndex() == 0:
            self.time_lord.time_signal.error_state.emit(True)
            self.time_lord.time_signal.steady_state.emit(False)
            self.time_lord.time_signal.lower_output.emit('You must select a Task!')
            # self.time_lord.clocked_in = False
            return False
        else:
            self.time_lord.time_signal.error_state.emit(False)
            self.time_lord.time_signal.steady_state.emit(True)
        return True

    # ----------------------------------------------------------------------------------------------------------------
    # Timesheet Data Updaters - Set the project, entity and task drop downs.
    # ----------------------------------------------------------------------------------------------------------------
    def set_project_list(self, projects=None):
        # Clear out the projects so that we are not double adding entries.
        self.ui.project_dropdown.clear()
        # Collect the active projects from Shotgun
        active_projects = projects
        # Iterate through the list and add all the active projects to the dropdown
        if active_projects:
            for project in active_projects:
                self.ui.project_dropdown.addItem('%s' % project['name'], project['id'])
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'Getting default selection from settings.')
        # Get the index of the last project as listed in the UI
        proj_index = self.ui.project_dropdown.findText(self.last_saved_project)
        # Select the current project.
        if proj_index >= 0:
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'Setting project to last project listed.')
            self.ui.project_dropdown.setCurrentIndex(proj_index)

        # Connect the project drop-down to an on-change event.

    def request_entities(self, message=None):
        selected_proj = self.ui.project_dropdown.currentText()
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'selected project is %s' % selected_proj)
        project_id = self.ui.project_dropdown.itemData(self.ui.project_dropdown.currentIndex())

        if project_id:
            self.last_project_id = project_id
            self.time_lord.time_signal.error_state.emit(False)
            self.time_lord.time_signal.steady_state.emit(True)
            # Collect assets and shots.
            self.time_lord.time_signal.req_entity_list.emit(project_id)

    def req_update_entities(self, message=None):
        '''
        This function will trigger another function that will update_entities.  The reason for this (instead of going
        directly to update_entities) is that update_entities requires more elaborate data than a
        currentIndexChanged.connect() event can support.
        :param message: String trigger.  Does nothing.
        :return:
        '''
        proj_id = self.ui.project_dropdown.itemData(self.ui.project_dropdown.currentIndex())
        self.time_lord.time_signal.req_entity_list.emit(proj_id)

    def update_entities(self, data=None):
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,  data)
        if data:
            last_timesheet = data[0]
            self.last_timesheet = last_timesheet
            entities = data[1]
            # Put in the Assets first... Oh!  Use the categories and Sequences?
            self.ui.entity_dropdown.clear()
            self.ui.entity_dropdown.addItem('Select Asset/Shot', 0)
            for entity in entities:
                self.ui.entity_dropdown.addItem(entity['code'], entity['id'])
            self.ui.entity_dropdown.update()
        else:
            self.time_lord.time_signal.lower_output.emit('Project Dump: %s' % data)
            self.time_lord.time_signal.error_state.emit(True)
            self.time_lord.time_signal.steady_state.emit(False)
        entity_index = self.ui.entity_dropdown.findText(self.last_saved_entity)
        if entity_index >= 0:
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'Setting entity to last saved entity')
            self.ui.entity_dropdown.setCurrentIndex(entity_index)

    def req_update_tasks(self, message=None):
        '''
        This method askes for a regular update from an onChangeEvent with no data
        :param message:
        :return:
        '''
        ent_id = self.ui.entity_dropdown.itemData(self.ui.entity_dropdown.currentIndex())
        ent_name = self.ui.entity_dropdown.currentText()
        proj_index = self.ui.project_dropdown.currentIndex()

        context = {
            'entity_id': ent_id,
            'entity_name': ent_name,
            'proj_id': self.ui.project_dropdown.itemData(proj_index)
        }
        self.time_lord.time_signal.req_task_list.emit(context)

    def update_tasks(self, tasks=None):
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,  'Setting tasks...')
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,  tasks)
        if tasks:
            self.ui.task_dropdown.clear()
            self.ui.task_dropdown.addItem('Select Task', 0)
            for task in tasks:
                self.ui.task_dropdown.addItem(task['content'], task['id'])
        else:
            self.ui.task_dropdown.clear()
            self.ui.task_dropdown.addItem('Select Task', 0)
        if self.last_saved_task != self.last_timesheet['entity']['name']:
            self.last_saved_task = self.last_timesheet['entity']['name']
        task_index = self.ui.task_dropdown.findText(self.last_saved_task)
        if task_index >= 0:
            self.ui.task_dropdown.setCurrentIndex(task_index)
        # Lastly, connect the Task to an on-change event
        self.ui.task_dropdown.currentIndexChanged.connect(self.switch_state)
        self.switch_tasks()

    def switch_tasks(self):
        # QUERY: DO I need have the __init__ call the switch tasks? Or do I use a different method up there?
        #       The fear is that the last_saved_task might not accurately reflect what's going on, due to signal and
        #       slot delays.
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'Switching tasks...')
        if self.last_saved_task != self.ui.task_dropdown.currentText() and self.time_lord.clocked_in:
            self.time_lord.time_signal.clock_state.emit(2)
        else:
            if self.time_lord.clocked_in:
                self.time_lord.time_signal.clock_state.emit(1)
            else:
                self.time_lord.time_signal.clock_state.emit(0)

    def switch_state(self):
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'Switch state triggered')
        match = True

        selected_proj = self.ui.project_dropdown.currentText()

        # Check that the project matches
        if selected_proj != self.last_project_name:
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'Last project name does not match.')
            match = False

        # I get the entity, because it does not come with last_timesheet data
        # FIXME: Direct call.  This might be a good place for a signal wait_cond.
        entity = sg_data.get_entity_links(self.last_timesheet['entity']['type'], self.last_saved_task,
                                          self.last_task_id, self.last_project_id)
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'entity returns: %s' % entity)
        if entity:
            if entity['entity']['name'] != self.ui.entity_dropdown.currentText():
                print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                      'Battle of Hastings: Entity does not match the current text.')
                match = False
        elif self.last_saved_entity != self.ui.entity_dropdown.currentText():
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'Battle of Hastings: The entity still does not match the dropdown.')
            match = False

        if self.last_saved_task != self.ui.task_dropdown.currentText():
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'Tasks aren\'t cool.')
            match = False
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'Everything\'s cool now.')

        if match and self.time_lord.clocked_in:
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'match and timelord clocked in.  Emit 1')
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
        elif not match and self.time_lord.clocked_in:
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'Not matched and timelord clocked in.  Emit 2')
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
        elif not self.time_lord.clocked_in:
            print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                  'Timelord not clocked in.  Doesn\'t matter if it\'s matched.  Emit 0')
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
        self.time_lord.time_signal.set_last_timesheet.emit('Update')

    def set_start_datetime_clock(self, start_time=None):
        '''
        This will pop up a ui to set the start datetime.
        :param start_time:
        :return:
        '''
        pass

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

    def clock_in_button_state(self, message=None):
        # FIXME: This is getting called twice, one right after another.
        '''
        Takes an integer value between 0 and 2
        :param message: (int) 0 = clocked out, 1 = clocked in, 2 = clock switch
        :return:
        '''
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'clock_in_button_state message: %s' % message)
        # A value of None for message means that there is not clock-out time and the sheet is still active.
        self.ui.clock_button.setStyleSheet('background-image: url(:/lights buttons/elements/'
                                           'clock_button_%i.png);'
                                           'background-repeat: none;'
                                           'background-color: rgba(0, 0, 0, 0);'
                                           'border-color: rgba(0, 0, 0, 0);' % message)
        if message >= 1:
            # Let the engine know that it is clocked in.
            self.time_lord.clocked_in = True
            if message == 2:
                try:
                    self.ui.clock_button.clicked.disconnect(self.start_time)
                except:
                    pass
                try:
                    self.ui.clock_button.clicked.disconnect(self.stop_time)
                except:
                    pass
                self.ui.clock_button.clicked.connect(self.switch_time)
            # self.clock_out()
        else:
            # Let the engine know that it is clocked out.
            self.time_lord.clocked_in = False

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
        if self.time_lord.clocked_in:
            start_time = self.last_timesheet['sg_task_start']
            hour = start_time.time().hour
            minute = start_time.time().minute
            second = start_time.time().second
            hours = (30 * (hour + (minute / 60.0)))
            minutes = (6 * (minute + (second / 60.0)))
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
        if not self.time_lord.clocked_in:
            # self.last_timesheet = tl_time.get_last_timesheet(user=user)
            # self.timesheet_update.time_signal.ui_update.emit('Update!')
            # self.time_lord.time_signal.ui_update.emit()
            try:
                end_time = self.last_timesheet['sg_task_end']
                # NOTE: This is currently partially detecting that the thing is clocked out outside of the UI
                print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
                      'end_time: %s' % end_time)
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
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'Emitted: %s' % update)

    def update_from_timesheet(self, message=None):
        print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,
              'Updating the UI with... %s' % message)
        if message:
            task = message['task']
            tast_id = message['task_id']
            proj = message['project']
            proj_id = message['project_id']
            entity = message['entity']
            entity_id = message['entity_id']

            proj_index = self.ui.project_dropdown.findText(proj)

            if proj_index >= 0:
                print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,  'Updating project')
                self.ui.project_dropdown.setCurrentIndex(proj_index)
            self.request_entities()

            ent_index = self.ui.entity_dropdown.findText(entity)
            if ent_index >= 0:
                print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,  'Updating entity...')
                self.ui.entity_dropdown.setCurrentIndex(ent_index)

            task_index = self.ui.task_dropdown.findText(task)
            if task_index >= 0:
                print(inspect.stack()[0][2], inspect.stack()[1][2], inspect.stack()[1][3], datetime.now().time().second,  'Updating Tasks...')
                self.ui.task_dropdown.setCurrentIndex(task_index)

            # Send a signal to update the local timesheet.
            print '~' * 60
            print 'IS CLOCKED IN: %s' % self.time_lord.clocked_in
            print 'Testing last timesheet: %s' % self.last_timesheet


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
