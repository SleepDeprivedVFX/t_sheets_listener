from PySide.QtCore import *
from PySide.QtGui import *
import time
from datetime import datetime, timedelta
import sys, os, ctypes
from ui import alert_dialog as ad


class ts_loop(QThread):
    def __init__(self):
        QThread.__init__(self)

    def loop_gen(self):
        self.emit(SIGNAL('doIt()'))


class ts_alert(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.alert = ad.Ui_Dialog()
        self.alert.setupUi(self)

    def fuck(self):
        self.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = ts_alert(QObject)
    # QObject.connect(ts_loop, SIGNAL('doIt()'), a.fuck, Qt.QueuedConnection)
    a.start()
    sys.exit(app.exec_())
