
import ctypes
import sys
import time
from datetime import datetime, timedelta

from ui import alert_dialog as ad
from ui import lunch_break_dialog as lbd

import sys, time
from PySide.QtGui import *
from PySide.QtCore import *

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

# Create a SG Database for the following.
lunch_start_time = datetime.strptime('00:00:00', '%H:%M:%S')
lunch_end_time = datetime.strptime('23:59:59', '%H:%M:%S')
timer_seconds = 240
ts_buffer = QWaitCondition()
buffer_not_full = QWaitCondition()
mutex = QMutex()


class ts_signal(QObject):
    sig = Signal(str)
    lunch = Signal(str)
    alert = Signal(str)


class ts_timer(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.running = True
        self.signal = ts_signal()
        self.lunch_break = False
        ch = datetime.now().hour
        cm = datetime.now().minute
        cs = datetime.now().second
        self.click_time = datetime.strptime('%s:%s:%s' % (ch, cm, cs), '%H:%M:%S')

    def run(self, *args, **kwargs):
        break_timer = False
        break_start = None
        break_end = None
        while self.running:
            ch = datetime.now().hour
            cm = datetime.now().minute
            cs = datetime.now().second
            ct = datetime.strptime('%s:%s:%s' % (ch, cm, cs), '%H:%M:%S')
            if ctypes.windll.user32.GetKeyState(0x01) not in [0, 1] and not break_timer:
                self.click_time = ct
            elapsed = (ct - self.click_time).seconds
            if elapsed >= timer_seconds and not break_timer:
                if lunch_start_time <= ct < lunch_end_time:
                    break_timer = True
                    break_start = ct
                    print 'Break Start: %s' % break_start
            if ctypes.windll.user32.GetKeyState(0x01) not in [0, 1] and break_timer:
                break_end = ct
                print 'Break End: %s' % break_end
                self.click_time = ct
                self.signal.lunch.emit('{"start": %s, "end": %s' % (break_start, break_end))
                break_timer = False
                break_start = None
                break_end = None


class ts_main(QMainWindow):
    """
    Opens from the if __name__ == '__main__' routine
    """
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)

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

        # Connect the Threads
        # self.thread = ts_thread()
        self.run_ts_timer = ts_timer()
        self.run_ts_timer.signal.lunch.connect(self.open_lunch_break)
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

    def open_lunch_break(self, data=None):
        print data
        ts_buffer.wakeAll()
        self.lunch_dialog = QDialog(self)
        self.lunch_ui = lbd.Ui_Dialog()
        self.lunch_ui.setupUi(self.lunch_dialog)
        self.lunch_ui.yes_btn.clicked.connect(self.save_lunch_break)
        self.lunch_dialog.exec_()

    def save_lunch_break(self):
        print 'Save lunch break'
        # mutex.lock()
        # ts_buffer.wait(mutex)
        test_signal = self.lunch_dialog.finished
        if test_signal:
            self.lunch_dialog.hide()
            # self.run_ts_timer.exiting = False
            if not self.run_ts_timer.isRunning():
                print 'Not running...'
                # self.run_ts_timer.run()
        # mutex.unlock()


if __name__=='__main__':
    # Set up the app
    app = QApplication(sys.argv)
    # Run ts_main hidden
    window = ts_main()
    # window.show()
    window.hide()
    sys.exit(app.exec_())
