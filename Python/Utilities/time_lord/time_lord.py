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
    2. Get the main clock to work
    3. Create a date-picker to set the start and end time clocks.
        a. If the thing is not clocked in
        b. If the user sets start and end times
        c. Make the button yellow
        d. Add a completed time sheet.  Append create_new_timesheet() to include an end_time parameter
    4. Setup a live stream feed for limited data to the lower output.  Like Bullgozer and Rollout Machine
    5. Fix drop down appearance.
    6. Figure out how to make this into an exe file, or some kind of other "run" function that hides the python
    7. Automatically check for lunch breaks - Maybe have the button turn yellow again...
    8. Build in a rolling log file
    9. Have the start and end clocks do the following:
        a. If not clocked in...  hmmm. wait... I was going to say, if not clocked in, have it mirror the main time,
            but, perhaps it should only reflect the last in and out times?  Thus, those clocks don't usually move.
            However... if we want a user to clock in "now" then it should run the current time.  But, if the user
            pre-sets the time using the "set date-time" button, then that start time would hold (unless it conflicted
            with a previous entry.  Which brings about item...
    10. Have the clock in process ensure that the recorded in time is not prior to a previous out time.
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

config = configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'psychic_paper.log'
log_path = os.path.join(config['log_path'], log_file)
if config['debug_logging'] == 'True' or 'true' or True:
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


# ------------------------------------------------------------------------------------------------------
# Signal Emitters
# ------------------------------------------------------------------------------------------------------
class time_signals(QtCore.QObject):
    log = QtCore.Signal(str)
    error = QtCore.Signal(str)
    debug = QtCore.Signal(str)
    kill_signal = QtCore.Signal(bool)
    main_clock = QtCore.Signal(tuple)
    in_clock = QtCore.Signal(tuple)
    out_clock = QtCore.Signal(tuple)
    in_date = QtCore.Signal(str)
    out_date = QtCore.Signal(str)
    running_clock = QtCore.Signal(str)
    upper_output = QtCore.Signal(str)
    lower_output = QtCore.Signal(str)
    error_state = QtCore.Signal(bool)
    steady_state = QtCore.Signal(bool)
    clock_state = QtCore.Signal(int)
    daily_total = QtCore.Signal(float)
    weekly_total = QtCore.Signal(float)


class time_engine(QtCore.QThread):
    # This bit is trial and error.  It may have to go into the main UI, but my fear is that
    # the process will hang up the UI.
    def __init__(self, parent=None):
        super(time_engine, self).__init__(parent)
        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.update)
        # timer.start(1000)

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
        hour = datetime.now().hour
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

                if datetime.now().minute != minute:
                    daily_total = tl_time.get_daily_total(user=user)
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
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.time_signal = time_signals()
        self.kill_it = False
        self.clocked_in = False
        self.error_state = False
        self.steady_state = True
        self.kill_signal = self.time_signal.kill_signal.connect(self.kill)
        self.last_timesheet = tl_time.get_last_timesheet(user=user)

    def kill(self):
        self.kill_it = True

    def run(self, *args, **kwargs):
        self.run_the_clock()

    def run_the_clock(self):
        second = int(datetime.now().second)
        while self.clocked_in and not self.kill_it:
            # Make sure the loop only functions on a whole second
            if int(datetime.now().second) != second:
                second = int(datetime.now().second)
                # self.time_signal.main_clock.emit(str(second))
                daily_total = tl_time.get_daily_total(user=user)
                weekly_total = tl_time.get_weekly_total(user=user)
                if self.clocked_in:
                    rt = tl_time.get_running_time(timesheet=self.last_timesheet)
                    running_time = rt['rt']
                    # Here we take the running time and emit it to the display.
                    self.time_signal.running_clock.emit(running_time)
                    trt = '%s:%s:%s' % (rt['h'], rt['m'], rt['s'])
                    start_time = self.last_timesheet['sg_task_start']
                    start = '%s %s' % (start_time.date(), start_time.time())
                    end = '%s %s' % (datetime.now().date(), datetime.now().time())
                    self.set_upper_output(trt=trt, start=start, end=end, user=user, total_hours=daily_total,
                                          week_total=weekly_total)

                    # Set the start time date rollers:
                    ts_start = self.last_timesheet['sg_task_start']
                    start_date = ts_start.strftime('%m-%d-%y')
                    self.time_signal.in_date.emit(start_date)
                else:
                    # Set the start time date rollers:
                    ts_start = datetime.now()
                    start_date = ts_start.strftime('%m-%d-%y')
                    self.time_signal.in_date.emit(start_date)
                    start = '%s %s' % (self.last_timesheet['sg_task_start'].date(),
                                       self.last_timesheet['sg_task_start'].time())
                    end = '%s %s' % (self.last_timesheet['sg_task_end'].date(),
                                     self.last_timesheet['sg_task_end'].time())
                    self.set_upper_output(trt='00:00:00', start=start, end=end, user=user, total_hours=daily_total,
                                          week_total=weekly_total)
                    break

    def set_upper_output(self, trt=None, start=None, end=None, user=None, total_hours=None, week_total=None):
        if self.clocked_in:
            status = 'IN'
        else:
            status = 'OUT'
        set_message = 'OUTPUT MONITOR\n' \
                      '------------------------------------\n' \
                      'TRT: %s\n' \
                      'Start: %s\nEnd: %s\n' \
                      '%s CLOCKED %s\n' \
                      'Total Hours: %s\n' \
                      'Week Total: %s' % (trt, start, end, user['name'], status, total_hours, week_total)
        self.time_signal.upper_output.emit(set_message)


class time_lord_ui(QtGui.QMainWindow):

    def __init__(self):
        super(time_lord_ui, self).__init__(parent=None)

        # # --------------------------------------------------------------------------------------------------------
        # # Initialize UI timer
        # # --------------------------------------------------------------------------------------------------------
        # timer = QtCore.QTimer(self)
        # timer.timeout.connect(self.update)
        # timer.start(1000)
        #
        # self.tick = QtCore.QTime.currentTime()

        # --------------------------------------------------------------------------------------------------------
        # Set the saved settings
        # --------------------------------------------------------------------------------------------------------
        self.settings = QtCore.QSettings('AdamBenson', 'TimeLord')
        self.last_project = self.settings.value('last_project', '.')
        self.last_entity = self.settings.value('last_entity', '.')
        self.last_task = self.settings.value('last_task', '.')

        # # --------------------------------------------------------------------------------------------------------
        # # Signal setup
        # # --------------------------------------------------------------------------------------------------------
        # self.time_signal = time_signals()

        # --------------------------------------------------------------------------------------------------------
        # Setup Time Engine
        # --------------------------------------------------------------------------------------------------------
        self.time_lord = time_lord()
        self.time_engine = time_engine()
        self.time_signal = time_signals()

        # Setup and connect the last timesheet.
        self.last_timesheet = None
        self.last_out_time = None
        self.last_in_time = None
        self.last_task_id = None
        self.last_project_name = None
        self.last_project_code = None
        self.last_project_id = None
        self.last_entity_type = None
        self.last_entity_id = None
        self.set_last_timesheet()

        # --------------------------------------------------------------------------------------------------------
        # Setup UI
        # --------------------------------------------------------------------------------------------------------
        self.ui = tlu.Ui_TimeLord()
        self.ui.setupUi(self)

        # Connect the signals to the functions below
        self.time_engine.time_signal.main_clock.connect(self.main_clock)
        self.time_engine.time_signal.in_clock.connect(self.set_in_clock)
        self.time_engine.time_signal.out_clock.connect(self.set_out_clock)
        self.time_lord.time_signal.upper_output.connect(self.upper_output)
        self.time_lord.time_signal.lower_output.connect(self.lower_output)
        self.time_lord.time_signal.error_state.connect(self.error_state)
        self.time_lord.time_signal.steady_state.connect(self.steady_state)
        self.time_lord.time_signal.clock_state.connect(self.clock_in_button_state)
        self.time_lord.time_signal.running_clock.connect(self.set_runtime_clock)
        self.time_lord.time_signal.in_date.connect(self.set_start_date_rollers)
        self.time_engine.time_signal.daily_total.connect(self.set_daily_total)
        self.time_engine.time_signal.weekly_total.connect(self.set_weekly_total)

        # Start the output window
        daily_total = tl_time.get_daily_total(user=user)
        weekly_total = tl_time.get_weekly_total(user=user)
        start = '%s %s' % (self.last_timesheet['sg_task_start'].date(),
                           self.last_timesheet['sg_task_start'].time())
        if self.last_timesheet['sg_task_end']:
            end = '%s %s' % (self.last_timesheet['sg_task_end'].date(),
                             self.last_timesheet['sg_task_end'].time())
        else:
            end = '%s %s' % (datetime.now().date(), datetime.now().time())
        self.time_lord.set_upper_output(trt='00:00:00', start=start, end=end, user=user,
                                        total_hours=daily_total, week_total=weekly_total)

        # Set state buttons
        if self.time_lord.error_state:
            self.error_state(True)
        else:
            self.error_state(False)

        if self.time_lord.steady_state:
            self.steady_state(True)
        else:
            self.steady_state(False)

        # Set the rollers
        now = datetime.now()
        d = now.strftime('%m-%d-%y')
        self.set_start_date_rollers(d=d)
        self.set_end_date_rollers(d=d)

        # Set main user info
        self.ui.artist_label.setText(user['name'])

        # ------------------------------------------------------------------------------------------------------------
        # Set the project list.
        # ------------------------------------------------------------------------------------------------------------
        ''' This may need to become its own routine. '''
        logger.debug('Adding projects to project drop down...')
        active_projects = sg_data.get_active_projects()
        if active_projects:
            for project in active_projects:
                self.ui.project_dropdown.addItem('%s - %s' % (project['code'], project['name']))
        logger.debug('Getting default selection from settings.')
        proj_index = self.ui.project_dropdown.findText(self.last_project)
        if proj_index >= 0:
            logger.debug('Setting project to last project listed.')
            self.ui.project_dropdown.setCurrentIndex(proj_index)

        # Connect the project drop-down to an on-change event.
        self.ui.project_dropdown.currentIndexChanged.connect(self.update_entities)
        self.ui.project_dropdown.currentIndexChanged.connect(self.switch_state)

        # Change the selection highlight to none
        self.ui.project_dropdown.setFocus()

        # Then run it for the first time.
        self.update_entities()
        # Now check that the last or currently clocked-in entity is selected
        entity_index = self.ui.entity_dropdown.findText(self.last_entity)
        if entity_index >= 0:
            logger.debug('Setting Entity to the last project clocked into...')
            self.ui.entity_dropdown.setCurrentIndex(entity_index)

        # Run the task check for the first time
        self.update_tasks()
        # Then connect the Entity drop-down to an on-change event
        self.ui.entity_dropdown.currentIndexChanged.connect(self.update_tasks)
        self.ui.entity_dropdown.currentIndexChanged.connect(self.switch_state)
        # Now check that the last task is selected
        task_index = self.ui.task_dropdown.findText(self.last_task)
        if task_index >= 0:
            logger.debug('Setting the task to the last clocked into...')
            self.ui.task_dropdown.setCurrentIndex(task_index)

        # Lastly, connect the Task to an on-change event
        self.ui.task_dropdown.currentIndexChanged.connect(self.switch_state)

        # ------------------------------------------------------------------------------------------------------------
        # Start making sure the correct thing is the active clock
        # ------------------------------------------------------------------------------------------------------------
        logger.debug('Getting entities for project %s' % self.last_project)
        if not self.ui.project_dropdown.currentText() == 'Select Project':
            proj_name = str(self.last_project).split(' - ')[-1]
            logger.debug('proj_name = %s' % proj_name)
            logger.debug('last_timesheet project = %s' % self.last_timesheet['project']['name'])
            if proj_name != self.last_timesheet['project']['name']:
                logger.debug('The project names do not match!  Please select the project again.')
                # This would indicate that the switch should be activated, or that the wrong thing is clocked in.

        # set button state
        if self.last_out_time:
            state = 0
            self.ui.clock_button.clicked.connect(self.start_time)
        elif not self.last_out_time:
            if self.ui.project_dropdown.currentText().split(' - ')[-1] == self.last_project_name\
                    and self.ui.entity_dropdown.currentText() == self.last_entity\
                    and self.ui.task_dropdown.currentText() == self.last_task:
                state = 1
            else:
                state = 2
            self.ui.clock_button.clicked.connect(self.stop_time)
        self.clock_in_button_state(state)

        # Set the running time clock.
        self.set_runtime_clock()

        # Setup the daily total meter
        # The formula (totalHours/dailyMax) * degrees(70) or (35) - 35  # -35 is for the offset rotation of the graphic.
        daily_total = tl_time.get_daily_total(user=user)
        self.time_engine.time_signal.daily_total.emit(daily_total)

        # The following test line will need to be automatically filled in future
        # cont.get_previous_work_day('06-17-2019', regular_days=config['regular_days'])

        # if self.time_lord.clocked_in:
        self.time_lord.start()
        self.time_engine.start()

    def set_last_timesheet(self):
        # --------------------------------------------------------------------------------------------------------
        # Find a current time-sheet and use it for defaults or, use the last saved information
        # --------------------------------------------------------------------------------------------------------
        # Get the last timesheet
        self.last_timesheet = tl_time.get_last_timesheet(user=user)
        self.time_lord.last_timesheet = self.last_timesheet
        logger.debug('LAST TIMESHEET: %s' % self.last_timesheet)

        # Get last start and end times
        self.last_out_time = self.last_timesheet['sg_task_end']
        self.last_in_time = self.last_timesheet['sg_task_start']

        if not self.last_out_time:
            # The timesheet is still clocked in.
            self.time_lord.clocked_in = True
            self.last_project_name = self.last_timesheet['project']['name']
            last_project_details = sg_data.get_project_details_by_name(self.last_project_name)
            self.last_project_code = last_project_details['code']
            self.last_project_id = last_project_details['id']
            self.last_project = '%s - %s' % (self.last_project_code, self.last_project_name)
            self.last_task = self.last_timesheet['entity']['name']
            self.last_task_id = self.last_timesheet['entity']['id']
            last_entity_details = sg_data.get_entity_links(self.last_timesheet['entity']['type'],
                                                           self.last_task,
                                                           self.last_timesheet['entity']['id'],
                                                           self.last_project_id)
            if last_entity_details:
                self.last_entity_type = last_entity_details['entity']['type']
                self.last_entity_id = last_entity_details['entity']['id']
                self.last_entity = last_entity_details['entity']['name']
                self.last_project = '%s - %s' % (self.last_project_code, self.last_project_name)
        else:
            self.time_lord.clocked_in = False
            self.last_project_name = self.last_project.split(' - ')[-1]
            self.last_project_code = self.last_project.split(' - ')[0]
            self.last_project_id = sg_data.get_project_details_by_name(self.last_project_name)['id']
            last_entity_details = sg_data.get_entity_links(self.last_timesheet['entity']['type'],
                                                           self.last_timesheet['entity']['name'],
                                                           self.last_timesheet['entity']['id'],
                                                           self.last_project_id)
            if last_entity_details:
                self.last_entity_type = last_entity_details['entity']['type']
                self.last_entity_id = last_entity_details['entity']['id']
            else:
                self.last_entity_type = None
                self.last_entity_id = None

    def set_daily_total(self, total):
        if total:
            total -= 5.0
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

    def set_weekly_total(self, total):
        if total:
            total -= 5.0
            angle = ((total / (float(config['ot_hours']) * 10.0)) * 100.00) - 25.00  # I know my graphic spans 100 dgrs.
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

    def update_settings(self):
        self.settings.setValue('last_project', self.ui.project_dropdown.currentText())
        self.settings.setValue('last_entity', self.ui.entity_dropdown.currentText())
        self.settings.setValue('last_task', self.ui.task_dropdown.currentText())

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
        self.update_settings()
        # TODO: Add check to see if the service is already running first
        # if not self.time_lord.clocked_in:
        #     self.clock_in()
        self.clock_in()
        self.time_lord.start()

    def stop_time(self):
        self.time_lord.clocked_in = False
        self.time_lord.kill_it = True
        self.update_settings()
        self.clock_out()

    def switch_time(self):
        self.time_lord.clocked_in = False  # Or should this be True? Do I need to kill the clock?
        self.update_settings()
        self.clock_out()
        self.clock_in()
        self.time_lord.start()

    def clock_out(self, message=None):
        print 'Clocking out...'
        # if not self.selection_check():
        #     return False
        try:
            self.ui.clock_button.clicked.disconnect(self.stop_time)
        except:
            pass
        try:
            self.ui.clock_button.clicked.disconnect(self.switch_time)
        except:
            pass
        self.ui.clock_button.clicked.connect(self.start_time)
        self.time_lord.time_signal.clock_state.emit(0)
        daily_total = tl_time.get_daily_total(user=user)
        weekly_total = tl_time.get_weekly_total(user=user)
        tl_time.clock_out_time_sheet(timesheet=self.last_timesheet, clock_out=datetime.now())
        self.time_lord.time_signal.lower_output.emit('You have clocked out!')
        self.last_timesheet = tl_time.get_last_timesheet(user=user)

        ts_start = self.last_timesheet['sg_task_start']
        start_date = ts_start.strftime('%m-%d-%y')
        self.time_lord.time_signal.in_date.emit(start_date)
        start = '%s %s' % (self.last_timesheet['sg_task_start'].date(),
                           self.last_timesheet['sg_task_start'].time())
        end = '%s %s' % (self.last_timesheet['sg_task_end'].date(),
                         self.last_timesheet['sg_task_end'].time())
        self.time_lord.set_upper_output(trt='00:00:00', start=start, end=end, user=user, total_hours=daily_total,
                                        week_total=weekly_total)

    def clock_in(self, message=None):
        print 'Clocking in...'
        self.time_lord.clocked_in = True
        if not self.selection_check():
            return False
        try:
            self.ui.clock_button.clicked.disconnect(self.start_time)
        except:
            pass
        try:
            self.ui.clock_button.clicked.disconnect(self.switch_time)
        except:
            pass
        self.ui.clock_button.clicked.connect(self.stop_time)
        # self.time_lord.last_timesheet = tl_time.get_last_timesheet(user=user)
        self.time_lord.time_signal.clock_state.emit(1)
        self.time_lord.time_signal.lower_output.emit('New Timesheet created!')

        # Create context
        project_selection = self.ui.project_dropdown.currentText().split(' - ')[-1]
        project_details = sg_data.get_project_details_by_name(proj_name=project_selection)
        project_id = project_details['id']
        project_name = project_selection
        entity_id = sg_data.get_entity_id(proj_id=project_id, entity_name=self.ui.entity_dropdown.currentText())
        task_id = sg_data.get_task_id(entity_id=entity_id, task_name=self.ui.task_dropdown.currentText(),
                                      entity_name=self.ui.entity_dropdown.currentText(), proj_id=project_id)
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
        start_time = self.get_user_start_time()
        if not start_time:
            start_time = datetime.now()
        tl_time.create_new_timesheet(user=user, context=context, start_time=start_time)
        self.set_last_timesheet()

    def selection_check(self):
        if self.ui.project_dropdown.currentText() == 'Select Project' or self.ui.project_dropdown.currentIndex() == 0:
            self.time_lord.time_signal.error_state.emit(True)
            self.time_lord.time_signal.steady_state.emit(False)
            self.time_lord.time_signal.lower_output.emit('You must select a Project!')
            self.time_lord.clocked_in = False
            return False
        else:
            self.time_lord.time_signal.error_state.emit(False)
            self.time_lord.time_signal.steady_state.emit(True)
        if self.ui.entity_dropdown.currentText() == 'Select Asset/Shot' or self.ui.entity_dropdown.currentIndex() == 0:
            self.time_lord.time_signal.error_state.emit(True)
            self.time_lord.time_signal.steady_state.emit(False)
            self.time_lord.time_signal.lower_output.emit('You must select an entity!')
            self.time_lord.clocked_in = False
            return False
        else:
            self.time_lord.time_signal.error_state.emit(False)
            self.time_lord.time_signal.steady_state.emit(True)
        if self.ui.task_dropdown.currentText() == 'Select Task' or self.ui.task_dropdown.currentIndex() == 0:
            self.time_lord.time_signal.error_state.emit(True)
            self.time_lord.time_signal.steady_state.emit(False)
            self.time_lord.time_signal.lower_output.emit('You must select a Task!')
            self.time_lord.clocked_in = False
            return False
        else:
            self.time_lord.time_signal.error_state.emit(False)
            self.time_lord.time_signal.steady_state.emit(True)
        return True

    def update_entities(self, message=None):
        selected_proj = self.ui.project_dropdown.currentText().split(' - ')[-1]
        logger.debug('selected project is %s' % selected_proj)
        project = sg_data.get_project_details_by_name(proj_name=selected_proj)

        if project:
            self.time_lord.time_signal.error_state.emit(False)
            self.time_lord.time_signal.steady_state.emit(True)
            # Collect assets and shots.
            asset_entities = sg_data.get_project_assets(proj_id=project['id'])
            logger.debug('Assets collected: %s' % asset_entities)
            shot_entities = sg_data.get_project_shots(proj_id=project['id'])
            logger.debug('Shots Collected: %s' % shot_entities)

            # Put in the Assets first... Oh!  Use the categories and Sequences?
            self.ui.entity_dropdown.clear()
            self.ui.entity_dropdown.addItem('Select Asset/Shot')
            for asset in asset_entities:
                self.ui.entity_dropdown.addItem(asset['code'])
            for shot in shot_entities:
                self.ui.entity_dropdown.addItem(shot['code'])
            self.ui.entity_dropdown.update()
        else:
            self.time_lord.time_signal.lower_output.emit('Project Dump: %s' % project)
            self.time_lord.time_signal.error_state.emit(True)
            self.time_lord.time_signal.steady_state.emit(False)

    def update_tasks(self):
        logger.debug('Getting tasks...')
        # if not self.last_entity_id:
        # Here is where I will ensure the selection from the UI and retry to get
        # the entity_id:
        current_entity = self.ui.entity_dropdown.currentText()
        self.last_entity_id = sg_data.get_entity_id(proj_id=self.last_project_id,
                                                    entity_name=current_entity)
        tasks = sg_data.get_entity_tasks(entity_id=self.last_entity_id, entity_name=current_entity,
                                         proj_id=self.last_project_id)
        if tasks:
            self.ui.task_dropdown.clear()
            self.ui.task_dropdown.addItem('Select Task')
            for task in tasks:
                self.ui.task_dropdown.addItem(task['content'])
        else:
            self.ui.task_dropdown.clear()
            self.ui.task_dropdown.addItem('Select Task')

    def switch_tasks(self):
        logger.debug('Switching tasks...')
        if self.last_task != self.ui.task_dropdown.currentText() and self.time_lord.clocked_in:
            self.time_lord.time_signal.clock_state.emit(2)
        else:
            if self.time_lord.clocked_in:
                self.time_lord.time_signal.clock_state.emit(1)
            else:
                self.time_lord.time_signal.clock_state.emit(0)

    def switch_state(self):
        match = True

        selected_proj = self.ui.project_dropdown.currentText().split(' - ')[-1]
        project = sg_data.get_project_details_by_name(proj_name=selected_proj)

        # Check that the project matches
        if self.ui.project_dropdown.currentText().split(' - ')[-1] != self.last_project_name:
            match = False

        # I get the entity, because it does not come with last_timesheet data
        entity = sg_data.get_entity_links(self.last_timesheet['entity']['type'], self.last_task, self.last_task_id,
                                          self.last_project_id)
        if entity:
            if entity['entity']['name'] != self.ui.entity_dropdown.currentText():
                match = False
        elif self.last_entity != self.ui.entity_dropdown.currentText():
            match = False

        if self.last_task != self.ui.task_dropdown.currentText():
            match = False

        if match and self.time_lord.clocked_in:
            self.time_lord.time_signal.clock_state.emit(1)
        elif not match and self.time_lord.clocked_in:
            self.time_lord.time_signal.clock_state.emit(2)
        elif not self.time_lord.clocked_in:
            self.time_lord.time_signal.clock_state.emit(0)

    def set_start_datetime_clock(self, start_time=None):
        '''
        This will pop up a ui to set the start datetime.
        :param start_time:
        :return:
        '''
        pass

    def upper_output(self, message=None):
        self.ui.output_window.setPlainText(message)

    def lower_output(self, message=None):
        self.ui.lower_output.setPlainText(message)

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
        '''
        Takes an integer value between 0 and 2
        :param message: (int) 0 = clocked out, 1 = clocked in, 2 = clock switch
        :return:
        '''
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
            # self.clock_switch()

    def get_running_time(self):
        '''
        This may actually need to move into the time_continuum and get run in the thread.
        set_runtime_clock would then be the connected listener.
        :return:
        '''
        ts = self.last_timesheet
        if not ts['sg_task_end']:
            full_start = ts['sg_task_start']

    def set_runtime_clock(self, t='000000'):
        '''
        Sets the running time clock.
        :param t: (str) - While this is a number value, it must be exactly 6 digits long, thus string to maintain
                            the number of zeros needed for the default.
        :return: Running time.
        '''
        if len(t) == 6:
            logger.debug('Setting the runtime clock to %s' % t)
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
            end_time = self.last_timesheet['sg_task_end']
            hour = end_time.time().hour
            minute = end_time.time().minute
            second = end_time.time().second
            hours = (30 * (hour + (minute / 60.0)))
            minutes = (6 * (minute + (second / 60.0)))
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


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('AdamBenson')
    app.setOrganizationDomain('adamdbenson.com')
    app.setApplicationName('TimeLord')
    window = time_lord_ui()
    window.show()
    # sys.excepthook()  # TODO: Get this to work.
    sys.exit(app.exec_())

