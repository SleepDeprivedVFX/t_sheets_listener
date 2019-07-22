import win32file
import win32con
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from pynput.mouse import Listener
import ConfigParser
import sys
import os

sys_path = sys.path
config_file = 'tardis_config.cfg'
configuration = ConfigParser.ConfigParser()
configuration.read(config_file)
# print configuration.get('Time Lord', 'regular_days')


class tardis(win32serviceutil.ServiceFramework):
    _svc_name_ = 'tardis'
    _svc_display_name_ = 'TARDIS'

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

    def main(self):
        while self.time_flies:
            print 'Hello'


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(tardis)
