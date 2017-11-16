# from libs.pynput import mouse
import ctypes
import sys
import time
from datetime import datetime

from Python.Utilities.t_sheets_listener.ui.PySide import QtGui
from ui import alert_dialog as ad


class ts_alert(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        print 'Fucking worked!'
        self.ui = ad.Ui_Dialog()
        self.ui.setupUi(self)


class ts_timer:
    """
    T-Sheets Listener Utility.
    This tool runs in the background of a computer to listen for mouse clicks at certain times of day, in order to run
    tasks that are dependent on a users login status.
    A user is clocked in and the time is between 12 and 2:30 - The timer starts looking for inactivity.  If inactive for
    more than 15 minutes, it will start a "lunch break" timer.  At the next click, it will assume the lunch break is
    over and will bring up a dialog box for confirmation.
    The user is clocked in and nearing their 8 hours - The timer pops up informing them that they have 15 minutes until
    they go into overtime.  This dialog does nothing else.
    It's after 7 and there has been no activity for 15 minutes.  Pops up a dialog with a count-down asking if the user
    is still working.  If no activity is detected again, it will clock them out and start their slave.
    """
    def __init__(self):
        self.run_time = True
        self.run_timer()
        self.alert_message = None

    def run_timer(self):
        s = 0
        m = 0
        h = 0
        r = 0.0
        break_timer = False
        start_break = None
        end_break = None
        ot_timer = False
        eod_timer = False
        while self.run_time:
            now_hour = datetime.now().hour
            now_min = datetime.now().minute
            r += 1.0
            t = float(r/1000)
            if t.is_integer():
                if s < 59:
                    s += 1
                else:
                    if m < 59:
                        s = 0
                        m += 1
                    elif m == 59 and h <= 22:
                        h += 1
                        m = 0
                        s = 0
                print '%s:%s:%s' % (h, m, s)
                now_time = datetime.strptime('%s:%s' % (now_hour, now_min), '%H:%M')
                lunch_start = datetime.strptime('12:00', '%H:%M')
                lunch_end = datetime.strptime('15:35', '%H:%M')
                if s >= 10 and not break_timer:
                    if lunch_start <= now_time < lunch_end:
                        # this will eventually be set to 15 minutes
                        start_break = datetime.now()  # - timedelta(minutes=1)
                        print 'Start Break At: %s' % start_break
                        break_timer = True

                        self.alert_message = ts_alert()
                        # Test launch slave
                        # The os.startfile works, but we'll need to test processor functions
                        # print dir(ctypes.windll.kernel32)
                        # os.startfile(r'C:\Program Files\Thinkbox\Deadline9\bin\deadlineslave.exe')

            if ctypes.windll.user32.GetKeyState(0x01) not in [0, 1]:
                if break_timer:
                    end_break = datetime.now()
                    break_time = end_break - start_break
                    print 'Open Lunch Menu'
                    break_timer = False
                    print 'Break Time: %s' % break_time

                s = 0
                m = 0
                h = 0
            time.sleep(0.001)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    run = ts_timer()
    sys.exit(app.exec_())


