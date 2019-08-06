from ui import time_lord_lunch as tll
from PySide import QtGui, QtCore
import sys
import pprint
import time
import threading

# def shitTheBed(message=None):
#     print message
#     test = QtGui.QMessageBox()
#     if message:
#         test.setText(message)
#     test.addButton('Fart', QtGui.QMessageBox.YesRole)
#     test.addButton('Dookie', QtGui.QMessageBox.NoRole)
#     shit = test.exec_()
#     return shit

class bullshit_signals(QtCore.QObject):
    yes = QtCore.Signal(str)
    no = QtCore.Signal(str)
    jackshit = QtCore.Signal(str)
    timer = QtCore.Signal(str)

class other_thing(QtGui.QWidget):
    def __init__(self):
        super(other_thing, self).__init__(parent=None)

        self.bullshit = bullshit_signals()
        self.ui = tll.Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.yup)
        self.ui.pushButton_2.clicked.connect(self.nope)
        # self.show()

    def yup(self, message=None):
        self.bullshit.yes.emit(message)

    def nope(self, message=None):
        self.bullshit.no.emit(message)

    def closeEvent(self, event, *args, **kwargs):
        self.bullshit.jackshit.emit('Bullshit')
        event.ignore()

    def count_off(self):
        while True:
            self.bullshit.timer.emit('Dang')
            time.sleep(5)


class thing(QtGui.QMainWindow):
    def __init__(self):
        super(thing, self).__init__(parent=None)
        self.bullshit = other_thing()
        self.bullshit.bullshit.yes.connect(self.doit)
        self.bullshit.bullshit.no.connect(self.donttoit)
        self.bullshit.bullshit.jackshit.connect(self.uhuh)
        self.bullshit.bullshit.timer.connect(self.fuck_you)
        self.fuck_you()

    def fuck_you(self):
        self.bullshit.show()

    def doit(self):
        print 'It is Done!'
        self.bullshit.hide()

    def donttoit(self):
        print 'Skip it'
        self.bullshit.hide()

    def uhuh(self):
        self.bullshit.show()

    def closeEvent(self, event, *args, **kwargs):
        event.accept()


# t = threading.Thread(target=count_off)
# t.start()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = thing()
    w.show()
    sys.exit(app.exec_())
# app = QtGui.QApplication(sys.argv)
# bullshit = bullshit_signals()
# shit = other_thing()
# shit.ui.pushButton.connect()
# if bullshit.yes:
#     print 'hello'


#
# if shit == QtGui.QMessageBox.AcceptRole:
#     f = other_thing()
#     sys.exit(app.exec_())
#
# elif shit == QtGui.QMessageBox.RejectRole:
#     print 'Hell No'
# else:
#     print 'Damn.'
#
#
