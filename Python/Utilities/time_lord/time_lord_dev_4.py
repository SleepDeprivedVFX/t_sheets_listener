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

    def run(self):
        while not self.kill_it:
            # Setup a clock system
            self.tick = QtCore.QTime.currentTime()
            hour = (30.0 * (self.tick.hour() + (self.tick.minute() / 60.0)))
            minute = (6.0 * (self.tick.minute() + (self.tick.second() / 60.0)))

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
            self.time_hour.setPixmap(hour_hand_rot)
            self.time_minute.setPixmap(minute_hand_rot)
            self.time_hour.update()
            self.time_minute.update()

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
        logger.info('Time Machine Started')

    def run(self):
        self.listener()

    def listener(self):
        """
        The main listener loop.  Checks for new time sheets and updates the other services.
        :return:
        """
        while not self.kill_it:

            time.sleep(1)


# ------------------------------------------------------------------------------------------------------
# Primary Tools
# ------------------------------------------------------------------------------------------------------
# NOTE: time_lord currently does most of the processing
class time_lord(QtCore.QThread):
    """
    The Time Lord is the main functional tool kit for the UI
    """
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.kill_it = False

    def run(self):
        while not self.kill_it:

            # Wait a second
            time.sleep(1)


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

        # Connect to threads
        self.time_lord = time_lord()
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
        self.time_lord.project_dropdown = self.ui.project_dropdown
        self.time_lord.entity_dropdown = self.ui.entity_dropdown
        self.time_lord.task_dropdown = self.ui.task_dropdown
        # Clock Elements
        self.time_engine.time_hour = self.ui.time_hour
        self.time_engine.time_minute = self.ui.time_minute

        # Set main user info
        self.ui.artist_label.setText(user['name'])

        # Start your engines
        self.time_lord.start()
        self.time_engine.start()


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
