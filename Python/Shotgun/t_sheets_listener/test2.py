
import ctypes
import sys
import time
from datetime import datetime

from ui import alert_dialog as ad
from ui import lunch_break_dialog as lbd

import sys, time
from PySide.QtGui import *
from PySide.QtCore import *

lunch_start_time = '00:00'
lunch_end_time = '23:59'


class ts_signal(QObject):
    # Perhaps here is where I would define different kinds of signals: Lunch break, alert, that sort of thing...
    # Perhaps...
    # ex:
    # sig = Signal(str)
    # otherSig = Signal(str)
    # Then, below, it would connect like self.signal.otherSig.connect(self.function)
    sig = Signal(str)
    lunch = Signal(str)
    alert = Signal(str)


class ts_timer(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False
        self.signal = ts_signal()

    def run(self):
        s = 0
        m = 0
        h = 0
        r = 0.0
        break_timer = False
        start_break = None
        end_break = None
        ot_timer = False
        eod_timer = False
        while not self.exiting:
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
                lunch_start = datetime.strptime(lunch_start_time, '%H:%M')
                lunch_end = datetime.strptime(lunch_end_time, '%H:%M')
                if s >= 5 and not break_timer:
                    if lunch_start <= now_time < lunch_end:
                        # this will eventually be set to 15 minutes
                        start_break = datetime.now()  # - timedelta(minutes=1)
                        break_timer = True
                        print 'Start Break At: %s' % start_break

            if ctypes.windll.user32.GetKeyState(0x01) not in [0, 1]:
                if break_timer:
                    end_break = datetime.now()
                    break_time = end_break - start_break
                    print 'Open Lunch Menu'
                    break_timer = False
                    print 'Break Time: %s' % break_time
                    # self.alert_message = ts_alert()
                    # self.alert_message.show()
                    self.signal.lunch.emit('"startBreak": %s, "endBreak": %s, "breakTotal": %s' % (start_break,
                                                                                                   end_break,
                                                                                                   break_time))

                s = 0
                m = 0
                h = 0
            time.sleep(0.001)

        # The Following is where I would put my timer math and triggers and shit... I think.
        # end = time.time()+10
        # while self.exiting==False:
        #     sys.stdout.write('*')
        #     sys.stdout.flush()
        #     time.sleep(1)
        #     now = time.time()
        #     if now>=end:
        #         self.exiting=True

        # If what I figured out is correct in the ts_signal(), then in order to trigger one dialog or another,
        # I would need different Signal(str) setup and then triggered from the timer loop.

        # self.signal.sig.emit('OK')
        # self.signal.alert.emit('Can this be anything?')



class ts_thread(QThread):
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.exiting = False

    def run(self):
        while self.exiting==False:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1)


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

        # Connect the Threads
        self.thread = ts_thread()
        self.run_ts_timer = ts_timer()

        self.batchbutton.clicked.connect(self.handletoggle)
        self.longbutton.clicked.connect(self.start_ts_timer)
        self.thread.started.connect(self.started)
        self.thread.finished.connect(self.finished)
        self.thread.terminated.connect(self.terminated)

        # Here, the long thread def (in my case this would be like a dialog window opening) is connected to the ts_main
        # def longoperationcomplete, which resides in this class.  This dynamically updates the main window.
        # I will want to do similar things with the dialog boxes.
        # The following line connects ANY signal from the ts_timer to the longoperationcomplete
        self.run_ts_timer.signal.lunch.connect(self.open_lunch_break)
        # I think I may have figured this out in the ts_signal() class.  See above.
        # It also means that longoperationcomlete() should be one of the dialog boxes.
        # The next catch is... how do I run a Dialog box, and how do I pass data to it.  Perhaps, multiple signals?

        # This is me just test-running another class from a hidden window.
        self.start_ts_timer()
        '''
        So... Here I would have 'longoperation()' be like my timer.  Or, rather/perhaps the MyLongThread() class would
        be the timer, and longoperation just starts it.  Then that would/might send out signals to operations that open
        other dialog boxes.
        This is going to be tricky.
        '''

    def started(self):
        self.label1.setText('Continuous batch started')

    def finished(self):
        self.label1.setText('Continuous batch stopped')

    def terminated(self):
        self.label1.setText('Continuous batch terminated')

    def handletoggle(self):
        if self.thread.isRunning():
            self.thread.exiting=True
            self.batchbutton.setEnabled(False)
            while self.thread.isRunning():
                time.sleep(0.01)
                continue
            self.batchbutton.setText('Start batch')
            self.batchbutton.setEnabled(True)
        else:
            self.thread.exiting=False
            self.thread.start()
            self.batchbutton.setEnabled(False)
            while not self.thread.isRunning():
                time.sleep(0.01)
                continue
            self.batchbutton.setText('Stop batch')
            self.batchbutton.setEnabled(True)

    def start_ts_timer(self):
        # This method simply starts the timer.
        if not self.run_ts_timer.isRunning():
            self.run_ts_timer.exiting=False
            self.run_ts_timer.start()
            # The following two lines are specific to this example, and not necessary.
            self.label2.setText('Long operation started')
            self.longbutton.setEnabled(False)

    def open_lunch_break(self, data=None):
        print data
        self.lunch_dialog = QDialog(self)
        self.lunch_ui = lbd.Ui_Dialog()
        self.lunch_ui.setupUi(self.lunch_dialog)
        self.lunch_ui.yes_btn.clicked.connect(self.save_lunch_break)
        self.lunch_dialog.exec_()

    def save_lunch_break(self):
        print 'Save lunch break'
        test_signal = self.lunch_dialog.finished
        if test_signal:
            self.lunch_dialog.close()


if __name__=='__main__':
    # Set up the app
    app = QApplication(sys.argv)
    # Run ts_main hidden
    window = ts_main()
    # window.show()
    window.hide()
    sys.exit(app.exec_())