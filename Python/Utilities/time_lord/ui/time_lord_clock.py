# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_clock.ui'
#
# Created: Thu Jun 20 17:31:22 2019
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
        self.time_lord_title = QtGui.QLabel(self.centralwidget)
        self.time_lord_title.setGeometry(QtCore.QRect(500, 70, 161, 31))
        self.time_lord_title.setStyleSheet("font: 24pt \"Arial\";")
        self.time_lord_title.setObjectName("time_lord_title")
        self.project_label = QtGui.QLabel(self.centralwidget)
        self.project_label.setGeometry(QtCore.QRect(30, 340, 46, 13))
        self.project_label.setObjectName("project_label")
        self.project_dropdown = QtGui.QComboBox(self.centralwidget)
        self.project_dropdown.setGeometry(QtCore.QRect(80, 340, 69, 22))
        self.project_dropdown.setObjectName("project_dropdown")
        self.asset_shot_label = QtGui.QLabel(self.centralwidget)
        self.asset_shot_label.setGeometry(QtCore.QRect(10, 380, 71, 16))
        self.asset_shot_label.setObjectName("asset_shot_label")
        self.asset_shot_progress = QtGui.QComboBox(self.centralwidget)
        self.asset_shot_progress.setGeometry(QtCore.QRect(80, 380, 69, 22))
        self.asset_shot_progress.setObjectName("asset_shot_progress")
        self.task_label = QtGui.QLabel(self.centralwidget)
        self.task_label.setGeometry(QtCore.QRect(30, 420, 46, 13))
        self.task_label.setObjectName("task_label")
        self.task_progress = QtGui.QComboBox(self.centralwidget)
        self.task_progress.setGeometry(QtCore.QRect(80, 410, 69, 22))
        self.task_progress.setObjectName("task_progress")
        self.start_time_label = QtGui.QLabel(self.centralwidget)
        self.start_time_label.setGeometry(QtCore.QRect(210, 360, 81, 16))
        self.start_time_label.setObjectName("start_time_label")
        self.end_time_label = QtGui.QLabel(self.centralwidget)
        self.end_time_label.setGeometry(QtCore.QRect(430, 350, 46, 13))
        self.end_time_label.setObjectName("end_time_label")
        self.start_time = QtGui.QDateTimeEdit(self.centralwidget)
        self.start_time.setGeometry(QtCore.QRect(210, 380, 194, 22))
        self.start_time.setObjectName("start_time")
        self.end_time = QtGui.QDateTimeEdit(self.centralwidget)
        self.end_time.setGeometry(QtCore.QRect(430, 380, 194, 22))
        self.end_time.setObjectName("end_time")
        self.clock_button = QtGui.QPushButton(self.centralwidget)
        self.clock_button.setGeometry(QtCore.QRect(540, 450, 75, 23))
        self.clock_button.setObjectName("clock_button")
        self.switch_button = QtGui.QPushButton(self.centralwidget)
        self.switch_button.setGeometry(QtCore.QRect(240, 450, 75, 23))
        self.switch_button.setObjectName("switch_button")
        self.artist_label = QtGui.QLabel(self.centralwidget)
        self.artist_label.setGeometry(QtCore.QRect(60, 290, 46, 13))
        self.artist_label.setObjectName("artist_label")
        self.daily_total_progress = QtGui.QProgressBar(self.centralwidget)
        self.daily_total_progress.setGeometry(QtCore.QRect(230, 160, 118, 23))
        self.daily_total_progress.setProperty("value", 24)
        self.daily_total_progress.setObjectName("daily_total_progress")
        self.daily_total_label = QtGui.QLabel(self.centralwidget)
        self.daily_total_label.setGeometry(QtCore.QRect(230, 130, 71, 16))
        self.daily_total_label.setObjectName("daily_total_label")
        self.weekly_total_label = QtGui.QLabel(self.centralwidget)
        self.weekly_total_label.setGeometry(QtCore.QRect(450, 130, 71, 16))
        self.weekly_total_label.setObjectName("weekly_total_label")
        self.weekly_total_progress = QtGui.QProgressBar(self.centralwidget)
        self.weekly_total_progress.setGeometry(QtCore.QRect(430, 160, 118, 23))
        self.weekly_total_progress.setProperty("value", 24)
        self.weekly_total_progress.setObjectName("weekly_total_progress")
        self.test_counter = QtGui.QLabel(self.centralwidget)
        self.test_counter.setGeometry(QtCore.QRect(100, 30, 46, 13))
        self.test_counter.setObjectName("test_counter")
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
        self.time_lord_title.setText(QtGui.QApplication.translate("TimeLord", "Time Lord", None, QtGui.QApplication.UnicodeUTF8))
        self.project_label.setText(QtGui.QApplication.translate("TimeLord", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.asset_shot_label.setText(QtGui.QApplication.translate("TimeLord", "Asset / Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.task_label.setText(QtGui.QApplication.translate("TimeLord", "Task", None, QtGui.QApplication.UnicodeUTF8))
        self.start_time_label.setText(QtGui.QApplication.translate("TimeLord", "Start Time", None, QtGui.QApplication.UnicodeUTF8))
        self.end_time_label.setText(QtGui.QApplication.translate("TimeLord", "End Time", None, QtGui.QApplication.UnicodeUTF8))
        self.clock_button.setText(QtGui.QApplication.translate("TimeLord", "Clock In", None, QtGui.QApplication.UnicodeUTF8))
        self.switch_button.setText(QtGui.QApplication.translate("TimeLord", "Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.artist_label.setText(QtGui.QApplication.translate("TimeLord", "Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.daily_total_label.setText(QtGui.QApplication.translate("TimeLord", "Daily Total", None, QtGui.QApplication.UnicodeUTF8))
        self.weekly_total_label.setText(QtGui.QApplication.translate("TimeLord", "Weekly Total", None, QtGui.QApplication.UnicodeUTF8))
        self.test_counter.setText(QtGui.QApplication.translate("TimeLord", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOptions.setTitle(QtGui.QApplication.translate("TimeLord", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCrash_Computer.setText(QtGui.QApplication.translate("TimeLord", "Crash Computer", None, QtGui.QApplication.UnicodeUTF8))

