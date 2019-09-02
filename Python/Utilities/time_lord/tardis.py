import os
import sys
import win32api
import win32con
import win32gui_struct
import itertools
import glob
import subprocess
import logging
import threading
import shotgun_api3 as sgapi
from PySide import QtCore, QtGui
from ctypes import windll, Structure, c_long, byref
import time
from datetime import datetime, timedelta
from dateutil import parser

from bin import companions, configuration, time_continuum, shotgun_collect

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui

# Setup Tardis systems
sys_path = sys.path

config = configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'tardis_report.log'
log_root = os.path.join(sys.path[0], 'logs')
if not os.path.exists(log_root):
    os.makedirs(log_root)
log_path = os.path.join(log_root, log_file)
if config['debug_logging'] == 'True' or 'true' or True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('tardis_report')
logger.setLevel(level=level)
fh = logging.FileHandler(filename=log_path)
fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
fh.setFormatter(fm)
logger.addHandler(fh)

logger.info('The TARDIS has started!')

# --------------------------------------------------------------------------------------------------
# Setup Shotgun Connection
# --------------------------------------------------------------------------------------------------
sg = sgapi.Shotgun(config['sg_url'], config['sg_name'], config['sg_key'])
logger.debug('Shotgun is connected.')

# --------------------------------------------------------------------------------------------------
# Connect Time Lord Components
# --------------------------------------------------------------------------------------------------
# setup continuum
logger.info('Opening a portal to the time continuum...')
tl_time = time_continuum.continuum(sg)
logger.info('time_continuum is opened...')

# Setup and get users
users = companions.companions(sg)
user = users.get_user_from_computer()
logger.info('User information collected...')

# setup shotgun data connection
sg_data = shotgun_collect.sg_data(sg)
logger.info('Shotgun commands brought in.')


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def query_mouse_position():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return {"x": pt.x, "y": pt.y}


# class chronograph(QtGui.QMainWindow):
#     def __init__(self):
#         super(chronograph, self).__init__(parent=None)
#         # Run the chronograph
#         self.chronograph()

def chronograph():
    '''
    This thread will process the timer events throughout the day.
    :return:
    '''
    set_timer = None
    sleep = 0.1
    timer_trigger = int(config['timer'])
    trigger = (timer_trigger * 60) / sleep

    # Set lunch timers
    start_time = parser.parse(config['approx_lunch_start']).time()
    end_time = parser.parse(config['approx_lunch_end']).time()
    lunch_start = None
    lunch_end = None
    lunch_timer = int(config['lunch_minutes'])
    lunch_break = lunch_timer * 60
    lunch_task_id = sg_data.get_lunch_task(lunch_proj_id=int(config['admin_proj_id']), task_name=config['lunch'])
    if lunch_task_id:
        lunch_task_id = lunch_task_id['id']
    lunch_timesheet = False

    # Set start and end of day
    sod = parser.parse(config['regular_start']).time()
    eod = parser.parse(config['regular_end'])
    eod_countdown = (eod - timedelta(minutes=timer_trigger)).time()
    eod = eod.time()
    user_clocked_in = tl_time.is_user_clocked_in(user=user)

    path = sys.path[0]
    minute = int(datetime.now().minute)

    # Part of temp count system
    temp_count = 0

    while True:
        pos = query_mouse_position()
        # print pos
        # print datetime.now().time()
        time.sleep(sleep)
        if pos == query_mouse_position():
            # -------------------------------------------------------------------------------------------------------
            # The mouse has stopped moving.
            # -------------------------------------------------------------------------------------------------------
            if not set_timer:
                # If there is no timer, create a timer
                set_timer = 1
            else:
                # Run the existing timer until the following conditions are met.
                if minute != int(datetime.now().minute):
                    minute = int(datetime.now().minute)
                    if not user_clocked_in:
                        user_clocked_in = tl_time.is_user_clocked_in(user=user)
                # --------------------------------------------------------------------------------------
                # Lunch Timer
                # --------------------------------------------------------------------------------------
                if sod > datetime.now().time():
                    # Reset the lunch_timesheet
                    lunch_timesheet = False
                if set_timer > trigger and start_time < datetime.now().time() < end_time and not lunch_start:
                    # The user has not moved their mouse in long enough to trigger a lunch break event.
                    logger.info('Start the Lunch Timer')
                    logger.info('Getting the most recent timesheet...')
                    if not lunch_timesheet:
                        # If lunch_timesheet is false, check it again to make sure that it hasn't since been added.
                        lunch_timesheet = tl_time.get_todays_lunch(user=user, lunch_id=lunch_task_id,
                                                                   lunch_proj_id=int(config['admin_proj_id']))
                    if not lunch_timesheet:
                        # If the lunch_timesheet is STILL false, THEN set the lunch start time
                        lunch_start = datetime.now() - timedelta(seconds=(trigger * sleep))
                        logger.debug('LUNCH HAS STARTED: %s' % lunch_start)
                    else:
                        logger.debug('Already has lunch!')
                        lunch_start = None

                # --------------------------------------------------------------------------------------
                # Start of Day
                # --------------------------------------------------------------------------------------

                # if not user_clocked_in and datetime.now().time() > sod:
                #     print 'Time to clock in!'
                #     while not tl_time.is_user_clocked_in(user=user):
                #         sod_launch_path = os.path.join(path, 'time_lord.py')
                #         sod_launch = subprocess.call('python.exe %s' % sod_launch_path)
                #         # sod_launch.wait()

                # --------------------------------------------------------------------------------------
                # End of Day
                # --------------------------------------------------------------------------------------
                if set_timer > trigger and datetime.now().time() > eod:
                    if tl_time.is_user_clocked_in(user=user):
                        print 'IT IS AFTER HOURS!!!'
                        eod_launch_path = os.path.join(path, 'eod.py')
                        get_lunch = subprocess.Popen('pythonw.exe %s' % eod_launch_path)
                        get_lunch.wait()
                        user_clocked_in = False
                set_timer += 1

                # Temp counter - Delete me
                if set_timer / 10 != temp_count:
                    temp_count = set_timer / 10
                    print temp_count
        else:
            # -------------------------------------------------------------------------------------------------------
            # The mouse IS moving
            # -------------------------------------------------------------------------------------------------------

            # -------------------------------------------------------------------------------------
            # Lunch Timer
            # -------------------------------------------------------------------------------------
            if set_timer > trigger and start_time < datetime.now().time() < end_time and lunch_start \
                    and (datetime.now() - lunch_start) > timedelta(seconds=lunch_break) and not lunch_timesheet:
                # If the timer has gone on long enough and been triggered...
                logger.info('End the lunch timer')
                lunch_end = datetime.now()
                print 'lunch start: %s' % lunch_start
                print 'lunch end  : %s' % lunch_end
                total_time = lunch_end - lunch_start
                print total_time
                print total_time.seconds

                # Pop up window, then set lunch break.
                if user_clocked_in:
                    lunch_launch_path = os.path.join(path, 'lunch.py')
                    get_lunch = subprocess.Popen('pythonw.exe %s -s "%s" -e "%s"' % (lunch_launch_path,
                                                                                    lunch_start.time(),
                                                                                    lunch_end.time()))
                    get_lunch.wait()
                    time.sleep(2)
            elif set_timer > trigger and datetime.now().time() > end_time and lunch_start \
                    and (datetime.now() - lunch_start) > timedelta(seconds=lunch_break):
                # If the user has been gone too long beyond lunch....
                if user_clocked_in:
                    logger.info('Gone too long.  Clocking out...')
                    lunch_timesheet = tl_time.get_last_timesheet(user=user)
                    clock_out = tl_time.clock_out_time_sheet(timesheet=lunch_timesheet, clock_out=lunch_start)

            # -----------------------------------------------------------------------------------------
            # End of Day
            # -----------------------------------------------------------------------------------------

            set_timer = None
            lunch_start = None
            lunch_end = None
            lunch_timesheet = False
            # print 'TIMER RESET'


# Setup Threading
logger.debug('Starting the chronograph thread...')
time_loop = threading.Thread(target=chronograph, name='Chronograph')
time_loop.setDaemon(True)
time_loop.start()


class tardis(object):
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]

    FIRST_ID = 1023

    def __init__(self,
                 icon,
                 hover_text,
                 menu_options,
                 on_quit=None,
                 default_menu_index=None,
                 window_class_name=None, ):

        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit

        menu_options = menu_options + (('Quit', None, self.QUIT),)
        self._next_action_id = self.FIRST_ID
        self.menu_actions_by_id = set()
        self.menu_options = self._add_ids_to_menu_options(list(menu_options))
        self.menu_actions_by_id = dict(self.menu_actions_by_id)
        del self._next_action_id

        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = window_class_name or "SysTrayIconPy"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.restart,
                       win32con.WM_DESTROY: self.destroy,
                       win32con.WM_COMMAND: self.command,
                       win32con.WM_USER + 20: self.notify, }
        # Register the Window class.
        window_class = win32gui.WNDCLASS()
        hinst = window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map  # could also specify a wndproc.
        classAtom = win32gui.RegisterClass(window_class)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(classAtom,
                                          self.window_class_name,
                                          style,
                                          0,
                                          0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0,
                                          0,
                                          hinst,
                                          None)
        win32gui.UpdateWindow(self.hwnd)
        self.notify_id = None
        self.refresh_icon()

        win32gui.PumpMessages()

    def _add_ids_to_menu_options(self, menu_options):
        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in self.SPECIAL_ACTIONS:
                self.menu_actions_by_id.add((self._next_action_id, option_action))
                result.append(menu_option + (self._next_action_id,))
            elif non_string_iterable(option_action):
                result.append((option_text,
                               option_icon,
                               self._add_ids_to_menu_options(option_action),
                               self._next_action_id))
            else:
                print 'Unknown item', option_text, option_icon, option_action
            self._next_action_id += 1
        return result

    def refresh_icon(self):
        # Try and find a custom icon
        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(self.icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                       self.icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)
        else:
            print "Can't find icon file - using default."
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id:
            message = win32gui.NIM_MODIFY
        else:
            message = win32gui.NIM_ADD
        self.notify_id = (self.hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER + 20,
                          hicon,
                          self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def restart(self, hwnd, msg, wparam, lparam):
        self.refresh_icon()

    def destroy(self, hwnd, msg, wparam, lparam):
        if self.on_quit: self.on_quit(self)
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

    def notify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONDBLCLK:
            self.execute_menu_option(self.default_menu_index + self.FIRST_ID)
        elif lparam == win32con.WM_RBUTTONUP:
            self.show_menu()
        elif lparam == win32con.WM_LBUTTONUP:
            pass
        return True

    def show_menu(self):
        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu, self.menu_options)
        # win32gui.SetMenuDefaultItem(menu, 1000, 0)

        pos = win32gui.GetCursorPos()
        # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.hwnd,
                                None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def create_menu(self, menu, menu_options):
        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = self.prep_menu_icon(option_icon)

            if option_id in self.menu_actions_by_id:
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                self.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(self, icon):
        # First load the icon.
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        # Fill the background.
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        # unclear if brush needs to be feed.  Best clue I can find is:
        # "GetSysColorBrush returns a cached brush instead of allocating a new
        # one." - implies no DeleteObject
        # draw the icon
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)

        return hbm

    def command(self, hwnd, msg, wparam, lparam):
        id = win32gui.LOWORD(wparam)
        self.execute_menu_option(id)

    def execute_menu_option(self, id):
        menu_action = self.menu_actions_by_id[id]
        if menu_action == self.QUIT:
            win32gui.DestroyWindow(self.hwnd)
        else:
            menu_action(self)


def non_string_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return not isinstance(obj, basestring)


# Minimal self test. You'll need a bunch of ICO files in the current working
# directory in order for this to work...
if __name__ == '__main__':

    icons = itertools.cycle(glob.glob('icons/*.ico'))
    # for i in icons:
    #     print i
    hover_text = "Time Lord TARDIS"


    def run_time_lord(tardis):
        # This will launch the Time Lord in a completely separate process
        path = sys.path[0]
        time_lord_path = os.path.join(path, 'time_lord.py')
        subprocess.Popen('pythonw.exe %s' % time_lord_path)


    def overtime(tardis):
        print "overtime."


    def lunch(tardis):
        # This will launch the Lunch Menu in a completely separate process
        path = sys.path[0]
        lunch_path = os.path.join(path, 'lunch.py')
        subprocess.Popen('pythonw.exe %s' % lunch_path)


    menu_options = (('Launch Time Lord', icons.next(), run_time_lord),
                    ('Tools', icons.next(), (('Overtime Tool', icons.next(), overtime),
                                             ('Lunch Break', icons.next(), lunch),
                                             ))
                    )


    def bye(tardis):
        # Tardis killer.  May need to eventually kill all other processes as well.
        print 'Why you quiting bro?'


    tardis(icons.next(), hover_text, menu_options, on_quit=bye, default_menu_index=0)


