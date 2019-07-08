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

    def kill(self):
        self.kill_it = True

    def run(self, *args, **kwargs):
        self.run_the_clock()
        if self.clocked_in:
            # TODO: Add the things that an already clocked in user would need.
            #       For instance, they would NOT use the last thing they clocked into, only what is currently active.
            pass
        else:
            # Setup the things that an un-clocked in person would need.  Last thing they were clocked to, that sort of
            # jazz.
            pass

    def run_the_clock(self):
        # TODO: This will need to make sure that the UI is ready to start running. Project, Entity and Task are set
        #       and kick it back if they are not. Set the error light to red, display output, don't start the clock.
        second = int(datetime.now().second)
        while not self.kill_it:
            if int(datetime.now().second) != second:
                second = int(datetime.now().second)
                self.time_signal.main_clock.emit(str(second))

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

        # --------------------------------------------------------------------------------------------------------
        # Find a current time-sheet and use it for defaults or, use the last saved information
        # --------------------------------------------------------------------------------------------------------
        # Get the last timesheet
        self.last_timesheet = tl_time.get_last_timesheet(user=user)
        print 'LAST TIMESHEET: %s' % self.last_timesheet

        # Get last start and end times
        self.last_out_time = self.last_timesheet['sg_task_end']
        self.last_in_time = self.last_timesheet['sg_task_start']

        if not self.last_out_time:
            # The timesheet is still clocked in.
            self.last_project_name = self.last_timesheet['project']['name']
            last_project_details = sg_data.get_project_details_by_name(self.last_project_name)
            self.last_project_code = last_project_details['code']
            self.last_project_id = last_project_details['id']
            self.last_project = '%s - %s' % (self.last_project_code, self.last_project_name)
            self.last_task = self.last_timesheet['entity']['name']
            self.last_task_id = self.last_timesheet['entity']['id']
            last_entity_details = sg_data.get_entity_links(self.last_timesheet['entity']['type'],
                                                                self.last_task,
                                                                self.last_timesheet['entity']['id'])
            if last_entity_details:
                self.last_entity_type = last_entity_details['entity']['type']
                self.last_entity_id = last_entity_details['entity']['id']
                self.last_entity = last_entity_details['entity']['name']
        else:
            self.last_project_name = self.last_project.split(' - ')[-1]
            self.last_project_code = self.last_project.split(' - ')[0]
            last_entity_details = sg_data.get_entity_links(self.last_timesheet['entity']['type'],
                                                           self.last_timesheet['entity']['name'],
                                                           self.last_timesheet['entity']['id'])
            if last_entity_details:
                self.last_entity_type = last_entity_details['entity']['type']
                self.last_entity_id = last_entity_details['entity']['id']
            else:
                self.last_entity_type = None
                self.last_entity_id = None
            self.last_project_id = sg_data.get_project_details_by_name(self.last_project_name)['id']

        # --------------------------------------------------------------------------------------------------------
        # Signal setup
        # --------------------------------------------------------------------------------------------------------
        self.time_signal = time_signals()

        # --------------------------------------------------------------------------------------------------------
        # Setup Time Engine
        # --------------------------------------------------------------------------------------------------------
        self.time_lord = time_lord()

        # --------------------------------------------------------------------------------------------------------
        # Setup UI
        # --------------------------------------------------------------------------------------------------------
        self.ui = tlu.Ui_TimeLord()
        self.ui.setupUi(self)

        # Connect the signals to the functions below
        self.time_lord.time_signal.main_clock.connect(self.main_clock)
        self.time_lord.time_signal.upper_output.connect(self.upper_output)
        self.time_lord.time_signal.error_state.connect(self.error_state)
        self.time_lord.time_signal.steady_state.connect(self.steady_state)
        self.time_lord.time_signal.clock_state.connect(self.clock_in_button_state)

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
        # Now check that the last task is selected
        task_index = self.ui.task_dropdown.findText(self.last_task)
        if task_index >= 0:
            logger.debug('Setting the task to the last clocked into...')
            self.ui.task_dropdown.setCurrentIndex(task_index)

        # Lastly, connect the Task to an on-change event
        self.ui.task_dropdown.currentIndexChanged.connect(self.switch_tasks)

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
        elif not self.last_out_time:
            if self.ui.project_dropdown.currentText().split(' - ')[-1] == self.last_project_name\
                    and self.ui.entity_dropdown.currentText() == self.last_entity\
                    and self.ui.task_dropdown.currentText() == self.last_task:
                state = 1
            else:
                state = 2
        self.clock_in_button_state(state)

        # self.ui.daily_total_progress.setValue(12)
        self.ui.clock_button.clicked.connect(self.start_time)

        test = QtGui.QTransform()
        test.rotate(30 * (self.tick.second()))
        self.ui.time_hour.setTransform(test)
        self.ui.time_hour.update()

        # The following test line will need to be automatically filled in future
        # cont.get_previous_work_day('06-17-2019', regular_days=config['regular_days'])

    def update_settings(self):
        self.settings.setValue('last_project', self.ui.project_dropdown.currentText())
        self.settings.setValue('last_entity', self.ui.entity_dropdown.currentText())
        self.settings.setValue('last_task', self.ui.task_dropdown.currentText())

    def start_time(self):
        # TODO: Add features that start other processes as well.  Change the button connections, et cetera
        self.time_lord.kill_it = False
        self.update_settings()
        # TODO: The following .start() line may need to be moved up to the init
        self.time_lord.start()
        self.clock_in()

    def stop_time(self):
        self.time_lord.kill_it = True
        self.update_settings()
        self.clock_out()

    def switch_time(self):
        self.time_lord.kill_it = False  # Or should this be True? Do I need to kill the clock?
        self.update_settings()

    def clock_out(self, message=None):
        print 'Clocking out...'
        self.ui.clock_button.clicked.disconnect(self.stop_time)
        self.ui.clock_button.clicked.connect(self.start_time)
        self.time_lord.time_signal.clock_state.emit(0)

    def clock_in(self, message=None):
        print 'Clocking in...'
        self.ui.clock_button.clicked.disconnect(self.start_time)
        self.ui.clock_button.clicked.connect(self.stop_time)
        self.time_lord.time_signal.clock_state.emit(1)

    def clock_switch(self, message=None):
        print 'Switching the clock...'
        # self.ui.clock_button.clicked.disconnect(self.start_time)
        # self.ui.clock_button.clicked.disconnect(self.stop_time)
        # self.ui.clock_button.clicked.connect(self.)  # NOT SURE ABOUT ALL THIS YET
        self.time_lord.time_signal.clock_state.emit(2)

    def update_entities(self):
        # TODO: Add a button update routine for switching tasks that are not current.
        #       Or, just automatically change it to switch?  What about start up?
        selected_proj = self.ui.project_dropdown.currentText().split(' - ')[-1]
        logger.debug('selected project is %s' % selected_proj)
        project = sg_data.get_project_details_by_name(proj_name=selected_proj)

        # Emit the button states
        if project['code'] != self.last_project_name and self.time_lord.clocked_in:
            self.time_lord.time_signal.clock_state.emit(2)
        else:
            if self.time_lord.clocked_in:
                self.time_lord.time_signal.clock_state.emit(1)
            else:
                self.time_lord.time_signal.clock_state.emit(0)

        if project:
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

    def update_tasks(self):
        # TODO: Add a button update routine for switching tasks that are not current.
        logger.debug('Getting tasks...')
        tasks = sg_data.get_entity_tasks(self.last_entity_id)
        entity = sg_data.get_entity_links(self.last_timesheet['entity']['type'], self.last_task, self.last_task_id)
        if entity:
            if entity['entity']['name'] != self.ui.entity_dropdown.currentText() and self.time_lord.clocked_in:
                self.time_lord.time_signal.clock_state.emit(2)
            else:
                if self.time_lord.clocked_in:
                    self.time_lord.time_signal.clock_state.emit(1)
                else:
                    self.time_lord.time_signal.clock_state.emit(0)
        if tasks:
            self.ui.task_dropdown.clear()
            self.ui.task_dropdown.addItem('Select Task')
            for task in tasks:
                self.ui.task_dropdown.addItem(task['content'])

    def switch_tasks(self):
        logger.debug('Switching tasks...')
        if self.last_task != self.ui.task_dropdown.currentText() and self.time_lord.clocked_in:
            self.time_lord.time_signal.clock_state.emit(2)
        else:
            if self.time_lord.clocked_in:
                self.time_lord.time_signal.clock_state.emit(1)
            else:
                self.time_lord.time_signal.clock_state.emit(0)

    def upper_output(self, message=None):
        self.ui.output_window.setPlainText(message)

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
            # self.clock_out()
        else:
            # Let the engine know that it is clocked out.
            self.time_lord.clocked_in = False
            # self.clock_switch()

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

