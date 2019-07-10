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
    main_clock = QtCore.Signal(str)
    in_clock = QtCore.Signal(str)
    out_clock = QtCore.Signal(str)
    running_clock = QtCore.Signal(str)
    upper_output = QtCore.Signal(str)
    lower_output = QtCore.Signal(str)
    error_state = QtCore.Signal(bool)
    steady_state = QtCore.Signal(bool)
    clock_state = QtCore.Signal(int)


# class time_engine(QtCore.QThread):
#     # This bit is trial and error.  It may have to go into the main UI, but my fear is that
#     # the process will hang up the UI.
#     def __init__(self, parent=None):
#         super(time_engine, self).__init__(parent)
#         timer = QtCore.QTimer(self)
#         timer.timeout.connect(self.update)
#         timer.start(1000)


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
        # if self.clocked_in:
        #     # TODO: Add the things that an already clocked in user would need.
        #     #       For instance, they would NOT use the last thing they clocked into, only what is currently active.
        #     pass
        # else:
        #     # Setup the things that an un-clocked in person would need.  Last thing they were clocked to, that sort of
        #     # jazz.
        #     pass

    def run_the_clock(self):
        # TODO: This will need to make sure that the UI is ready to start running. Project, Entity and Task are set
        #       and kick it back if they are not. Set the error light to red, display output, don't start the clock.
        second = int(datetime.now().second)
        while self.clocked_in:
            if int(datetime.now().second) != second:
                second = int(datetime.now().second)
                self.time_signal.main_clock.emit(str(second))
                print self.clocked_in
                if self.clocked_in:
                    running_time = tl_time.get_running_time(timesheet=self.last_timesheet)
                    # Here we take the running time and emit it to the display.
                    self.time_signal.running_clock.emit(running_time)

    def set_upper_output(self, trt=None, start=None, end=None, user=None):
        set_message = 'OUTPUT MONITOR\n' \
                      '------------------------------------\n' \
                      'TRT: %s\n' \
                      'Start: %s - End: %s\n' \
                      '%s CLOCKED IN' % (trt, start, end, user['name'])
        self.time_signal.upper_output.emit(set_message)


class time_lord_ui(QtGui.QMainWindow):

    def __init__(self):
        super(time_lord_ui, self).__init__(parent=None)

        # --------------------------------------------------------------------------------------------------------
        # Initialize UI timer
        # --------------------------------------------------------------------------------------------------------
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

        self.tick = QtCore.QTime.currentTime()

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
        self.time_lord.time_signal.main_clock.connect(self.main_clock)
        self.time_lord.time_signal.upper_output.connect(self.upper_output)
        self.time_lord.time_signal.lower_output.connect(self.lower_output)
        self.time_lord.time_signal.error_state.connect(self.error_state)
        self.time_lord.time_signal.steady_state.connect(self.steady_state)
        self.time_lord.time_signal.clock_state.connect(self.clock_in_button_state)
        self.time_lord.time_signal.running_clock.connect(self.set_runtime_clock)

        # Start the output window
        # TODO: Update this with actual data instead of presets
        self.time_lord.set_upper_output(trt='00:00:00', start='date & time 1', end='Clock out time', user=user)

        # Set state buttons
        if self.time_lord.error_state:
            self.error_state(True)
        else:
            self.error_state(False)

        if self.time_lord.steady_state:
            self.steady_state(True)
        else:
            self.steady_state(False)

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
        # TODO: First routine should get the current running time. Start Time - Now()
        #       Perhaps return it as a 6 digit string.
        #       Second routine should set the value to the clock.
        self.set_runtime_clock()

        # self.ui.daily_total_progress.setValue(12)

        test = QtGui.QTransform()
        test.rotate(30 * (self.tick.second()))
        self.ui.time_hour.setTransform(test)
        self.ui.time_hour.update()

        # The following test line will need to be automatically filled in future
        # cont.get_previous_work_day('06-17-2019', regular_days=config['regular_days'])

        # if self.time_lord.clocked_in:
        self.time_lord.start()

    def set_last_timesheet(self):
        # --------------------------------------------------------------------------------------------------------
        # Find a current time-sheet and use it for defaults or, use the last saved information
        # --------------------------------------------------------------------------------------------------------
        # Get the last timesheet
        self.last_timesheet = tl_time.get_last_timesheet(user=user)
        self.time_lord.last_timesheet = self.last_timesheet
        print 'LAST TIMESHEET: %s' % self.last_timesheet

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
            print 'in', last_entity_details
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
            print 'out', last_entity_details
            if last_entity_details:
                self.last_entity_type = last_entity_details['entity']['type']
                self.last_entity_id = last_entity_details['entity']['id']
            else:
                self.last_entity_type = None
                self.last_entity_id = None

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
        tl_time.clock_out_time_sheet(timesheet=self.last_timesheet, clock_out=datetime.now())
        self.time_lord.time_signal.lower_output.emit('You have clocked out!')

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
        task_id = sg_data.get_task_id(entity_id=entity_id, task_name=self.ui.task_dropdown.currentText())
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
        # TODO: I think this is not updating because it is not a signal.  Thus it's all frozen or some shit
        #       since now I'm start()ing the whole thing in the init.
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
        else:
            self.time_lord.time_signal.lower_output.emit('Project Dump: %s' % project)
            self.time_lord.time_signal.error_state.emit(True)
            self.time_lord.time_signal.steady_state.emit(False)

    def update_tasks(self):
        logger.debug('Getting tasks...')
        if not self.last_entity_id:
            # Here is where I will ensure the selection from the UI and retry to get
            # the entity_id:
            current_entity = self.ui.entity_dropdown.currentText()
            self.last_entity_id = sg_data.get_entity_id(proj_id=self.last_project_id,
                                                        entity_name=current_entity)
        tasks = sg_data.get_entity_tasks(self.last_entity_id)
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

    def main_clock(self, in_time):
        # Function that automatically updates UI when triggered by a signal
        # self.ui.test_counter.setText(in_time)
        angle = int(in_time) * 6
        test = QtGui.QTransform()
        test.rotate(angle)
        self.ui.time_hour.setTransform(test)
        self.ui.time_hour.update()
        print angle


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName('AdamBenson')
    app.setOrganizationDomain('adamdbenson.com')
    app.setApplicationName('TimeLord')
    window = time_lord_ui()
    window.show()
    sys.exit(app.exec_())

