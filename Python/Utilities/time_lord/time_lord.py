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

        # Initialize UI timer
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

        self.tick = QtCore.QTime.currentTime()

        # Setup settings system
        self.settings = QtCore.QSettings('AdamBenson', 'TimeLord')
        self.last_project = self.settings.value('last_project', '.')
        self.last_entity = self.settings.value('last_entity', '.')
        self.last_task = self.settings.value('last_task', '.')

        # Signal setup
        self.time_signal = time_signals()

        # Setup Time Engine
        self.time_lord = time_lord()

        # Setup UI
        self.ui = tlu.Ui_TimeLord()
        self.ui.setupUi(self)

        # Connect the signals to the functions below
        self.time_lord.time_signal.main_clock.connect(self.main_clock)
        self.time_lord.time_signal.upper_output.connect(self.upper_output)
        self.time_lord.time_signal.error_state.connect(self.error_state)
        self.time_lord.time_signal.steady_state.connect(self.steady_state)

        # Start the output window
        # TODO: Update this with actual data instead of presets
        self.time_lord.set_upper_output(trt='00:00:00', start='date & time 1', end='Clock out time', user=user)

        # Check if the user is clocked in and set those values.
        last_timesheet = tl_time.get_last_timesheet(user=user)
        if not last_timesheet['sg_task_end']:
            self.ui.clock_button.setStyleSheet('background-image: url(:/lights buttons/elements/'
                                               'red_in_out_button.png);')
            # Let the engine know that it is clocked in.
            self.time_lord.clocked_in = True
        else:
            self.ui.clock_button.setStyleSheet('background-image: url(:/lights buttons/elements/'
                                               'green_in_out_button.png);')
            # Let the engine know that it is clocked out.
            self.time_lord.clocked_in = False

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

        # Connect the drop-down to an on-change event.
        self.ui.project_dropdown.currentIndexChanged.connect(self.update_entities)

        # ------------------------------------------------------------------------------------------------------------
        # Use the project selection to get a list of Entities
        # ------------------------------------------------------------------------------------------------------------
        logger.debug('Getting entities for project %s' % self.last_project)
        if not self.ui.project_dropdown.currentText() == 'Select Project':
            proj_name = str(self.last_project).split(' - ')[1]
            logger.debug('proj_name = %s' % proj_name)
            logger.debug('last_timesheet project = %s' % last_timesheet['project']['name'])
            if proj_name != last_timesheet['project']['name']:
                logger.debug('The project names do not match!  Please select the project again.')
                # This would indicate that the switch should be activated, or that the wrong thing is clocked in.

        # self.ui.daily_total_progress.setValue(12)
        self.ui.clock_button.clicked.connect(self.start_time)

        test = QtGui.QTransform()
        test.rotate(30 * (self.tick.second()))
        self.ui.time_hour.setTransform(test)
        self.ui.time_hour.update()

        # The following test line will need to be automatically filled in future
        # cont.get_previous_work_day('06-17-2019', regular_days=config['regular_days'])

    def start_time(self):
        self.time_lord.kill_it = False
        self.settings.setValue('last_project', self.ui.project_dropdown.currentText())
        self.settings.setValue('last_entity', self.ui.entity_dropdpwn.currentText())
        self.settings.setValue('last_task', self.ui.task_dropdown.currentText())
        self.time_lord.start()

    def update_entities(self):
        selected_proj = self.ui.project_dropdown.currentText().split(' - ')[-1]
        logger.debug('selected project is %s' % selected_proj)
        project = sg_data.get_project_details_by_name(proj_name=selected_proj)
        if project:
            # Collect assets and shots.
            asset_entities = sg_data.get_project_assets(proj_id=project['id'])
            logger.debug('Assets collected: %s' % asset_entities)
            shot_entities = sg_data.get_project_shots(proj_id=project['id'])
            logger.debug('Shots Collected: %s' % shot_entities)

            # Put in the Assets first... Oh!  Use the categories and Sequences?

    def upper_output(self, message):
        self.ui.output_window.setPlainText(message)

    def error_state(self, message):
        # This method turns on or off the red error state light
        if message:
            self.ui.red_light.setVisible(True)
        else:
            self.ui.red_light.setVisible(False)

    def steady_state(self, message):
        # This method turns on or off the green steady state light.?
        if message:
            self.ui.green_light.setVisible(True)
        else:
            self.ui.green_light.setVisible(False)

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

