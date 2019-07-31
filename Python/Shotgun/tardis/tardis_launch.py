import win32file
import win32con
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import psutil
import subprocess
from pynput.mouse import Listener
import ConfigParser
import logging
import sys
import os
from PySide import QtCore, QtGui
from ctypes import windll, Structure, c_long, byref


class tardis_launch(win32serviceutil.ServiceFramework):
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

    def main(self):
        while True:
            test = True
            for proc in psutil.process_iter():
                try:
                    if 'notepad.exe' == proc.name().lower():
                        test = False
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            if test:
                subprocess.Popen('C:\\Users\\adamb\\OneDrive\\Documents\\Scripts\\Python\\Shotgun\\tardis\\launch_notepad.bat')


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(tardis_launch)
