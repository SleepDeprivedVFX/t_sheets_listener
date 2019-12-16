#!python
from __future__ import print_function

try:
    import win32service as svc
    import win32serviceutil as svcutil
except ImportError:
    print("wtsmonitor-svc: PyWin32 modules not found", file=sys.stderr)
    sys.exit(1)

import wtsmonitor


class WTSMonitorService(svcutil.ServiceFramework):
    _svc_name_ = "WTSMonitor"
    _svc_display_name_ = "Terminal Services event monitor"
    _svc_description_ = "Runs custom actions on Terminal Services session events."
    _svc_deps_ = ["TermService"]

    m = None

    def SvcStop(self):
        self.ReportServiceStatus(svc.SERVICE_STOP_PENDING)
        self.m.stop()
        self.ReportServiceStatus(svc.SERVICE_STOPPED)

    def SvcDoRun(self):
        self.m = wtsmonitor.WTSMonitor(all_sessions=True)
        self.m.start()


if __name__ == '__main__':
    svcutil.HandleCommandLine(WTSMonitorService)
