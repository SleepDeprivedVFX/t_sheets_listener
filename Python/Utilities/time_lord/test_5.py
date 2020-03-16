from PySide2 import QtCore, QtWidgets, QtGui

test_signal = QtCore.SIGNAL('fart')


class test_1(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        test_signal.connect(self.shit)

    def shit(self):
        print('First Shit worked.')


class test_2(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        test_signal.connect(self.dick)

    def run(self):
        print('Foo')

    def dick(self):
        print('dick')


class test_3():
    t1 = test_1
    t2 = test_2

    emit('Fuck')


test_3()

