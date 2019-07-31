import sys
from PySide import QtGui, QtCore


def window():
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    b = QtGui.QPushButton(w)
    b.setText("Show message!")

    b.move(50, 50)
    b.clicked.connect(showdialog)
    w.setWindowTitle("PyQt Dialog demo")
    w.hide()
    showdialog()
    sys.exit(app.exec_())


def showdialog():
    msg = QtGui.QMessageBox()
    msg.setIcon(QtGui.QMessageBox.Information)

    msg.setText("This is a message box")
    msg.setInformativeText("This is additional information")
    msg.setWindowTitle("MessageBox demo")
    msg.setDetailedText("The details are as follows:")
    msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
    msg.buttonClicked.connect(msgbtn)

    retval = msg.exec_()
    print "value of pressed message box button:", retval


def msgbtn(i):
    print "Button pressed is:", i.text()


if __name__ == '__main__':
    window()