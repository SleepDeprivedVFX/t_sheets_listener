
import ctypes
import sys
import time
from datetime import datetime

from ui import alert_dialog as ad

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
        # The Following is where I would put my timer math and triggers and shit... I think.
        end = time.time()+10
        while self.exiting==False:
            sys.stdout.write('*')
            sys.stdout.flush()
            time.sleep(1)
            now = time.time()
            if now>=end:
                self.exiting=True

        # If what I figured out is correct in the ts_signal(), then in order to trigger one dialog or another,
        # I would need different Signal(str) setup and then triggered from the timer loop.
        self.signal.sig.emit('OK')
        self.signal.alert.emit('Can this be anything?')
        self.signal.lunch.emit('Maybe: this, Can: too')



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
        self.run_ts_timer.signal.sig.connect(self.longoperationcomplete)
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

    def longoperationcomplete(self,data):
        self.label2.setText('Long operation completed with: '+data)
        self.longbutton.setEnabled(True)


if __name__=='__main__':
    # Set up the app
    app = QApplication(sys.argv)
    # Run ts_main hidden
    window = ts_main()
    # window.show()
    window.hide()
    sys.exit(app.exec_())