# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_clock.ui'
#
# Created: Wed Jun 26 17:03:09 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_TimeLord(object):
    def setupUi(self, TimeLord):
        TimeLord.setObjectName("TimeLord")
        TimeLord.resize(1305, 1073)
        TimeLord.setMinimumSize(QtCore.QSize(1305, 1073))
        TimeLord.setMaximumSize(QtCore.QSize(1305, 1073))
        TimeLord.setStyleSheet("QWidget{\n"
"background-image: url(:/backgrounds/pre-rendered_image.jpg);\n"
"background-repeat: none;\n"
"background-color: rgba(100, 100, 100, 0);\n"
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
"\n"
"")
        self.centralwidget = QtGui.QWidget(TimeLord)
        self.centralwidget.setObjectName("centralwidget")
        self.time_lord_title = QtGui.QLabel(self.centralwidget)
        self.time_lord_title.setGeometry(QtCore.QRect(530, 20, 161, 31))
        self.time_lord_title.setStyleSheet("font: 24pt \"Arial\";")
        self.time_lord_title.setObjectName("time_lord_title")
        self.project_dropdown = QtGui.QComboBox(self.centralwidget)
        self.project_dropdown.setGeometry(QtCore.QRect(198, 731, 331, 51))
        self.project_dropdown.setStyleSheet("background-image: url(:/backgrounds/project_bar.png);\n"
"image: url(:/backgrounds/project_bar.png);\n"
"")
        self.project_dropdown.setObjectName("project_dropdown")
        self.asset_shot_progress = QtGui.QComboBox(self.centralwidget)
        self.asset_shot_progress.setGeometry(QtCore.QRect(200, 820, 321, 51))
        self.asset_shot_progress.setStyleSheet("background-image: url(:/backgrounds/AssetShot_bar.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.asset_shot_progress.setObjectName("asset_shot_progress")
        self.task_progress = QtGui.QComboBox(self.centralwidget)
        self.task_progress.setGeometry(QtCore.QRect(200, 910, 321, 51))
        self.task_progress.setStyleSheet("background-image: url(:/backgrounds/task_bar.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 1, 0);")
        self.task_progress.setObjectName("task_progress")
        self.start_time = QtGui.QDateTimeEdit(self.centralwidget)
        self.start_time.setGeometry(QtCore.QRect(640, 750, 194, 22))
        self.start_time.setObjectName("start_time")
        self.end_time = QtGui.QDateTimeEdit(self.centralwidget)
        self.end_time.setGeometry(QtCore.QRect(970, 750, 194, 22))
        self.end_time.setObjectName("end_time")
        self.clock_button = QtGui.QPushButton(self.centralwidget)
        self.clock_button.setGeometry(QtCore.QRect(1060, 860, 111, 121))
        self.clock_button.setStyleSheet("background-image: url(:/backgrounds/red_InOut_button.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.clock_button.setText("")
        self.clock_button.setObjectName("clock_button")
        self.switch_button = QtGui.QPushButton(self.centralwidget)
        self.switch_button.setGeometry(QtCore.QRect(574, 862, 121, 121))
        self.switch_button.setStyleSheet("background-image: url(:/backgrounds/red_InOut_button.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.switch_button.setText("")
        self.switch_button.setObjectName("switch_button")
        self.artist_label = QtGui.QLabel(self.centralwidget)
        self.artist_label.setGeometry(QtCore.QRect(205, 572, 331, 91))
        self.artist_label.setStyleSheet("background-image: url(:/backgrounds/artist_background.png);\n"
"font: 22pt \"Calisto MT\";")
        self.artist_label.setObjectName("artist_label")
        self.output_window = QtGui.QPlainTextEdit(self.centralwidget)
        self.output_window.setGeometry(QtCore.QRect(900, 110, 311, 341))
        self.output_window.setStyleSheet("background-image: url(:/backgrounds/screen_bg.png);\n"
"border-color: rgba(255, 255, 255, 0);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.output_window.setFrameShape(QtGui.QFrame.NoFrame)
        self.output_window.setFrameShadow(QtGui.QFrame.Plain)
        self.output_window.setObjectName("output_window")
        self.run_hour_ten = QtGui.QGraphicsView(self.centralwidget)
        self.run_hour_ten.setGeometry(QtCore.QRect(370, 350, 61, 101))
        self.run_hour_ten.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/vt_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_hour_ten.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_hour_ten.setFrameShadow(QtGui.QFrame.Plain)
        self.run_hour_ten.setObjectName("run_hour_ten")
        self.run_hour_one = QtGui.QGraphicsView(self.centralwidget)
        self.run_hour_one.setGeometry(QtCore.QRect(460, 350, 61, 101))
        self.run_hour_one.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/vt_4.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_hour_one.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_hour_one.setFrameShadow(QtGui.QFrame.Plain)
        self.run_hour_one.setObjectName("run_hour_one")
        self.run_minute_ten = QtGui.QGraphicsView(self.centralwidget)
        self.run_minute_ten.setGeometry(QtCore.QRect(560, 350, 61, 101))
        self.run_minute_ten.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/vt_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_minute_ten.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_minute_ten.setFrameShadow(QtGui.QFrame.Plain)
        self.run_minute_ten.setObjectName("run_minute_ten")
        self.run_minute_one = QtGui.QGraphicsView(self.centralwidget)
        self.run_minute_one.setGeometry(QtCore.QRect(630, 350, 61, 101))
        self.run_minute_one.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/vt_3.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_minute_one.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_minute_one.setFrameShadow(QtGui.QFrame.Plain)
        self.run_minute_one.setObjectName("run_minute_one")
        self.run_second_ten = QtGui.QGraphicsView(self.centralwidget)
        self.run_second_ten.setGeometry(QtCore.QRect(730, 350, 61, 101))
        self.run_second_ten.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/vt_5.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_second_ten.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_second_ten.setFrameShadow(QtGui.QFrame.Plain)
        self.run_second_ten.setObjectName("run_second_ten")
        self.run_second_one = QtGui.QGraphicsView(self.centralwidget)
        self.run_second_one.setGeometry(QtCore.QRect(810, 350, 61, 101))
        self.run_second_one.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/vt_9.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_second_one.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_second_one.setFrameShadow(QtGui.QFrame.Plain)
        self.run_second_one.setObjectName("run_second_one")
        self.week_meter = QtGui.QGraphicsView(self.centralwidget)
        self.week_meter.setGeometry(QtCore.QRect(760, 160, 20, 81))
        self.week_meter.setStyleSheet("background-image: url(:/dial hands/meter_dial.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.week_meter.setFrameShape(QtGui.QFrame.NoFrame)
        self.week_meter.setFrameShadow(QtGui.QFrame.Plain)
        self.week_meter.setObjectName("week_meter")
        self.day_meter = QtGui.QGraphicsView(self.centralwidget)
        self.day_meter.setGeometry(QtCore.QRect(520, 160, 20, 81))
        self.day_meter.setStyleSheet("background-image: url(:/dial hands/meter_dial.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.day_meter.setFrameShape(QtGui.QFrame.NoFrame)
        self.day_meter.setFrameShadow(QtGui.QFrame.Plain)
        self.day_meter.setObjectName("day_meter")
        self.time_minute = QtGui.QGraphicsView(self.centralwidget)
        self.time_minute.setGeometry(QtCore.QRect(240, 170, 31, 181))
        self.time_minute.setStyleSheet("background-image: url(:/dial hands/clock_minute_hand.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.time_minute.setFrameShape(QtGui.QFrame.NoFrame)
        self.time_minute.setFrameShadow(QtGui.QFrame.Plain)
        self.time_minute.setObjectName("time_minute")
        self.time_hour = QtGui.QGraphicsView(self.centralwidget)
        self.time_hour.setGeometry(QtCore.QRect(240, 180, 31, 181))
        self.time_hour.setStyleSheet("background-image: url(:/dial hands/clock_hour_hand.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.time_hour.setFrameShape(QtGui.QFrame.NoFrame)
        self.time_hour.setFrameShadow(QtGui.QFrame.Plain)
        self.time_hour.setObjectName("time_hour")
        TimeLord.setCentralWidget(self.centralwidget)
        self.actionCrash_Computer = QtGui.QAction(TimeLord)
        self.actionCrash_Computer.setObjectName("actionCrash_Computer")

        self.retranslateUi(TimeLord)
        QtCore.QMetaObject.connectSlotsByName(TimeLord)

    def retranslateUi(self, TimeLord):
        TimeLord.setWindowTitle(QtGui.QApplication.translate("TimeLord", "Time Lord", None, QtGui.QApplication.UnicodeUTF8))
        self.time_lord_title.setText(QtGui.QApplication.translate("TimeLord", "Time Lord", None, QtGui.QApplication.UnicodeUTF8))
        self.artist_label.setText(QtGui.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-size:22pt;\">Artist</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCrash_Computer.setText(QtGui.QApplication.translate("TimeLord", "Crash Computer", None, QtGui.QApplication.UnicodeUTF8))

from resources import time_lord_resources_rc
