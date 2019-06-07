# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_clock.ui'
#
# Created: Wed May 29 15:44:50 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_TimeLord(object):
    def setupUi(self, TimeLord):
        TimeLord.setObjectName("TimeLord")
        TimeLord.resize(687, 572)
        TimeLord.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"selection-color: rgb(115, 115, 115);\n"
"selection-background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.centralwidget = QtGui.QWidget(TimeLord)
        self.centralwidget.setObjectName("centralwidget")
        self.analogClock = AnalogClock(self.centralwidget)
        self.analogClock.setGeometry(QtCore.QRect(100, 110, 141, 131))
        self.analogClock.setStyleSheet("")
        self.analogClock.setInputMethodHints(QtCore.Qt.ImhNone)
        self.analogClock.setObjectName("analogClock")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 30, 161, 31))
        self.label.setStyleSheet("font: 24pt \"Arial\";")
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(380, 120, 46, 13))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(430, 120, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(380, 170, 71, 16))
        self.label_3.setObjectName("label_3")
        self.comboBox_2 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(430, 200, 69, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(390, 250, 46, 13))
        self.label_4.setObjectName("label_4")
        self.comboBox_3 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(430, 260, 69, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(210, 360, 81, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(430, 350, 46, 13))
        self.label_6.setObjectName("label_6")
        self.dateTimeEdit = QtGui.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit.setGeometry(QtCore.QRect(210, 380, 194, 22))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.dateTimeEdit_2 = QtGui.QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit_2.setGeometry(QtCore.QRect(430, 380, 194, 22))
        self.dateTimeEdit_2.setObjectName("dateTimeEdit_2")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(460, 450, 75, 23))
        self.pushButton.setObjectName("pushButton")
        TimeLord.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(TimeLord)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 687, 21))
        self.menubar.setObjectName("menubar")
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")
        TimeLord.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(TimeLord)
        self.statusbar.setObjectName("statusbar")
        TimeLord.setStatusBar(self.statusbar)
        self.actionCrash_Computer = QtGui.QAction(TimeLord)
        self.actionCrash_Computer.setObjectName("actionCrash_Computer")
        self.menuOptions.addAction(self.actionCrash_Computer)
        self.menubar.addAction(self.menuOptions.menuAction())

        self.retranslateUi(TimeLord)
        QtCore.QMetaObject.connectSlotsByName(TimeLord)

    def retranslateUi(self, TimeLord):
        TimeLord.setWindowTitle(QtGui.QApplication.translate("TimeLord", "Time Lord", None, QtGui.QApplication.UnicodeUTF8))
        self.analogClock.setToolTip(QtGui.QApplication.translate("TimeLord", "The current time", None, QtGui.QApplication.UnicodeUTF8))
        self.analogClock.setWhatsThis(QtGui.QApplication.translate("TimeLord", "The analog clock widget displays the current time.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("TimeLord", "Time Lord", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("TimeLord", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("TimeLord", "Asset / Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("TimeLord", "Task", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("TimeLord", "Start Time", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("TimeLord", "End Time", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("TimeLord", "Clock In", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOptions.setTitle(QtGui.QApplication.translate("TimeLord", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCrash_Computer.setText(QtGui.QApplication.translate("TimeLord", "Crash Computer", None, QtGui.QApplication.UnicodeUTF8))

from analogclock import AnalogClock
