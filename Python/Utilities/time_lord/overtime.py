"""
This is primarily for processing the UI for the overtime pop up.
It should do several things:
1. Pop-up alert when a user is about to go into overtime
2. Off up an overtime form.
3. Pop-Up alert when a user hits overtime.
4. Annoy the shit out of someone until they clock out once they're in overtime.  Unless the OT was approved.
    a. This may require another custom field to be added to Shotgun.  i.e. Overtime Approved Checkbox

"""
import shotgun_api3 as sgapi
import os
import sys
from PySide import QtGui, QtCore
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta
from dateutil import parser
import time
import math

# Time Lord Libraries
from bin.time_continuum import continuum
from bin.companions import companions
import bin.configuration
import bin.shotgun_collect
from bin.comm_system import comm_sys

from ui import time_lord_ot_alert as ot

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.4.7'

config = bin.configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'overtime.log'
log_root = os.path.join(sys.path[0], 'logs')
if not os.path.exists(log_root):
    os.makedirs(log_root)
log_path = os.path.join(log_root, log_file)
debug = config['debug_logging']
if debug == 'True' or debug == 'true' or debug == True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('overtime')
logger.setLevel(level=level)
fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                              backupCount=int(config['log_days']))
fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
fh.setFormatter(fm)
logger.addHandler(fh)

logger.info('Overtime Utility has started.')

# --------------------------------------------------------------------------------------------------
# Setup Shotgun Connection
# --------------------------------------------------------------------------------------------------
sg = sgapi.Shotgun(config['sg_url'], config['sg_name'], config['sg_key'])
logger.debug('Shotgun is connected.')

# --------------------------------------------------------------------------------------------------
# Connect Time Lord Components
# --------------------------------------------------------------------------------------------------
# setup continuum
tl_time = continuum(sg, config=config, sub='overtime')

# Setup and get users
users = companions(sg, config=config, sub='overtime')
user = users.get_user_from_computer()

# setup shotgun data connection
sg_data = bin.shotgun_collect.sg_data(sg, config=config, sub='overtime')

# Setup the communications system
comm = comm_sys(sg, config=config, sub='overtime')


class ot_signals(QtCore.QObject):
    snd_minutes = QtCore.Signal(str)
    snd_seconds = QtCore.Signal(str)
    snd_color = QtCore.Signal(str)
    button_state = QtCore.Signal(str)
    timesheet = QtCore.Signal(dict)
    message = QtCore.Signal(str)


class ot_clock(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.kill_it = False
        self.signals = ot_signals()
        self.timesheet_update = datetime.now()
        self.timesheet = tl_time.get_latest_timesheet(user=user)
        self.clocked_in = tl_time.is_user_clocked_in(user=user)

    def run(self, *args, **kwargs):
        self.chronograph()

    def chronograph(self):
        while not self.kill_it:
            if not self.clocked_in:
                self.kill_it = True
                continue

            lunch_task_id = sg_data.get_lunch_task(lunch_proj_id=int(config['admin_proj_id']),
                                                   task_name=config['lunch'])
            if lunch_task_id:
                lunch_task_id = lunch_task_id['id']

            daily_total = tl_time.get_daily_total(user=user, lunch_id=lunch_task_id)
            time_left = (float(config['ot_hours']) - daily_total) * 60.0
            secs, mins = math.modf(time_left)
            secs = math.fabs(int(secs * 60))
            mins = int(mins)
            secs = str('%02d' % secs)
            mins = str('%02d' % mins)
            self.signals.snd_minutes.emit(mins)
            self.signals.snd_seconds.emit(secs)
            if float(time_left) < 0.0:
                if self.timesheet_update > (datetime.now() + timedelta(minutes=15)):
                    self.timesheet_update = datetime.now()
                    self.timesheet = tl_time.get_latest_timesheet(user=user)
                self.signals.timesheet.emit(self.timesheet)
                self.signals.message.emit('You are in Overtime!!')
                color = 'color: rgb(255, 0, 0);'
                self.signals.snd_color.emit(color)
                self.signals.button_state.emit('Clock Out')
            else:
                self.signals.message.emit('You are about to go into Overtime!')

            # Hold for time loop
            time.sleep(1)


class overtime_popup(QtGui.QWidget):
    """
    NOTE: Conditions I need to set for the various activities:
        1. Change and listen to button states:
            a. No btn (not called that) - When it's before time, needs to close the window
                        When it's after time, it needs to clock out the user.
            b. Yes btn - Needs to send a slack message, possibly with a lengthy OAuth 2 link embedded in it.
        2. Check for Timesheet OT Status.  This also needs to happen elsewhere!  Because:
            a. If a timesheet is approved for OT, and the user switches times, the next time needs to carry over
                the OT
        3. Need to connect to the messaging system (Slack)
            a. Trying to figure out how to build a slack message with an embedded button that has a functional Shotgun
                REST API link built into it.  May not be possible.  Which means... additional server.
            b. Have to get a message link to activate the approved_for_OT checkbox AND send user a message back.
    """
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.timesheet = None
        self.signals = ot_signals()
        self.ot_clock = ot_clock()
        self.ot_clock.start()

        self.ui = ot.Ui_OT()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))
        self.setWindowTitle('Overtime! v%s' % __version__)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.ui.variable_btn.clicked.connect(self.thanks)
        self.ui.requestOT_btn.clicked.connect(self.request_ot)

        if not tl_time.is_user_clocked_in(user=user):
            self.set_buttons(state='Not Clocked In')
            self.ui.minutes.display(0)
            self.ui.seconds.display(0)
            self.ui.message1.setText('You are not clocked in. This is pointless.')
            self.ui.message2.setText('Just close the window.')

        self.stay_opened = True

        # CONNECTIONS
        self.ot_clock.signals.snd_minutes.connect(self.set_minutes)
        self.ot_clock.signals.snd_seconds.connect(self.set_seconds)
        self.ot_clock.signals.snd_color.connect(self.set_color)
        self.ot_clock.signals.button_state.connect(self.set_buttons)
        self.ot_clock.signals.timesheet.connect(self.set_timesheet)
        self.ot_clock.signals.message.connect(self.set_main_message)

    def request_ot(self):
        print('Request OT')
        admins = users.get_admins()
        print('admins: %s' % admins)
        if not self.timesheet:
            self.timesheet = tl_time.get_latest_timesheet(user=user)
        print('timesheet: %s' % self.timesheet)
        if admins:
            for admin in admins:
                try:
                    comm.send_ot_message(user=admin, proj=self.timesheet['project'], entity=self.timesheet['entity'])
                    print('Message Sent!')
                except Exception as e:
                    print('What the fuck: %s' % e)
        self.stay_opened = False
        self.close()

    def set_timesheet(self, timesheet=None):
        if timesheet:
            self.timesheet = timesheet

    def set_buttons(self, state=None):
        if state:
            if state == 'Clock Out':
                try:
                    self.ui.variable_btn.clicked.disconnect(self.thanks)
                except Exception:
                    pass
                self.ui.variable_btn.clicked.connect(self.clock_out)
                self.ui.variable_btn.setText('Clock Out')
            elif state == 'Not Clocked In':
                print('Disconnecting shit.')
                try:
                    self.ui.variable_btn.clicked.disconnect(self.clock_out)
                    print('disconnected')
                except Exception:
                    print('Failed')
                    pass
                self.ui.variable_btn.clicked.connect(self.thanks)
                self.ui.variable_btn.setText('Close')
                self.ui.requestOT_btn.hide()
                self.ui.or_sep.hide()
            else:
                try:
                    self.ui.variable_btn.clicked.disconnect(self.clock_out)
                except Exception:
                    pass
                self.ui.variable_btn.clicked.connect(self.thanks)
                self.ui.variable_btn.setText('Thanks for the Reminder')

    def set_color(self, color=None):
        if color:
            self.ui.minutes.setStyleSheet(color)
            self.ui.seconds.setStyleSheet(color)

    def set_main_message(self, msg=None):
        if msg:
            self.ui.message1.setText(msg)

    def set_minutes(self, mins=None):
        if mins:
            self.ui.minutes.display(mins)

    def set_seconds(self, secs=None):
        if secs:
            self.ui.seconds.display(secs)

    def thanks(self):
        self.stay_opened = False
        self.close()

    def clock_out(self):
        self.stay_opened = False
        tl_time.clock_out_time_sheet(timesheet=self.timesheet, clock_out=datetime.now())
        self.close()

    def closeEvent(self, event, *args, **kwargs):
        if self.stay_opened:
            event.ignore()
            logger.warning('You can\'t close the window this way!')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    o = overtime_popup()
    o.show()
    sys.exit(app.exec_())
