# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_clock.ui'
#
# Created: Mon Jul 01 11:27:09 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_TimeLord(object):
    def setupUi(self, TimeLord):
        TimeLord.setObjectName("TimeLord")
        TimeLord.resize(978, 807)
        TimeLord.setMinimumSize(QtCore.QSize(978, 807))
        TimeLord.setMaximumSize(QtCore.QSize(978, 807))
        TimeLord.setStyleSheet("QWidget{\n"
"\n"
"background-image: url(:/backgrounds/time_lord_bg.png);\n"
"background-repeat: none;\n"
"background-color: rgba(100, 100, 100, 0);\n"
"selection-color: rgb(115, 115, 115);\n"
"selection-background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.centralwidget = QtGui.QWidget(TimeLord)
        self.centralwidget.setObjectName("centralwidget")
        self.project_dropdown = QtGui.QComboBox(self.centralwidget)
        self.project_dropdown.setGeometry(QtCore.QRect(160, 550, 221, 31))
        self.project_dropdown.setStyleSheet("background-image: url(:/backgrounds/elements/project_bg.png);\n"
"image: url(:/backgrounds/project_bar.png);\n"
"padding-left: 25px;\n"
"subcontrol-origin: padding;\n"
"subcontrol-position: top right;\n"
"font: 16pt \"Calisto MT\";\n"
"color: rgb(56, 9, 8);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.project_dropdown.setObjectName("project_dropdown")
        self.project_dropdown.addItem("")
        self.asset_shot_progress = QtGui.QComboBox(self.centralwidget)
        self.asset_shot_progress.setGeometry(QtCore.QRect(160, 610, 221, 41))
        self.asset_shot_progress.setStyleSheet("background-image: url(:/backgrounds/elements/entity_bg.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"padding-left: 25px;\n"
"subcontrol-origin: padding;\n"
"subcontrol-position: top right;\n"
"font: 16pt \"Calisto MT\";\n"
"color: rgb(56, 9, 8);")
        self.asset_shot_progress.setObjectName("asset_shot_progress")
        self.task_name = QtGui.QComboBox(self.centralwidget)
        self.task_name.setGeometry(QtCore.QRect(160, 680, 221, 31))
        self.task_name.setStyleSheet("background-image: url(:/backgrounds/elements/task_bg.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 1, 0);\n"
"padding-left: 25px;\n"
"subcontrol-origin: padding;\n"
"subcontrol-position: top right;\n"
"font: 16pt \"Calisto MT\";\n"
"color: rgb(56, 9, 8);")
        self.task_name.setObjectName("task_name")
        self.clock_button = QtGui.QPushButton(self.centralwidget)
        self.clock_button.setGeometry(QtCore.QRect(790, 640, 91, 91))
        self.clock_button.setStyleSheet("background-image: url(:/lights buttons/elements/red_in_out_button.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.clock_button.setText("")
        self.clock_button.setObjectName("clock_button")
        self.switch_button = QtGui.QPushButton(self.centralwidget)
        self.switch_button.setGeometry(QtCore.QRect(430, 640, 91, 91))
        self.switch_button.setStyleSheet("background-image: url(:/lights buttons/elements/green_switch_button.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.switch_button.setText("")
        self.switch_button.setObjectName("switch_button")
        self.artist_label = QtGui.QLabel(self.centralwidget)
        self.artist_label.setGeometry(QtCore.QRect(160, 440, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Calisto MT")
        font.setPointSize(22)
        font.setWeight(50)
        font.setItalic(False)
        font.setBold(False)
        self.artist_label.setFont(font)
        self.artist_label.setStyleSheet("background-image: url(:/backgrounds/elements/artist_name.png);\n"
"font:22pt \"Calisto MT\";\n"
"color: rgb(56, 9, 8);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.artist_label.setTextFormat(QtCore.Qt.AutoText)
        self.artist_label.setMargin(0)
        self.artist_label.setObjectName("artist_label")
        self.output_window = QtGui.QPlainTextEdit(self.centralwidget)
        self.output_window.setGeometry(QtCore.QRect(690, 90, 211, 61))
        self.output_window.setStyleSheet("background-image: url(:/backgrounds/elements/output_monitor_top.png);\n"
"border-color: rgba(255, 255, 255, 0);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.output_window.setFrameShape(QtGui.QFrame.NoFrame)
        self.output_window.setFrameShadow(QtGui.QFrame.Plain)
        self.output_window.setObjectName("output_window")
        self.run_hour_ten = QtGui.QGraphicsView(self.centralwidget)
        self.run_hour_ten.setGeometry(QtCore.QRect(280, 270, 41, 61))
        self.run_hour_ten.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/zero_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_hour_ten.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_hour_ten.setFrameShadow(QtGui.QFrame.Plain)
        self.run_hour_ten.setObjectName("run_hour_ten")
        self.run_hour_one = QtGui.QGraphicsView(self.centralwidget)
        self.run_hour_one.setGeometry(QtCore.QRect(340, 270, 41, 61))
        self.run_hour_one.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/three_3.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_hour_one.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_hour_one.setFrameShadow(QtGui.QFrame.Plain)
        self.run_hour_one.setObjectName("run_hour_one")
        self.run_minute_ten = QtGui.QGraphicsView(self.centralwidget)
        self.run_minute_ten.setGeometry(QtCore.QRect(415, 270, 41, 61))
        self.run_minute_ten.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/five_5.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_minute_ten.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_minute_ten.setFrameShadow(QtGui.QFrame.Plain)
        self.run_minute_ten.setObjectName("run_minute_ten")
        self.run_minute_one = QtGui.QGraphicsView(self.centralwidget)
        self.run_minute_one.setGeometry(QtCore.QRect(480, 270, 41, 61))
        self.run_minute_one.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/nine_9.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_minute_one.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_minute_one.setFrameShadow(QtGui.QFrame.Plain)
        self.run_minute_one.setObjectName("run_minute_one")
        self.run_second_ten = QtGui.QGraphicsView(self.centralwidget)
        self.run_second_ten.setGeometry(QtCore.QRect(550, 270, 51, 61))
        self.run_second_ten.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/two_2.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_second_ten.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_second_ten.setFrameShadow(QtGui.QFrame.Plain)
        self.run_second_ten.setObjectName("run_second_ten")
        self.run_second_one = QtGui.QGraphicsView(self.centralwidget)
        self.run_second_one.setGeometry(QtCore.QRect(610, 270, 41, 61))
        self.run_second_one.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/one_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_second_one.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_second_one.setFrameShadow(QtGui.QFrame.Plain)
        self.run_second_one.setObjectName("run_second_one")
        self.week_meter = QtGui.QGraphicsView(self.centralwidget)
        self.week_meter.setGeometry(QtCore.QRect(570, 100, 20, 81))
        self.week_meter.setStyleSheet("background-image: url(:/dial hands/elements/meter_1_needle.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.week_meter.setFrameShape(QtGui.QFrame.NoFrame)
        self.week_meter.setFrameShadow(QtGui.QFrame.Plain)
        self.week_meter.setRenderHints(QtGui.QPainter.SmoothPixmapTransform|QtGui.QPainter.TextAntialiasing)
        self.week_meter.setTransformationAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.week_meter.setObjectName("week_meter")
        self.day_meter = QtGui.QGraphicsView(self.centralwidget)
        self.day_meter.setGeometry(QtCore.QRect(390, 100, 21, 81))
        self.day_meter.setStyleSheet("background-image: url(:/dial hands/elements/meter_1_needle.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.day_meter.setFrameShape(QtGui.QFrame.NoFrame)
        self.day_meter.setFrameShadow(QtGui.QFrame.Plain)
        self.day_meter.setObjectName("day_meter")
        self.time_minute = QtGui.QGraphicsView(self.centralwidget)
        self.time_minute.setGeometry(QtCore.QRect(180, 110, 31, 171))
        self.time_minute.setStyleSheet("background-image: url(:/dial hands/elements/clock_1_minute.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.time_minute.setFrameShape(QtGui.QFrame.NoFrame)
        self.time_minute.setFrameShadow(QtGui.QFrame.Plain)
        self.time_minute.setObjectName("time_minute")
        self.time_hour = QtGui.QGraphicsView(self.centralwidget)
        self.time_hour.setGeometry(QtCore.QRect(180, 110, 31, 171))
        self.time_hour.setStyleSheet("background-image: url(:/dial hands/elements/clock_1_hour.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.time_hour.setFrameShape(QtGui.QFrame.NoFrame)
        self.time_hour.setFrameShadow(QtGui.QFrame.Plain)
        self.time_hour.setObjectName("time_hour")
        self.start_tens_month = QtGui.QGraphicsView(self.centralwidget)
        self.start_tens_month.setGeometry(QtCore.QRect(460, 550, 31, 41))
        self.start_tens_month.setStyleSheet("background-image: url(:/roller_numbers/elements/start_m_tens_zero_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_tens_month.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_tens_month.setFrameShadow(QtGui.QFrame.Plain)
        self.start_tens_month.setObjectName("start_tens_month")
        self.start_ones_month = QtGui.QGraphicsView(self.centralwidget)
        self.start_ones_month.setGeometry(QtCore.QRect(490, 550, 31, 41))
        self.start_ones_month.setStyleSheet("background-image: url(:/roller_numbers/elements/start_m_ones_six_6.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_ones_month.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_ones_month.setFrameShadow(QtGui.QFrame.Plain)
        self.start_ones_month.setObjectName("start_ones_month")
        self.start_tens_day = QtGui.QGraphicsView(self.centralwidget)
        self.start_tens_day.setGeometry(QtCore.QRect(530, 550, 21, 41))
        self.start_tens_day.setStyleSheet("background-image: url(:/roller_numbers/elements/start_d_tens_zero_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_tens_day.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_tens_day.setFrameShadow(QtGui.QFrame.Plain)
        self.start_tens_day.setObjectName("start_tens_day")
        self.start_ones_day = QtGui.QGraphicsView(self.centralwidget)
        self.start_ones_day.setGeometry(QtCore.QRect(560, 550, 21, 41))
        self.start_ones_day.setStyleSheet("background-image: url(:/roller_numbers/elements/start_m_ones_four_4.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_ones_day.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_ones_day.setFrameShadow(QtGui.QFrame.Plain)
        self.start_ones_day.setObjectName("start_ones_day")
        self.start_tens_year = QtGui.QGraphicsView(self.centralwidget)
        self.start_tens_year.setGeometry(QtCore.QRect(600, 550, 21, 41))
        self.start_tens_year.setStyleSheet("background-image: url(:/roller_numbers/elements/start_s_tens_one_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_tens_year.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_tens_year.setFrameShadow(QtGui.QFrame.Plain)
        self.start_tens_year.setObjectName("start_tens_year")
        self.start_ones_year = QtGui.QGraphicsView(self.centralwidget)
        self.start_ones_year.setGeometry(QtCore.QRect(630, 550, 21, 41))
        self.start_ones_year.setStyleSheet("background-image: url(:/roller_numbers/elements/start_s_ones_nine_9.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_ones_year.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_ones_year.setFrameShadow(QtGui.QFrame.Plain)
        self.start_ones_year.setObjectName("start_ones_year")
        self.end_tens_month = QtGui.QGraphicsView(self.centralwidget)
        self.end_tens_month.setGeometry(QtCore.QRect(700, 550, 31, 41))
        self.end_tens_month.setStyleSheet("background-image: url(:/roller_numbers/elements/end_m_tens_zero_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_tens_month.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_tens_month.setFrameShadow(QtGui.QFrame.Plain)
        self.end_tens_month.setObjectName("end_tens_month")
        self.end_ones_month = QtGui.QGraphicsView(self.centralwidget)
        self.end_ones_month.setGeometry(QtCore.QRect(730, 550, 31, 41))
        self.end_ones_month.setStyleSheet("background-image: url(:/roller_numbers/elements/end_m_ones_six_6.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_ones_month.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_ones_month.setFrameShadow(QtGui.QFrame.Plain)
        self.end_ones_month.setObjectName("end_ones_month")
        self.end_tens_day = QtGui.QGraphicsView(self.centralwidget)
        self.end_tens_day.setGeometry(QtCore.QRect(770, 550, 21, 41))
        self.end_tens_day.setStyleSheet("background-image: url(:/roller_numbers/elements/end_d_tens_zer_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_tens_day.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_tens_day.setFrameShadow(QtGui.QFrame.Plain)
        self.end_tens_day.setObjectName("end_tens_day")
        self.end_ones_day = QtGui.QGraphicsView(self.centralwidget)
        self.end_ones_day.setGeometry(QtCore.QRect(800, 550, 21, 41))
        self.end_ones_day.setStyleSheet("background-image: url(:/roller_numbers/elements/end_d_ones_four_4.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_ones_day.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_ones_day.setFrameShadow(QtGui.QFrame.Plain)
        self.end_ones_day.setObjectName("end_ones_day")
        self.end_tens_year = QtGui.QGraphicsView(self.centralwidget)
        self.end_tens_year.setGeometry(QtCore.QRect(830, 550, 31, 41))
        self.end_tens_year.setStyleSheet("background-image: url(:/roller_numbers/elements/end_s_tens_one_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_tens_year.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_tens_year.setFrameShadow(QtGui.QFrame.Plain)
        self.end_tens_year.setObjectName("end_tens_year")
        self.end_ones_year = QtGui.QGraphicsView(self.centralwidget)
        self.end_ones_year.setGeometry(QtCore.QRect(860, 550, 31, 41))
        self.end_ones_year.setStyleSheet("background-image: url(:/roller_numbers/elements/end_s_ones_nine_9.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_ones_year.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_ones_year.setFrameShadow(QtGui.QFrame.Plain)
        self.end_ones_year.setObjectName("end_ones_year")
        self.start_clock_hour = QtGui.QGraphicsView(self.centralwidget)
        self.start_clock_hour.setGeometry(QtCore.QRect(560, 410, 21, 111))
        self.start_clock_hour.setStyleSheet("background-image: url(:/dial hands/elements/clock_2_hour.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_clock_hour.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_clock_hour.setFrameShadow(QtGui.QFrame.Plain)
        self.start_clock_hour.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)
        self.start_clock_hour.setResizeAnchor(QtGui.QGraphicsView.NoAnchor)
        self.start_clock_hour.setObjectName("start_clock_hour")
        self.end_clock_hour = QtGui.QGraphicsView(self.centralwidget)
        self.end_clock_hour.setGeometry(QtCore.QRect(770, 410, 21, 111))
        self.end_clock_hour.setStyleSheet("background-image: url(:/dial hands/elements/clock_3_hour.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_clock_hour.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_clock_hour.setFrameShadow(QtGui.QFrame.Plain)
        self.end_clock_hour.setObjectName("end_clock_hour")
        self.lower_output = QtGui.QGraphicsView(self.centralwidget)
        self.lower_output.setGeometry(QtCore.QRect(690, 160, 211, 181))
        self.lower_output.setStyleSheet("background-image: url(:/backgrounds/elements/output_monitor_bottom.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.lower_output.setFrameShape(QtGui.QFrame.NoFrame)
        self.lower_output.setFrameShadow(QtGui.QFrame.Plain)
        self.lower_output.setObjectName("lower_output")
        self.red_light = QtGui.QGraphicsView(self.centralwidget)
        self.red_light.setGeometry(QtCore.QRect(805, 350, 71, 61))
        self.red_light.setStyleSheet("background-image: url(:/lights buttons/elements/red_light_on.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.red_light.setFrameShape(QtGui.QFrame.NoFrame)
        self.red_light.setFrameShadow(QtGui.QFrame.Plain)
        self.red_light.setObjectName("red_light")
        self.green_light = QtGui.QGraphicsView(self.centralwidget)
        self.green_light.setEnabled(True)
        self.green_light.setGeometry(QtCore.QRect(720, 350, 61, 61))
        self.green_light.setStyleSheet("background-image: url(:/lights buttons/elements/green_light_on.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.green_light.setFrameShape(QtGui.QFrame.NoFrame)
        self.green_light.setFrameShadow(QtGui.QFrame.Plain)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.green_light.setBackgroundBrush(brush)
        self.green_light.setObjectName("green_light")
        self.start_clock_minute = QtGui.QGraphicsView(self.centralwidget)
        self.start_clock_minute.setGeometry(QtCore.QRect(560, 410, 21, 111))
        self.start_clock_minute.setStyleSheet("background-image: url(:/dial hands/elements/clock_2_minute.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_clock_minute.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_clock_minute.setFrameShadow(QtGui.QFrame.Plain)
        self.start_clock_minute.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)
        self.start_clock_minute.setResizeAnchor(QtGui.QGraphicsView.NoAnchor)
        self.start_clock_minute.setObjectName("start_clock_minute")
        self.end_clock_minute = QtGui.QGraphicsView(self.centralwidget)
        self.end_clock_minute.setGeometry(QtCore.QRect(770, 410, 21, 111))
        self.end_clock_minute.setStyleSheet("background-image: url(:/dial hands/elements/clock_3_minute.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_clock_minute.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_clock_minute.setFrameShadow(QtGui.QFrame.Plain)
        self.end_clock_minute.setObjectName("end_clock_minute")
        self.start_date_button = QtGui.QPushButton(self.centralwidget)
        self.start_date_button.setGeometry(QtCore.QRect(630, 510, 31, 31))
        self.start_date_button.setStyleSheet("background-image: url(:/lights buttons/elements/start_date_button.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_date_button.setText("")
        self.start_date_button.setObjectName("start_date_button")
        self.end_date_button = QtGui.QPushButton(self.centralwidget)
        self.end_date_button.setGeometry(QtCore.QRect(850, 510, 31, 21))
        self.end_date_button.setStyleSheet("background-image: url(:/lights buttons/elements/end_date_button.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_date_button.setText("")
        self.end_date_button.setObjectName("end_date_button")
        TimeLord.setCentralWidget(self.centralwidget)
        self.actionCrash_Computer = QtGui.QAction(TimeLord)
        self.actionCrash_Computer.setObjectName("actionCrash_Computer")

        self.retranslateUi(TimeLord)
        QtCore.QMetaObject.connectSlotsByName(TimeLord)

    def retranslateUi(self, TimeLord):
        TimeLord.setWindowTitle(QtGui.QApplication.translate("TimeLord", "Time Lord", None, QtGui.QApplication.UnicodeUTF8))
        self.project_dropdown.setItemText(0, QtGui.QApplication.translate("TimeLord", "Select Project", None, QtGui.QApplication.UnicodeUTF8))
        self.artist_label.setText(QtGui.QApplication.translate("TimeLord", "Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCrash_Computer.setText(QtGui.QApplication.translate("TimeLord", "Crash Computer", None, QtGui.QApplication.UnicodeUTF8))

from resources import time_lord_resources_rc
