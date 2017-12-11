import ctypes
import msvcrt as ms
import logging
import os
import platform
import sys
import json
import urllib
import urllib2
import time
from datetime import datetime, timedelta

from PySide.QtCore import *
from PySide.QtGui import *
from shotgun_api3 import Shotgun

from ui import lunch_break_dialog as lbd
from ui import alert_dialog as ad

######################################################################################
# This updated test will work to use a time-subtraction based timer, instead of the
# additive timer I have now.
# In other words:
# While (ts_click_time - datetime.now()) < 15 minutes:
#   (mouse click) ------>
#   Set timer to now: ts_click_time = datetime.now()
# if datetime.now() > 15 minutes:
#   Send signal to Dialog
#   Set timer to now: ts_click_time = datetime.now()
#
# Feature List:
# 1. Create a Shotgun Database with parameters in it.  Allowing for remotely updating
#       the timers, break times, End of Day conditions.  Any hard coded variable.
# 2.
######################################################################################


# ----------------------------------------------------------------------------------------------------------------------
# Global Variables
# ----------------------------------------------------------------------------------------------------------------------

# Setup Logging....
dt_now = datetime.strftime(datetime.now(), '%Y%m%d_%H%M')
if not os.path.exists('%s\\TSheets_desktop' % os.environ['APPDATA']):
    os.mkdir('%s\\TSheets_desktop' % os.environ['APPDATA'])
if not os.path.exists('%s\\TSheets_desktop\\logs' % os.environ['APPDATA']):
    os.mkdir('%s\\TSheets_desktop\\logs' % os.environ['APPDATA'])

logger = logging.getLogger('t_sheets_desktop')
log_file = logging.FileHandler('%s\\TSheets_desktop\\logs\\ts_dt_log_%s.log' % (os.environ['APPDATA'], dt_now))
formatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s')
log_file.setFormatter(formatter)
logger.addHandler(log_file)
logger.setLevel(logging.DEBUG)

# Connect to Shotgun
logger.debug('Beginning Shotgun connection...')
shotgun_conf = {
    'url': 'https://asc.shotgunstudio.com',
    'name': 'tsheets_desktop',
    'key': 'c287b2609fc71a502e1d680a5f30f81b7a17876cb56b678b4c893306d8b4db2d'
}
sg = Shotgun(shotgun_conf['url'], shotgun_conf['name'], shotgun_conf['key'])

# Setup Timers
fields = [
    'sg_time',
    'sg_seconds',
    'sg_on_off'
]

# -----------------------------------------------------------------------------------------------------------------
#  SG Variables Set
# -----------------------------------------------------------------------------------------------------------------
lunch_start = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'lunch_start']], fields=fields)
lunch_end = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'lunch_end']], fields=fields)
lunch_start_time = datetime.strptime(lunch_start['sg_time'], '%H:%M:%S').time()
lunch_end_time = datetime.strptime(lunch_end['sg_time'], '%H:%M:%S').time()

lunch_params = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'lunch_timer']], fields=fields)
lunch_active = lunch_params['sg_on_off']
timer_seconds = lunch_params['sg_seconds']

start_slave = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'start_slave']], fields=fields)['sg_on_off']
end_of_day = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'end_of_day']], fields=fields)
eod_time = datetime.strptime(end_of_day['sg_time'], '%H:%M:%S').time()
eod_params = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'eod_timer']], fields=fields)
eod_timer = eod_params['sg_seconds']
eod_active = eod_params['sg_on_off']
overtime = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'overtime']], fields=fields)
ot_time = datetime.strptime(overtime['sg_time'], '%H:%M:%S').time()
ot_params = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'ot_timer']], fields=fields)
ot_timer = ot_params['sg_seconds']
ot_active = ot_params['sg_on_off']
reset = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'reset_time']], fields=fields)
reset_time = datetime.strptime(reset['sg_time'], '%H:%M:%S').time()
get_param_timer = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'param_reset_timer']], fields=fields)
param_timer = get_param_timer['sg_seconds']
logger.debug('Timers set from Shotgun.')


# Add buffers
logger.debug('Create Buffers...')
ts_buffer = QWaitCondition()
buffer_not_full = QWaitCondition()
mutex = QMutex()

# Define system variables
osSystem = platform.system()

if osSystem == 'Windows':
    base = '//hal'
    env_user = 'USERNAME'
    computername = 'COMPUTERNAME'
else:
    base = '/Volumes'
    env_user = 'USER'
    computername = 'HOSTNAME'

url = 'https://rest.tsheets.com/api/v1/'

admin = 'adamb'

# Make T-Sheets connections
logger.debug('Get T-Sheets Authorization from Shotgun')
auth_id = 3
auth_filters = [
    ['id', 'is', auth_id]
]
auth_fields = ['code']

auth_data = sg.find_one('CustomNonProjectEntity06', auth_filters, auth_fields)
authorization = auth_data['code']
headers = {
    'Authorization': 'Bearer %s' % authorization
}
logger.debug('T-Sheets authorization headers created!')


# ------------------------------------------------------------------------------------------------------------------
# T-Sheets Web Connection IO
# ------------------------------------------------------------------------------------------------------------------
class ts_portal:
    def _send_to_tsheets(self, page=None, data=None):
        if page:
            if data:
                try:
                    packed_data = json.dumps(data)
                    request = urllib2.Request('%s%s' % (url, page), headers=headers, data=packed_data)
                    request.add_header('Content-Type', 'application/json')
                    response = urllib2.urlopen(request)
                    response_data = json.loads(response.read())
                    return response_data
                except Exception, e:
                    logger.error('APP: Send to T-Sheets connection failed!  Error: %s' % e)
            else:
                logger.warning('_send_to_tsheets(data) not detected!')
                return False
        else:
            logger.warning('_send_to_tsheets(page) not detected!')
            return False

    def _return_from_tsheets(self, page=None, data=None):
        if page:
            try:
                if data:
                    data_list = urllib.urlencode(data)
                    Q = '?'
                else:
                    data_list = ''
                    Q = ''
                request = urllib2.Request('%s%s%s%s' % (url, page, Q, data_list), headers=headers)
                response = urllib2.urlopen(request)
                response_data = json.loads(response.read())
                return response_data
            except Exception, e:
                logger.error('APP: Return from T-Sheets Connection Failed!  Error: %s' % e)
        else:
            logger.warning('_return_from_tsheets(page) not detected.')
            return False

    def _edit_tsheets(self, page=None, data=None):
        if page:
            if data:
                try:
                    opener = urllib2.build_opener(urllib2.HTTPHandler)
                    packed_data = json.dumps(data)
                    request = urllib2.Request('%s%s' % (url, page), headers=headers, data=packed_data)
                    request.add_header('Content-Type', 'application/json')
                    request.get_method = lambda: 'PUT'
                    response = opener.open(request)
                    response_data = json.loads(response.read())
                    return response_data
                except Exception, e:
                    logger.error('APP: Edit T-Sheets Connection Failed! Error: %s' % e)
            else:
                logger.warning('_edit_thseets(data) not detected.')
                return False
        else:
            logger.warning('_edit_thseets(page) not detected.')
            return False

    def return_subs(self, job_id=None):
        # this returns all children of a parent job id.  It does not return sub-children.
        if job_id:
            subjobsparams = {
                'parent_ids': job_id,
                'active': 'yes'
            }
            subjoblist = urllib.urlencode(subjobsparams)
            subjob_request = urllib2.Request('%sjobcodes?%s' % (url, subjoblist), headers=headers)
            subjob_js = json.loads(urllib2.urlopen(subjob_request).read())
            for sj_type, sj_result in subjob_js.items():
                if sj_type == 'results':
                    sj_jobs_data = sj_result['jobcodes']
                    return sj_jobs_data
            logger.warning('return_subs data not processed!')
            return False
        logger.warning('return_subs data not processed!')
        return False


# -----------------------------------------------------------------------------------------------------------------
# Main Engines
# -----------------------------------------------------------------------------------------------------------------
class ts_signal(QObject):
    sig = Signal(str)
    lunch = Signal(str)
    alert = Signal(str)
    eod = Signal(str)
    stop_eod = Signal(str)
    clock_out = Signal(str)
    reset = Signal(int)


class ts_timer(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.running = True
        self.signal = ts_signal()
        self.lunch_break = False
        self.eod = False
        self.break_timer = False
        self.eod_tally = []
        self.break_tally = []
        ch = datetime.now().hour
        cm = datetime.now().minute
        cs = datetime.now().second
        self.click_time = datetime.strptime('%s:%s:%s' % (ch, cm, cs), '%H:%M:%S')
        self.param_timer = (self.click_time + timedelta(seconds=param_timer))
        print self.param_timer.time()
        self.signal.stop_eod.connect(self.kill_eod)

    def reset(self):
        self.running = False
        self.signal.reset.emit(0)
        self.running = True
        time.sleep(2)

    def run(self, *args, **kwargs):
        print 'Running...'
        # setup tests
        break_start = None
        break_end = None
        overtimer = False
        eod_start = None
        ot_diff = None
        mouse = ctypes.windll.user32

        # Start the main timer
        while self.running:
            # Set Click Timers
            ch = datetime.now().hour
            cm = datetime.now().minute
            cs = datetime.now().second
            ct = datetime.strptime('%s:%s:%s' % (ch, cm, cs), '%H:%M:%S')

            # Day Reset
            if ct.time() == reset_time:
                time.sleep(2)
                self.reset()

            # Reset Params
            if ct.time() == self.param_timer.time():
                self.param_timer = (ct + timedelta(seconds=param_timer))
                time.sleep(1)
                self.reset_variables()

            # Regular Click Check
            if mouse.GetKeyState(0x01) not in [0, 1] and not self.break_timer and not self.eod:
                self.click_time = ct

            elapsed = (ct - self.click_time).seconds

            # EOD Timer:
            eod_end = eod_timer * 2
            if ct.time() > eod_time and not self.eod and eod_timer <= elapsed < eod_end \
                    and len(self.eod_tally) < 1 and eod_active:
                self.eod = True
                self.eod_tally.append(True)
                eod_start = ct.time()
                print 'End of Day: %s' % eod_start
                stopped_working = (ct - timedelta(seconds=ot_timer)).time()
                self.signal.eod.emit('%s' % stopped_working)
            elif ct.time() > eod_time and elapsed > eod_end and len(self.eod_tally) == 1 and self.eod and eod_active:
                self.eod = False
                eod_start = ct.time()
                print 'Time clock out occurred: %s' % eod_start
                stopped_working = (ct - timedelta(seconds=elapsed)).time()
                self.signal.clock_out.emit('%s' % stopped_working)

            # Lunch Break Check 1
            if elapsed >= timer_seconds and not self.break_timer and len(self.break_tally) < 1 and lunch_active:
                if lunch_start_time <= ct.time() < lunch_end_time:
                    self.break_timer = True
                    self.break_tally.append(True)
                    break_start = ct.time()
                    print 'Break Start: %s' % break_start

            # Lunch Break Check 2
            if mouse.GetKeyState(0x01) not in [0, 1] and self.break_timer and lunch_active:
                break_end = ct.time()
                print 'Break End: %s' % break_end
                self.click_time = ct
                self.signal.lunch.emit('{"start": "%s", "end": "%s"}' % (break_start, break_end))
                self.break_timer = False
                break_start = None
                break_end = None

    def kill_eod(self):
        self.eod = False
        self.eod_tally = []
        ch = datetime.now().hour
        cm = datetime.now().minute
        cs = datetime.now().second
        self.click_time = datetime.strptime('%s:%s:%s' % (ch, cm, cs), '%H:%M:%S')

    # -----------------------------------------------------------------------------------------------------------------
    #  SG Variables Reset
    # -----------------------------------------------------------------------------------------------------------------
    def reset_variables(self):
        global lunch_active, lunch_start_time, lunch_end_time, timer_seconds, start_slave, eod_time, eod_timer, eod_active
        global ot_time, ot_timer, ot_active, reset_time, param_timer
        print 'Reset variables'

        lunch_start = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'lunch_start']], fields=fields)
        lunch_end = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'lunch_end']], fields=fields)
        lunch_start_time = datetime.strptime(lunch_start['sg_time'], '%H:%M:%S').time()
        lunch_end_time = datetime.strptime(lunch_end['sg_time'], '%H:%M:%S').time()

        lunch_params = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'lunch_timer']], fields=fields)
        lunch_active = lunch_params['sg_on_off']
        timer_seconds = lunch_params['sg_seconds']

        start_slave = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'start_slave']], fields=fields)[
            'sg_on_off']
        end_of_day = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'end_of_day']], fields=fields)
        eod_time = datetime.strptime(end_of_day['sg_time'], '%H:%M:%S').time()
        eod_params = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'eod_timer']], fields=fields)
        eod_timer = eod_params['sg_seconds']
        eod_active = eod_params['sg_on_off']
        overtime = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'overtime']], fields=fields)
        ot_time = datetime.strptime(overtime['sg_time'], '%H:%M:%S').time()
        ot_params = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'ot_timer']], fields=fields)
        ot_timer = ot_params['sg_seconds']
        ot_active = ot_params['sg_on_off']
        reset = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'reset_time']], fields=fields)
        reset_time = datetime.strptime(reset['sg_time'], '%H:%M:%S').time()
        get_param_timer = sg.find_one('CustomNonProjectEntity08', [['code', 'is', 'param_reset_timer']], fields=fields)
        param_timer = get_param_timer['sg_seconds']
        logger.debug('Timers reset from Shotgun.')
        print 'Done'
        return True


class ts_main(QMainWindow):
    """
    Opens from the if __name__ == '__main__' routine
    """
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.centralwidget = QWidget(self)
        self.batchbutton = QPushButton('Start batch',self)
        self.longbutton = QPushButton('Start long (10 seconds) operation',self)
        self.label1 = QLabel('Continuos batch')
        self.label2 = QLabel('Long batch')
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.batchbutton)
        self.vbox.addWidget(self.longbutton)
        self.vbox.addWidget(self.label1)
        self.vbox.addWidget(self.label2)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setLayout(self.vbox)
        self.lunch_dialog = None
        self.lunch_ui = None
        self.alert_dialog = None
        self.alert_ui = None
        self.portal = ts_portal()

        # Connect the Threads
        # self.thread = ts_thread()
        self.run_ts_timer = ts_timer()
        self.run_ts_timer.signal.lunch.connect(self.open_lunch_break)
        self.run_ts_timer.signal.eod.connect(self.eod)
        self.run_ts_timer.signal.clock_out.connect(self.clock_out)
        self.run_ts_timer.signal.reset.connect(self.reset)
        self.start_ts_timer()

    def started(self):
        self.label1.setText('Continuous batch started')

    def finished(self):
        print 'Finished...'

    def terminated(self):
        print 'terminated!'

    def start_ts_timer(self):
        # This method simply starts the timer.
        if not self.run_ts_timer.isRunning():
            self.run_ts_timer.exiting=False
            self.run_ts_timer.start()

    def reset(self):
        self.run_ts_timer = None
        self.run_ts_timer = ts_timer()
        self.run_ts_timer.signal.lunch.connect(self.open_lunch_break)
        self.run_ts_timer.signal.eod.connect(self.eod)
        self.run_ts_timer.signal.clock_out.connect(self.clock_out)
        self.run_ts_timer.signal.reset.connect(self.reset)
        self.start_ts_timer()

    def eod(self, data=None):
        print 'You stopped working at %s' % data
        cot = data.split(':')
        print cot
        clock_out_time = QTime(int(cot[0]), int(cot[1]), int(cot[2]))
        confirm_user = self.confirm_user()
        name = '%s %s' % (confirm_user['name'][0], confirm_user['name'][1])
        email = confirm_user['email']
        red_message = 'Are you still working?'
        main_message = 'No activity has been detected. Unless you click OK, you will be clocked out at the listed time.'
        sub_message = 'You can always clock back in, if this is in error.  You are responsible for your own timesheet!'
        self.alert_dialog = QDialog(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.alert_ui = ad.Ui_Dialog()
        self.alert_ui.setupUi(self.alert_dialog)
        self.alert_ui.eod_timer.setTime(clock_out_time)
        self.alert_ui.employee_name.setText(name)
        self.alert_ui.alert.setText(red_message)
        self.alert_ui.statement.setText(main_message)
        self.alert_ui.statement_2.setText(sub_message)
        self.alert_ui.ok_btn.clicked.connect(self.stay_clocked_in)
        self.alert_dialog.exec_()

    def stay_clocked_in(self):
        self.run_ts_timer.signal.stop_eod.emit(0)
        test_signal = self.alert_dialog.finished
        if test_signal:
            self.alert_dialog.hide()

    def clock_out(self, data=None):
        print 'Clocked Out At: %s' % data
        self.alert_dialog.hide()

    def open_lunch_break(self, data=None):
        t_data = eval(data)
        set_start = t_data['start']
        set_end = t_data['end']
        s = set_start.split(':')
        e = set_end.split(':')
        start = QTime(int(s[0]), int(s[1]), int(s[2]))
        end = QTime(int(e[0]), int(e[1]), int(e[2]))
        ts_buffer.wakeAll()
        self.lunch_dialog = QDialog(self)
        self.lunch_ui = lbd.Ui_Dialog()
        self.lunch_ui.setupUi(self.lunch_dialog)
        self.lunch_ui.start_time.setTime(start)
        self.lunch_ui.end_time.setTime(end)
        self.lunch_ui.yes_btn.clicked.connect(self.save_lunch_break)
        self.lunch_dialog.exec_()

    def save_lunch_break(self):
        logger.debug('Start lunch Break save...')
        s_h = self.lunch_ui.start_time.time().hour()
        s_m = self.lunch_ui.start_time.time().minute()
        s_s = self.lunch_ui.start_time.time().second()
        e_h = self.lunch_ui.end_time.time().hour()
        e_m = self.lunch_ui.end_time.time().minute()
        e_s = self.lunch_ui.end_time.time().second()
        start = '%s:%s:%s' % (s_h, s_m, s_s)
        end = '%s:%s:%s' % (e_h, e_m, e_s)
        logger.info('Start: %s, End %s' % (start, end))
        test_signal = self.lunch_dialog.finished
        if test_signal:
            self.lunch_dialog.hide()

    def get_sg_user(self, userid=None, name=None, email=None, sg_login=None, sg_computer=None):
        """
        Get a specific Shotgun User's details from any basic input.
        Only the first detected value will be searched.  If all 3 values are added, only the ID will be searched.
        :param userid: (int) Shotgun User ID number
        :param name:   (str) First and Last Name
        :param email:  (str) email@asc-vfx.com
        :return: user: (dict) Basic details
        """
        user = {}
        if userid or name or email or sg_login or sg_computer:
            filters = [
                ['sg_status_list', 'is', 'act']
            ]
            if userid:
                filters.append(['id', 'is', userid])
            elif name:
                filters.append(['name', 'is', name])
            elif email:
                filters.append(['email', 'is', email])
            elif sg_login:
                filters.append(['login', 'is', sg_login])
            elif sg_computer:
                filters.append(['sg_computer', 'is', sg_computer])
            fields = [
                'email',
                'name',
                'sg_computer',
                'login',
                'permission_rule_set',
                'projects',
                'groups'
            ]
            find_user = sg.find_one('HumanUser', filters, fields)
            if find_user:
                user_id = find_user['id']
                sg_email = find_user['email']
                computer = find_user['sg_computer']
                sg_name = find_user['name']
                # Dictionary {'type': 'PermissionRuleSet', 'id': 8 'name': 'Artist'}
                permissions = find_user['permission_rule_set']
                # List of Dictionaries [{'type': 'Group', 'id': 7, 'name':'VFX'}]
                groups = find_user['groups']
                login = find_user['login']
                # List of Dictionaries [{'type': 'Project', 'id': 168, 'name': 'masterTemplate'}]
                projects = find_user['projects']

                user[user_id] = {'name': sg_name, 'email': sg_email, 'computer': computer, 'permissions': permissions,
                                 'groups': groups, 'login': login, 'project': projects}
        else:
            logger.warning('No data passed to get_sg_user()!  Nothing processed!')
        return user

    def get_ts_active_users(self):
        ts_users = {}
        user_params = {'per_page': '50', 'active': 'yes'}
        user_js = self.portal._return_from_tsheets(page='users', data=user_params)
        if user_js:
            for l_type, result_data in user_js.items():
                if l_type == 'results':
                    user_data = result_data['users']
                    for user in user_data:
                        data = user_data[user]
                        first_name = data['first_name']
                        last_name = data['last_name']
                        email = data['email']
                        last_active = data['last_active']
                        active = data['active']
                        username = data['username']
                        user_id = data['id']
                        name = first_name, last_name
                        ts_users[email] = {'name': name, 'last_active': last_active, 'active': active,
                                           'username': username, 'email': email, 'id': user_id}
            return ts_users
        return False

    def get_ts_current_user_status(self, email=None):
        data = {}
        username = email
        # Send the Username from a script that already loads the shotgun data.  This returns the T-Sheets status of a
        # single user.
        all_users = self.get_ts_active_users()
        if username in all_users.keys():
            data = all_users[username]
        else:
            logger.warning('get_ts_current_user_status could not find the current user status!')
        return data

    def confirm_user(self):
        current_user = os.environ[env_user]
        current_comp = os.environ[computername]
        confirmed_user = False
        get_current_user = self.get_sg_user(sg_login=current_user)
        get_current_computer = self.get_sg_user(sg_computer=current_comp)
        if get_current_computer == get_current_user:
            user_data = get_current_user.values()[0]
            user_email = user_data['email']
            user_name = user_data['name']
            get_ts_user = self.get_ts_current_user_status(email=user_email)
            if get_ts_user:
                ts_user = '%s %s' % (get_ts_user['name'][0], get_ts_user['name'][1])
                if user_name == ts_user:
                    confirmed_user = get_ts_user
                else:
                    logger.warning('The User could not be confirmed on this computer.')
            else:
                logger.warning('confirm_user() has no value for get_ts_user data from get_ts_current_user_status()')
        return confirmed_user

if __name__=='__main__':
    # Set up the app
    app = QApplication(sys.argv)
    # Run ts_main hidden
    window = ts_main()
    # window.show()
    window.hide()
    sys.exit(app.exec_())
