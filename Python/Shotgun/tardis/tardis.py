import win32file
import win32con
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from pynput.mouse import Listener
import ConfigParser
import logging
import sys
import os
from PySide import QtCore, QtGui
from ctypes import windll, Structure, c_long, byref
import shotgun_api3 as sgapi
import time

from bin import companions, configuration, time_continuum, shotgun_collect

sys_path = sys.path

config = configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'tardis_report.log'
log_path = os.path.join(config['log_path'], log_file)
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
# tl_time = time_continuum(sg)
logger.info('time_continuum is opened...')

# Setup and get users
# users = companions(sg)
# user = users.get_user_from_computer()
logger.info('User information collected...')

# setup shotgun data connection
# sg_data = shotgun_collect.sg_data(sg)
logger.info('Shotgun commands brought in.')


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def query_mouse_position():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return {"x": pt.x, "y": pt.y}


class tardis(win32serviceutil.ServiceFramework):
    _svc_name_ = 'tardis'
    _svc_display_name_ = 'TARDIS'
    _svc_description_ = 'Time Lord Tardis Listener'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.time_flies = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()



    # def on_move(self, x, y):
    #     pass
    #
    # def on_click(self, x, y, button, pressed):
    #     test = QtGui.QMessageBox()
    #     test.setText('Fuck yeah: %s, %s' % (x, y))
    #     test.setInformativeText('Ooohhh La la!')
    #     test.setWindowTitle('Blows your fucking mind!!!')
    #     test.setDetailedText('Button pressed: %s' % button)
    #     test.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
    #
    #     test.exec_()
    #
    # def on_scroll(self, x, y, dx, dy):
    #     pass

    def main(self):
        # while self.time_flies:
        #     print 'Hello'
        set_timer = None
        while True:
            # with Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) as listener:
            #     listener.join()
            pos = query_mouse_position()
            logger.info('pre: %s' % pos)
            time.sleep(0.2)
            if pos == query_mouse_position():
                logger.info('post: %s' % query_mouse_position())
                if not set_timer:
                    set_timer = 1
                else:
                    if set_timer > 200:  # This will need to be set from configuration
                        logger.info('Start the lunch timer...')
                        '''
                        Might need to create a thread so I can check if is_running(): to keep from doubling up
                        on the iterations once the timer has started.
                        Also need to bring in configuration for various time start and stops.
                        First I need to convince PySide to work in a service, or get launched by a service
                        
                        '''
                    set_timer += 1
                logger.info('set timer: %s' % set_timer)
            else:
                set_timer = None
                logger.info(pos)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    win32serviceutil.HandleCommandLine(tardis)
