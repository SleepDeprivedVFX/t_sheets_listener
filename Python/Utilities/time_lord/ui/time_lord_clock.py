# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_clock.ui'
#
# Created: Fri Jun 07 15:21:26 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_TimeLord(object):
    def setupUi(self, TimeLord):
        TimeLord.setObjectName("TimeLord")
        TimeLord.resize(687, 572)
        TimeLord.setStyleSheet("QWidget{\n"
"background-color: rgb(100, 100, 100);\n"
"selection-color: rgb(115, 115, 115);\n"
"selection-background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);\n"
"}\n"
"\n"
"QMenuBar {\n"
"  background-color: rgb(90, 90, 90);\n"
"  padding: 2px;\n"
"  border: 1px solid #19232D;\n"
"  color: #F0F0F0;\n"
"}\n"
"\n"
"QMenuBar:focus {\n"
"  border: 1px solid #148CD2;\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"  background: transparent;\n"
"  padding: 4px;\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"  padding: 4px;\n"
"  background: transparent;\n"
"  border: 0px solid #32414B;\n"
"}\n"
"\n"
"QMenuBar::item:pressed {\n"
"  padding: 4px;\n"
"  border: 0px solid #32414B;\n"
"  background-color: #148CD2;\n"
"  color: #F0F0F0;\n"
"  margin-bottom: 0px;\n"
"  padding-bottom: 0px;\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.centralwidget = QtGui.QWidget(TimeLord)
        self.centralwidget.setObjectName("centralwidget")
        self.analogClock = AnalogClock(self.centralwidget)
        self.analogClock.setGeometry(QtCore.QRect(30, 70, 141, 131))
        self.analogClock.setStyleSheet("")
        self.analogClock.setInputMethodHints(QtCore.Qt.ImhNone)
        self.analogClock.setObjectName("analogClock")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 10, 161, 31))
        self.label.setStyleSheet("font: 24pt \"Arial\";")
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 340, 46, 13))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(80, 340, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 380, 71, 16))
        self.label_3.setObjectName("label_3")
        self.comboBox_2 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 380, 69, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 420, 46, 13))
        self.label_4.setObjectName("label_4")
        self.comboBox_3 = QtGui.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(80, 410, 69, 22))
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
        self.pushButton.setGeometry(QtCore.QRect(540, 450, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 450, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(60, 290, 46, 13))
        self.label_7.setObjectName("label_7")
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(230, 160, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(230, 130, 71, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(450, 130, 71, 16))
        self.label_9.setObjectName("label_9")
        self.progressBar_2 = QtGui.QProgressBar(self.centralwidget)
        self.progressBar_2.setGeometry(QtCore.QRect(430, 160, 118, 23))
        self.progressBar_2.setProperty("value", 24)
        self.progressBar_2.setObjectName("progressBar_2")
        self.start_time_clock = AnalogClock(self.centralwidget)
        self.start_time_clock.setGeometry(QtCore.QRect(230, 230, 100, 100))
        self.start_time_clock.setObjectName("start_time_clock")
        self.end_time_clock = AnalogClock(self.centralwidget)
        self.end_time_clock.setGeometry(QtCore.QRect(450, 220, 100, 100))
        self.end_time_clock.setObjectName("end_time_clock")
        TimeLord.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(TimeLord)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 687, 30))
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
        self.pushButton_2.setText(QtGui.QApplication.translate("TimeLord", "Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("TimeLord", "Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("TimeLord", "Daily Total", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("TimeLord", "Weekly Total", None, QtGui.QApplication.UnicodeUTF8))
        self.start_time_clock.setToolTip(QtGui.QApplication.translate("TimeLord", "The current time", None, QtGui.QApplication.UnicodeUTF8))
        self.start_time_clock.setWhatsThis(QtGui.QApplication.translate("TimeLord", "The analog clock widget displays the current time.", None, QtGui.QApplication.UnicodeUTF8))
        self.end_time_clock.setToolTip(QtGui.QApplication.translate("TimeLord", "The current time", None, QtGui.QApplication.UnicodeUTF8))
        self.end_time_clock.setWhatsThis(QtGui.QApplication.translate("TimeLord", "The analog clock widget displays the current time.", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOptions.setTitle(QtGui.QApplication.translate("TimeLord", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCrash_Computer.setText(QtGui.QApplication.translate("TimeLord", "Crash Computer", None, QtGui.QApplication.UnicodeUTF8))

from analogclock import AnalogClock
