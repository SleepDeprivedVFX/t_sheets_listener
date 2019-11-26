from PySide import QtCore, QtGui
from time import sleep
import sys

mutex = QtCore.QMutex()
waitCond = QtCore.QWaitCondition()


class signals(QtCore.QObject):
    sig = QtCore.Signal(bool)


class test1(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.signals = signals()
        self.stop = False
        self.signals.sig.connect(self.set_stop)

    def run(self, *args, **kwargs):
        self.do_something1()

    def set_stop(self, message=False):
        print('Setting stop: %s' % message)
        self.stop = message

    def do_something1(self):
        print('Doing something...')
        i = 1
        while True:
            if self.stop:
                waitCond.wait(mutex)
            print(i)
            i += 1
            sleep(1)


class test2(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.t1 = test1()

    def run(self, *args, **kwargs):
        self.t1.start()
        self.other_thing()

    def other_thing(self):
        mutexLock = QtCore.QMutexLocker(mutex)
        x = 200
        j = True
        while j:
            self.t1.signals.sig.emit(True)
            # mutex.lock()
            sleep(1.2)
            if x > 205:
                self.t1.signals.sig.emit(False)
                waitCond.wakeAll()
                j = False
            else:
                print x
                x += 1
            # mutex.unlock()
        waitCond.wakeAll()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    # t1 = test1()
    t2 = test2()
    # t1.start()
    t2.start()
    sys.exit(app.exec_())
