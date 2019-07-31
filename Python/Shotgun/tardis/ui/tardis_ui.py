# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Shotgun\tardis\ui\tardis_ui.ui'
#
# Created: Wed Jul 31 14:19:02 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_tardis(object):
    def setupUi(self, tardis):
        tardis.setObjectName("tardis")
        tardis.resize(96, 137)
        tardis.setMinimumSize(QtCore.QSize(96, 137))
        tardis.setMaximumSize(QtCore.QSize(164, 203))
        tardis.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout = QtGui.QVBoxLayout(tardis)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtGui.QLabel(tardis)
        self.title.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.line = QtGui.QFrame(tardis)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.timelord_btn = QtGui.QPushButton(tardis)
        self.timelord_btn.setObjectName("timelord_btn")
        self.verticalLayout.addWidget(self.timelord_btn)
        self.overtime_btn = QtGui.QPushButton(tardis)
        self.overtime_btn.setObjectName("overtime_btn")
        self.verticalLayout.addWidget(self.overtime_btn)
        self.lunch_btn = QtGui.QPushButton(tardis)
        self.lunch_btn.setObjectName("lunch_btn")
        self.verticalLayout.addWidget(self.lunch_btn)

        self.retranslateUi(tardis)
        QtCore.QMetaObject.connectSlotsByName(tardis)

    def retranslateUi(self, tardis):
        tardis.setWindowTitle(QtGui.QApplication.translate("tardis", "TARDIS", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("tardis", "TARDIS", None, QtGui.QApplication.UnicodeUTF8))
        self.timelord_btn.setText(QtGui.QApplication.translate("tardis", "Time Lord", None, QtGui.QApplication.UnicodeUTF8))
        self.overtime_btn.setText(QtGui.QApplication.translate("tardis", "Overtime Tool", None, QtGui.QApplication.UnicodeUTF8))
        self.lunch_btn.setText(QtGui.QApplication.translate("tardis", "Lunch Tool", None, QtGui.QApplication.UnicodeUTF8))

