from PySide.QtGui import *
from PySide.QtCore import *
import sys, os, subprocess, platform, ctypes
import time
from ui import alert_dialog


class popup(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = alert_dialog.Ui_Dialog
        self.ui.setupUi(self)
        self.ui.ok_btn.clicked.connect(self.shut_off)
        self.show()

    def run(self):
        print 'Hello'

    def shut_off(self):
        self.close()
        return


class ts_timer(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.worker = None
        self.slave = None
        self.run()

    def run(self):
        self.slave = QDialog()
        self.worker = popup()
        self.worker.moveToThread(self.slave)
        self.worker.connect(self.worker, SIGNAL(self.slave.started()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = ts_timer()
    sys.exit(app.exec_())



