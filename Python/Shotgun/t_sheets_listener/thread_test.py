from PySide.QtGui import *
from PySide.QtCore import *
import sys, os, subprocess, platform, ctypes
import time
from datetime import datetime, timedelta
import threading as th
from ui import alert_dialog as alert
from ui import lunch_break_dialog as lunch


class alert_message_dialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.alert_ui = None
        self.alert_ui = alert.Ui_Dialog()
        self.alert_ui.setupUi(self)
        self.alert_ui.ok_btn.clicked.connect(self.cancel_thread)

    def run(self):
        self.runThread()
        self.exec_()

    def runThread(self):
        QObject.connect(self.worker_thread, SIGNAL('Alert'), self.run_alert)
        self.worker_thread.start()

    def run_alert(self):
        print 'THIS WAS CALLED FROM THE SIGNAL'
        self.show()

    def cancel_thread(self):
        self.worker_thread.stop()


class worker_thread(QThread):
    def __init__(self, parentThread):
        QThread.__init__(self, parentThread)
        self.alert_dialog = alert_message_dialog()
        self.alert_ui = None

    def run(self):
        self.running = True
        success = self.do_work()
        print 'SUCCESS = %s' % success
        self.emit(SIGNAL('Alert'), success)

    def stop(self):
        self.running = False
        pass

    def do_work(self):
        # Not sure what else this is supposed to do now.
        self.alert_ui = alert.Ui_Dialog()
        self.alert_ui.setupUi()
        self.alert_ui.ok_btn.clicked.connect(self.stop)
        self.show()
        self.start()
        return True

    def clean_up(self):
        pass


class ts_timer(worker_thread):
    def __init__(self, parentThread):
        worker_thread.__init__(self, parentThread)
        self.running = True

    def ts_time_loop(self):
        # Make the timer its own thread with signals
        s = 0
        m = 0
        h = 0
        r = 0.0
        break_timer = False
        start_break = None
        end_break = None
        ot_timer = False
        eod_timer = False
        while self.running:
            now_hour = datetime.now().hour
            now_min = datetime.now().minute
            r += 1.0
            t = float(r / 1000)
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
                lunch_start = datetime.strptime('0:00', '%H:%M')
                lunch_end = datetime.strptime('23:59', '%H:%M')
                if s >= 5 and not break_timer:
                    if lunch_start <= now_time < lunch_end:
                        # this will eventually be set to 15 minutes
                        start_break = datetime.now()  # - timedelta(minutes=1)
                        print 'Start Break At: %s' % start_break
                        break_timer = True
                        # Send a signal instead of opening the thread
                        self.emit(SIGNAL('Alert'), alert_message_dialog)
                        # subprocess.Popen(r'C:\Program Files (x86)\Notepad++\notepad++.exe')

            if ctypes.windll.user32.GetKeyState(0x01) not in [0, 1]:
                if break_timer:
                    end_break = datetime.now()
                    break_time = end_break - start_break
                    # Send a signal instead
                    print 'Open Lunch Menu'
                    break_timer = False
                    print 'Break Time: %s' % break_time

                s = 0
                m = 0
                h = 0
            time.sleep(0.001)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     myapp = ts_timer(app)
#     myapp.ts_time_loop()
#     sys.exit(app.exec_())
d = alert_message_dialog(alert.Ui_Dialog)
d.worker_thread = worker_thread(alert_message_dialog)
d.run()


