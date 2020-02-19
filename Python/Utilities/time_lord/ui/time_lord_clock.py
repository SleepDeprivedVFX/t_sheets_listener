# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_clock.ui'
#
# Created: Thu Jan 16 16:20:57 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtGui, QtCore, QtWidgets

class Ui_TimeLord(object):
    def setupUi(self, TimeLord):
        TimeLord.setObjectName("TimeLord")
        TimeLord.resize(978, 805)
        TimeLord.setMinimumSize(QtCore.QSize(978, 805))
        TimeLord.setMaximumSize(QtCore.QSize(978, 805))
        TimeLord.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(TimeLord)
        self.centralwidget.setObjectName("centralwidget")
        self.bg = QtWidgets.QFrame(self.centralwidget)
        self.bg.setEnabled(True)
        self.bg.setGeometry(QtCore.QRect(0, 0, 978, 805))
        self.bg.setStyleSheet("QFrame {\n"
"    image: url(:/backgrounds/time_lord_bg.png);\n"
"    \n"
"    border-color: rgb(0, 0, 0);\n"
"}")
        self.bg.setFrameShape(QtWidgets.QFrame.Box)
        self.bg.setFrameShadow(QtWidgets.QFrame.Plain)
        self.bg.setLineWidth(5)
        self.bg.setObjectName("bg")
        self.start_tens_month = QtWidgets.QGraphicsView(self.bg)
        self.start_tens_month.setGeometry(QtCore.QRect(463, 551, 31, 43))
        self.start_tens_month.setStyleSheet("background-image: url(:/roller_numbers/elements/start_m_tens_0.png);")
        self.start_tens_month.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.start_tens_month.setFrameShadow(QtWidgets.QFrame.Plain)
        self.start_tens_month.setObjectName("start_tens_month")
        self.start_tens_year = QtWidgets.QGraphicsView(self.bg)
        self.start_tens_year.setGeometry(QtCore.QRect(602, 551, 21, 43))
        self.start_tens_year.setStyleSheet("background-image: url(:/roller_numbers/elements/start_y_tens_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_tens_year.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.start_tens_year.setFrameShadow(QtWidgets.QFrame.Plain)
        self.start_tens_year.setObjectName("start_tens_year")
        self.end_date_button = QtWidgets.QPushButton(self.bg)
        self.end_date_button.setGeometry(QtCore.QRect(848, 508, 27, 28))
        self.end_date_button.setStyleSheet("background-image: url(:/lights buttons/elements/end_date_button.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_date_button.setText("")
        self.end_date_button.setObjectName("end_date_button")
        self.run_hour_one = QtWidgets.QGraphicsView(self.bg)
        self.run_hour_one.setGeometry(QtCore.QRect(341, 269, 41, 61))
        self.run_hour_one.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/vt_3.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_hour_one.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.run_hour_one.setFrameShadow(QtWidgets.QFrame.Plain)
        self.run_hour_one.setObjectName("run_hour_one")
        self.red_light = QtWidgets.QGraphicsView(self.bg)
        self.red_light.setGeometry(QtCore.QRect(805, 352, 71, 61))
        self.red_light.setStyleSheet("background-image: url(:/lights buttons/elements/red_light_on.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.red_light.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.red_light.setFrameShadow(QtWidgets.QFrame.Plain)
        self.red_light.setObjectName("red_light")
        self.start_ones_month = QtWidgets.QGraphicsView(self.bg)
        self.start_ones_month.setGeometry(QtCore.QRect(491, 551, 31, 42))
        self.start_ones_month.setStyleSheet("background-image: url(:/roller_numbers/elements/start_m_ones_6.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_ones_month.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.start_ones_month.setFrameShadow(QtWidgets.QFrame.Plain)
        self.start_ones_month.setObjectName("start_ones_month")
        self.artist_label = QtWidgets.QLabel(self.bg)
        self.artist_label.setGeometry(QtCore.QRect(161, 440, 231, 40))
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
"background-color: transparent;\n"
"image: none;")
        self.artist_label.setTextFormat(QtCore.Qt.AutoText)
        self.artist_label.setMargin(0)
        self.artist_label.setObjectName("artist_label")
        self.start_tens_day = QtWidgets.QGraphicsView(self.bg)
        self.start_tens_day.setGeometry(QtCore.QRect(531, 550, 22, 45))
        self.start_tens_day.setStyleSheet("background-image: url(:/roller_numbers/elements/start_d_tens_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_tens_day.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.start_tens_day.setFrameShadow(QtWidgets.QFrame.Plain)
        self.start_tens_day.setObjectName("start_tens_day")
        self.run_hour_ten = QtWidgets.QGraphicsView(self.bg)
        self.run_hour_ten.setGeometry(QtCore.QRect(281, 269, 41, 61))
        self.run_hour_ten.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/vt_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_hour_ten.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.run_hour_ten.setFrameShadow(QtWidgets.QFrame.Plain)
        self.run_hour_ten.setObjectName("run_hour_ten")
        self.output_monitor = QtWidgets.QPlainTextEdit(self.bg)
        self.output_monitor.setGeometry(QtCore.QRect(694, 89, 205, 26))
        self.output_monitor.setStyleSheet("\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 7pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_monitor.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.output_monitor.setFrameShadow(QtWidgets.QFrame.Plain)
        self.output_monitor.setLineWidth(0)
        self.output_monitor.setMidLineWidth(0)
        self.output_monitor.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_monitor.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_monitor.setBackgroundVisible(False)
        self.output_monitor.setObjectName("output_monitor")
        self.end_ones_day = QtWidgets.QGraphicsView(self.bg)
        self.end_ones_day.setGeometry(QtCore.QRect(800, 551, 17, 40))
        self.end_ones_day.setStyleSheet("background-image: url(:/roller_numbers/elements/end_d_ones_4.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_ones_day.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.end_ones_day.setFrameShadow(QtWidgets.QFrame.Plain)
        self.end_ones_day.setObjectName("end_ones_day")
        self.end_tens_month = QtWidgets.QGraphicsView(self.bg)
        self.end_tens_month.setGeometry(QtCore.QRect(702, 551, 32, 41))
        self.end_tens_month.setStyleSheet("background-image: url(:/roller_numbers/elements/end_m_tens_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_tens_month.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.end_tens_month.setFrameShadow(QtWidgets.QFrame.Plain)
        self.end_tens_month.setObjectName("end_tens_month")
        self.run_minute_one = QtWidgets.QGraphicsView(self.bg)
        self.run_minute_one.setGeometry(QtCore.QRect(481, 269, 41, 61))
        self.run_minute_one.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/vt_9.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_minute_one.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.run_minute_one.setFrameShadow(QtWidgets.QFrame.Plain)
        self.run_minute_one.setObjectName("run_minute_one")
        self.end_tens_day = QtWidgets.QGraphicsView(self.bg)
        self.end_tens_day.setGeometry(QtCore.QRect(771, 550, 21, 43))
        self.end_tens_day.setStyleSheet("background-image: url(:/roller_numbers/elements/end_d_tens_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_tens_day.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.end_tens_day.setFrameShadow(QtWidgets.QFrame.Plain)
        self.end_tens_day.setObjectName("end_tens_day")
        self.run_second_ten = QtWidgets.QGraphicsView(self.bg)
        self.run_second_ten.setGeometry(QtCore.QRect(554, 269, 51, 61))
        self.run_second_ten.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/vt_2.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_second_ten.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.run_second_ten.setFrameShadow(QtWidgets.QFrame.Plain)
        self.run_second_ten.setObjectName("run_second_ten")
        self.start_ones_year = QtWidgets.QGraphicsView(self.bg)
        self.start_ones_year.setGeometry(QtCore.QRect(632, 551, 20, 42))
        self.start_ones_year.setStyleSheet("background-image: url(:/roller_numbers/elements/start_y_ones_9.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_ones_year.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.start_ones_year.setFrameShadow(QtWidgets.QFrame.Plain)
        self.start_ones_year.setObjectName("start_ones_year")
        self.start_ones_day = QtWidgets.QGraphicsView(self.bg)
        self.start_ones_day.setGeometry(QtCore.QRect(559, 551, 25, 40))
        self.start_ones_day.setStyleSheet("background-image: url(:/roller_numbers/elements/start_m_ones_4.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_ones_day.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.start_ones_day.setFrameShadow(QtWidgets.QFrame.Plain)
        self.start_ones_day.setObjectName("start_ones_day")
        self.end_tens_year = QtWidgets.QGraphicsView(self.bg)
        self.end_tens_year.setGeometry(QtCore.QRect(831, 551, 31, 39))
        self.end_tens_year.setStyleSheet("background-image: url(:/roller_numbers/elements/end_y_tens_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_tens_year.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.end_tens_year.setFrameShadow(QtWidgets.QFrame.Plain)
        self.end_tens_year.setObjectName("end_tens_year")
        self.clock_button = QtWidgets.QPushButton(self.bg)
        self.clock_button.setGeometry(QtCore.QRect(619, 626, 118, 119))
        self.clock_button.setStyleSheet("background-image: url(:/lights buttons/elements/clock_button_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border-color: rgba(0, 0, 0, 0);")
        self.clock_button.setText("")
        self.clock_button.setObjectName("clock_button")
        self.run_minute_ten = QtWidgets.QGraphicsView(self.bg)
        self.run_minute_ten.setGeometry(QtCore.QRect(420, 267, 41, 61))
        self.run_minute_ten.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/vt_5.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_minute_ten.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.run_minute_ten.setFrameShadow(QtWidgets.QFrame.Plain)
        self.run_minute_ten.setObjectName("run_minute_ten")
        self.start_date_button = QtWidgets.QPushButton(self.bg)
        self.start_date_button.setGeometry(QtCore.QRect(631, 509, 31, 28))
        self.start_date_button.setStyleSheet("background-image: url(:/lights buttons/elements/start_date_button.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_date_button.setText("")
        self.start_date_button.setObjectName("start_date_button")
        self.green_light = QtWidgets.QGraphicsView(self.bg)
        self.green_light.setEnabled(True)
        self.green_light.setGeometry(QtCore.QRect(720, 353, 61, 61))
        self.green_light.setStyleSheet("background-image: url(:/lights buttons/elements/green_light_on.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.green_light.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.green_light.setFrameShadow(QtWidgets.QFrame.Plain)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.green_light.setBackgroundBrush(brush)
        self.green_light.setObjectName("green_light")
        self.lower_output = QtWidgets.QPlainTextEdit(self.bg)
        self.lower_output.setGeometry(QtCore.QRect(694, 187, 206, 152))
        self.lower_output.setStyleSheet("QPlainTextEdit{\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);\n"
"}\n"
"")
        self.lower_output.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lower_output.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lower_output.setLineWidth(0)
        self.lower_output.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lower_output.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lower_output.setDocumentTitle("")
        self.lower_output.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.lower_output.setObjectName("lower_output")
        self.entity_dropdown = QtWidgets.QComboBox(self.bg)
        self.entity_dropdown.setGeometry(QtCore.QRect(151, 609, 242, 39))
        self.entity_dropdown.setStyleSheet("background-image: url(:/backgrounds/elements/entity_bg.png);\n"
"padding-left: 5px;\n"
"background-repeat: none;\n"
"background-color: rgba(118, 104, 79, 80);\n"
"font: 16pt \"Calisto MT\";\n"
"color: rgb(56, 9, 8);\n"
"subcontrol-origin: padding;\n"
"subcontrol-position: top right;\n"
"selection-background-color: rgba(118, 104, 79, 0);")
        self.entity_dropdown.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        self.entity_dropdown.setFrame(False)
        self.entity_dropdown.setObjectName("entity_dropdown")
        self.entity_dropdown.addItem("")
        self.end_ones_month = QtWidgets.QGraphicsView(self.bg)
        self.end_ones_month.setGeometry(QtCore.QRect(731, 551, 31, 39))
        self.end_ones_month.setStyleSheet("background-image: url(:/roller_numbers/elements/end_m_ones_6.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_ones_month.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.end_ones_month.setFrameShadow(QtWidgets.QFrame.Plain)
        self.end_ones_month.setObjectName("end_ones_month")
        self.task_dropdown = QtWidgets.QComboBox(self.bg)
        self.task_dropdown.setGeometry(QtCore.QRect(151, 679, 242, 34))
        self.task_dropdown.setStyleSheet("background-image: url(:/backgrounds/elements/task_bg.png);\n"
"padding-left: 5px;\n"
"background-color: rgba(118, 104, 79, 80);\n"
"background-repeat: none;\n"
"font: 16pt \"Calisto MT\";\n"
"color: rgb(56, 9, 8);\n"
"subcontrol-origin: padding;\n"
"subcontrol-position: top right;\n"
"selection-background-color: rgba(118, 104, 79, 0);")
        self.task_dropdown.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        self.task_dropdown.setFrame(False)
        self.task_dropdown.setObjectName("task_dropdown")
        self.task_dropdown.addItem("")
        self.project_dropdown = QtWidgets.QComboBox(self.bg)
        self.project_dropdown.setGeometry(QtCore.QRect(153, 547, 240, 33))
        self.project_dropdown.setAutoFillBackground(False)
        self.project_dropdown.setStyleSheet("image: url(:/backgrounds/elements/project_bar.png);\n"
"padding-left: 5px;\n"
"background-color: rgba(118, 104, 79, 80);\n"
"background-repeat: none;\n"
"font: 16pt \"Calisto MT\";\n"
"color: rgb(56, 9, 8);\n"
"subcontrol-origin: padding;\n"
"subcontrol-position: top right;\n"
"selection-background-color: rgba(118, 104, 79, 0);")
        self.project_dropdown.setEditable(False)
        self.project_dropdown.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        self.project_dropdown.setFrame(False)
        self.project_dropdown.setObjectName("project_dropdown")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/backgrounds/elements/project_bg.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(":/backgrounds/elements/project_bg.png"), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/backgrounds/elements/project_bg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/backgrounds/elements/project_bg.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/backgrounds/elements/project_bg.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(":/backgrounds/elements/project_bg.png"), QtGui.QIcon.Active, QtGui.QIcon.On)
        self.project_dropdown.addItem(icon, "")
        self.run_second_one = QtWidgets.QGraphicsView(self.bg)
        self.run_second_one.setGeometry(QtCore.QRect(611, 269, 41, 61))
        self.run_second_one.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/vt_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_second_one.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.run_second_one.setFrameShadow(QtWidgets.QFrame.Plain)
        self.run_second_one.setObjectName("run_second_one")
        self.end_ones_year = QtWidgets.QGraphicsView(self.bg)
        self.end_ones_year.setGeometry(QtCore.QRect(859, 551, 33, 39))
        self.end_ones_year.setStyleSheet("background-image: url(:/roller_numbers/elements/end_y_ones_9.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_ones_year.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.end_ones_year.setFrameShadow(QtWidgets.QFrame.Plain)
        self.end_ones_year.setObjectName("end_ones_year")
        self.time_hour = QtWidgets.QLabel(self.bg)
        self.time_hour.setGeometry(QtCore.QRect(110, 110, 168, 168))
        self.time_hour.setStyleSheet("image: none;")
        self.time_hour.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.time_hour.setText("")
        self.time_hour.setTextFormat(QtCore.Qt.PlainText)
        self.time_hour.setPixmap(QtGui.QPixmap(":/dial hands/elements/clock_1_hour.png"))
        self.time_hour.setScaledContents(False)
        self.time_hour.setAlignment(QtCore.Qt.AlignCenter)
        self.time_hour.setObjectName("time_hour")
        self.time_minute = QtWidgets.QLabel(self.bg)
        self.time_minute.setGeometry(QtCore.QRect(110, 110, 168, 168))
        self.time_minute.setStyleSheet("image: none;")
        self.time_minute.setText("")
        self.time_minute.setPixmap(QtGui.QPixmap(":/dial hands/elements/clock_1_minute.png"))
        self.time_minute.setAlignment(QtCore.Qt.AlignCenter)
        self.time_minute.setObjectName("time_minute")
        self.day_meter = QtWidgets.QLabel(self.bg)
        self.day_meter.setGeometry(QtCore.QRect(305, 77, 192, 192))
        self.day_meter.setStyleSheet("image: none;")
        self.day_meter.setText("")
        self.day_meter.setPixmap(QtGui.QPixmap(":/dial hands/elements/meter_1_needle.png"))
        self.day_meter.setScaledContents(False)
        self.day_meter.setAlignment(QtCore.Qt.AlignCenter)
        self.day_meter.setObjectName("day_meter")
        self.week_meter = QtWidgets.QLabel(self.bg)
        self.week_meter.setGeometry(QtCore.QRect(481, 76, 192, 192))
        self.week_meter.setStyleSheet("image: none;")
        self.week_meter.setText("")
        self.week_meter.setPixmap(QtGui.QPixmap(":/dial hands/elements/meter_1_needle.png"))
        self.week_meter.setAlignment(QtCore.Qt.AlignCenter)
        self.week_meter.setObjectName("week_meter")
        self.start_clock_minute = QtWidgets.QLabel(self.bg)
        self.start_clock_minute.setGeometry(QtCore.QRect(512, 404, 115, 115))
        self.start_clock_minute.setStyleSheet("image: none;")
        self.start_clock_minute.setText("")
        self.start_clock_minute.setPixmap(QtGui.QPixmap(":/dial hands/elements/clock_2_minute.png"))
        self.start_clock_minute.setAlignment(QtCore.Qt.AlignCenter)
        self.start_clock_minute.setObjectName("start_clock_minute")
        self.start_clock_hour = QtWidgets.QLabel(self.bg)
        self.start_clock_hour.setGeometry(QtCore.QRect(512, 404, 115, 115))
        self.start_clock_hour.setStyleSheet("image: none;")
        self.start_clock_hour.setText("")
        self.start_clock_hour.setPixmap(QtGui.QPixmap(":/dial hands/elements/clock_2_hour.png"))
        self.start_clock_hour.setAlignment(QtCore.Qt.AlignCenter)
        self.start_clock_hour.setObjectName("start_clock_hour")
        self.end_clock_hour = QtWidgets.QLabel(self.bg)
        self.end_clock_hour.setGeometry(QtCore.QRect(724, 406, 115, 115))
        self.end_clock_hour.setStyleSheet("image: none;")
        self.end_clock_hour.setText("")
        self.end_clock_hour.setPixmap(QtGui.QPixmap(":/dial hands/elements/clock_3_hour.png"))
        self.end_clock_hour.setAlignment(QtCore.Qt.AlignCenter)
        self.end_clock_hour.setObjectName("end_clock_hour")
        self.end_clock_minute = QtWidgets.QLabel(self.bg)
        self.end_clock_minute.setGeometry(QtCore.QRect(724, 406, 115, 115))
        self.end_clock_minute.setStyleSheet("image: none;")
        self.end_clock_minute.setText("")
        self.end_clock_minute.setPixmap(QtGui.QPixmap(":/dial hands/elements/clock_3_minute.png"))
        self.end_clock_minute.setAlignment(QtCore.Qt.AlignCenter)
        self.end_clock_minute.setObjectName("end_clock_minute")
        self.output_trt = QtWidgets.QPlainTextEdit(self.bg)
        self.output_trt.setGeometry(QtCore.QRect(695, 111, 205, 17))
        self.output_trt.setStyleSheet("\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_trt.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.output_trt.setFrameShadow(QtWidgets.QFrame.Plain)
        self.output_trt.setLineWidth(0)
        self.output_trt.setMidLineWidth(0)
        self.output_trt.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_trt.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_trt.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.output_trt.setBackgroundVisible(False)
        self.output_trt.setObjectName("output_trt")
        self.output_start_end = QtWidgets.QPlainTextEdit(self.bg)
        self.output_start_end.setGeometry(QtCore.QRect(695, 122, 204, 28))
        self.output_start_end.setStyleSheet("\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_start_end.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.output_start_end.setFrameShadow(QtWidgets.QFrame.Plain)
        self.output_start_end.setLineWidth(0)
        self.output_start_end.setMidLineWidth(0)
        self.output_start_end.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_start_end.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_start_end.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.output_start_end.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.output_start_end.setBackgroundVisible(False)
        self.output_start_end.setObjectName("output_start_end")
        self.output_user = QtWidgets.QPlainTextEdit(self.bg)
        self.output_user.setGeometry(QtCore.QRect(695, 145, 204, 20))
        self.output_user.setStyleSheet("\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_user.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.output_user.setFrameShadow(QtWidgets.QFrame.Plain)
        self.output_user.setLineWidth(0)
        self.output_user.setMidLineWidth(0)
        self.output_user.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_user.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_user.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.output_user.setBackgroundVisible(False)
        self.output_user.setObjectName("output_user")
        self.output_daily = QtWidgets.QPlainTextEdit(self.bg)
        self.output_daily.setGeometry(QtCore.QRect(695, 157, 204, 17))
        self.output_daily.setStyleSheet("\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_daily.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.output_daily.setFrameShadow(QtWidgets.QFrame.Plain)
        self.output_daily.setLineWidth(0)
        self.output_daily.setMidLineWidth(0)
        self.output_daily.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_daily.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_daily.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.output_daily.setBackgroundVisible(False)
        self.output_daily.setObjectName("output_daily")
        self.output_weekly = QtWidgets.QPlainTextEdit(self.bg)
        self.output_weekly.setGeometry(QtCore.QRect(695, 170, 204, 17))
        self.output_weekly.setStyleSheet("\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_weekly.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.output_weekly.setFrameShadow(QtWidgets.QFrame.Plain)
        self.output_weekly.setLineWidth(0)
        self.output_weekly.setMidLineWidth(0)
        self.output_weekly.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_weekly.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_weekly.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.output_weekly.setBackgroundVisible(False)
        self.output_weekly.setObjectName("output_weekly")
        TimeLord.setCentralWidget(self.centralwidget)
        self.actionCrash_Computer = QtWidgets.QAction(TimeLord)
        self.actionCrash_Computer.setObjectName("actionCrash_Computer")

        self.retranslateUi(TimeLord)
        QtCore.QMetaObject.connectSlotsByName(TimeLord)
        TimeLord.setTabOrder(self.clock_button, self.project_dropdown)
        TimeLord.setTabOrder(self.project_dropdown, self.entity_dropdown)
        TimeLord.setTabOrder(self.entity_dropdown, self.task_dropdown)
        TimeLord.setTabOrder(self.task_dropdown, self.start_date_button)
        TimeLord.setTabOrder(self.start_date_button, self.end_date_button)
        TimeLord.setTabOrder(self.end_date_button, self.run_hour_ten)
        TimeLord.setTabOrder(self.run_hour_ten, self.run_hour_one)
        TimeLord.setTabOrder(self.run_hour_one, self.run_minute_ten)
        TimeLord.setTabOrder(self.run_minute_ten, self.run_minute_one)
        TimeLord.setTabOrder(self.run_minute_one, self.run_second_ten)
        TimeLord.setTabOrder(self.run_second_ten, self.run_second_one)
        TimeLord.setTabOrder(self.run_second_one, self.start_tens_month)
        TimeLord.setTabOrder(self.start_tens_month, self.start_ones_month)
        TimeLord.setTabOrder(self.start_ones_month, self.start_tens_day)
        TimeLord.setTabOrder(self.start_tens_day, self.start_ones_day)
        TimeLord.setTabOrder(self.start_ones_day, self.start_tens_year)
        TimeLord.setTabOrder(self.start_tens_year, self.start_ones_year)
        TimeLord.setTabOrder(self.start_ones_year, self.end_tens_month)
        TimeLord.setTabOrder(self.end_tens_month, self.end_ones_month)
        TimeLord.setTabOrder(self.end_ones_month, self.end_tens_day)
        TimeLord.setTabOrder(self.end_tens_day, self.end_ones_day)
        TimeLord.setTabOrder(self.end_ones_day, self.end_tens_year)
        TimeLord.setTabOrder(self.end_tens_year, self.end_ones_year)
        TimeLord.setTabOrder(self.end_ones_year, self.red_light)
        TimeLord.setTabOrder(self.red_light, self.green_light)
        TimeLord.setTabOrder(self.green_light, self.output_monitor)
        TimeLord.setTabOrder(self.output_monitor, self.lower_output)

    def retranslateUi(self, TimeLord):
        TimeLord.setWindowTitle(QtWidgets.QApplication.translate("TimeLord", "Time Lord", None))
        self.start_tens_month.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Start Month</span><span style=\" color:#010101;\"><br/>The month record of the current timesheet.</span></p></body></html>", None))
        self.start_tens_year.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Start Year</span><span style=\" color:#010101;\"><br/>The year record of the current timesheet.</span></p></body></html>", None))
        self.end_date_button.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Set End Time Button</span><span style=\" color:#010101;\"><br/>This will manually set the end time for the latest timesheet.  If you are clocked in, it will clock you out at the time you set.</span></p></body></html>", None))
        self.run_hour_one.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Running Time Hours</span><span style=\" color:#010101;\"><br/>The total hours recorded on the current timesheet task</span></p></body></html>", None))
        self.red_light.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Error Light</span><span style=\" color:#010101;\"><br/>This light comes on when something is not kosher.  Either the selected Project/Entity/Task is not valid, or something has gone wrong!  See the Output Window.</span></p></body></html>", None))
        self.start_ones_month.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Start Month</span><span style=\" color:#010101;\"><br/>The month record of the current timesheet.</span></p></body></html>", None))
        self.artist_label.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Artist Name</span><span style=\" color:#010101;\"><br/>Set by the system by default. If you </span><span style=\" font-weight:600; color:#010101;\">do not</span><span style=\" color:#010101;\"> see your name here, chances are that this won\'t clock you in properly.</span></p></body></html>", None))
        self.artist_label.setText(QtWidgets.QApplication.translate("TimeLord", "Artist", None))
        self.start_tens_day.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Start Day</span><span style=\" color:#010101;\"><br/>The day record of the current timesheet.</span></p></body></html>", None))
        self.run_hour_ten.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Running Time Hours</span><span style=\" color:#010101;\"><br/>The total hours recorded on the current timesheet task</span></p></body></html>", None))
        self.output_monitor.setPlainText(QtWidgets.QApplication.translate("TimeLord", "OUTPUT MONITOR\n"
"------------------------------------", None))
        self.end_ones_day.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">End Day</span><span style=\" color:#010101;\"><br/>The end day record of the current timesheet.</span></p></body></html>", None))
        self.end_tens_month.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">End Month</span><span style=\" color:#010101;\"><br/>The end month record of the current timesheet.</span></p></body></html>", None))
        self.run_minute_one.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Running Time Minutes</span><span style=\" color:#010101;\"><br/>The total minutes recorded on the current timesheet task</span></p></body></html>", None))
        self.end_tens_day.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">End Day</span><span style=\" color:#010101;\"><br/>The end day record of the current timesheet.</span></p></body></html>", None))
        self.run_second_ten.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Running Time Seconds</span><span style=\" color:#010101;\"><br/>The total seconds recorded on the current timesheet task</span></p></body></html>", None))
        self.start_ones_year.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Start Year</span><span style=\" color:#010101;\"><br/>The year record of the current timesheet.</span></p></body></html>", None))
        self.start_ones_day.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#030303;\">Start Day</span><span style=\" color:#030303;\"><br/>The day record of the current timesheet.</span></p></body></html>", None))
        self.end_tens_year.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">End Year</span><span style=\" color:#010101;\"><br/>The end year record of the current timesheet.</span></p></body></html>", None))
        self.clock_button.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600;\">Clock In/Out/Switch Button<br/></span>This button clocks you in, out or switches your timesheet</p><p><span style=\" font-weight:600;\">Green:</span><span style=\" font-style:italic;\">Clock in<br/></span><span style=\" font-weight:600;\">Red: </span><span style=\" font-style:italic;\">Clock Out<br/></span><span style=\" font-weight:600;\">Yellow: </span><span style=\" font-style:italic;\">Switch Tasks</span></p></body></html>", None))
        self.run_minute_ten.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Running Time Minutes</span><span style=\" color:#010101;\"><br/>The total minutes recorded on the current timesheet task</span></p></body></html>", None))
        self.start_date_button.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Set Start Time Button<br/></span><span style=\" color:#010101;\">This will manually set the start time. If you are clocked in, it will adjust the current timesheet. If you are clocked out, it will set the time you would like to clock in to.</span></p></body></html>", None))
        self.green_light.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Activity Light</span><span style=\" color:#0a0a0a;\"><br/>Will be steady on, or flashing when things are either being processed, or are going well.</span></p></body></html>", None))
        self.lower_output.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Output Window<br/></span><span style=\" color:#0a0a0a;\">This displays functional information from under the hood of the Time Lord. Error and status messages can be found here.</span></p></body></html>", None))
        self.lower_output.setPlainText(QtWidgets.QApplication.translate("TimeLord", "Raw Data Ouput", None))
        self.entity_dropdown.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Entity Dropdown</span><span style=\" color:#010101;\"><br/>Sets either the Asset Entity or Shot entity that you are working on. Displays current values if you are clocked in.</span></p></body></html>", None))
        self.entity_dropdown.setItemText(0, QtWidgets.QApplication.translate("TimeLord", "Select Asset/Shot", None))
        self.end_ones_month.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">End Month</span><span style=\" color:#010101;\"><br/>The end month record of the current timesheet.</span></p></body></html>", None))
        self.task_dropdown.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Task Dropdown</span><span style=\" color:#010101;\"><br/>The actual task you are working on.  If you are clocked in, it displays the current task.</span></p></body></html>", None))
        self.task_dropdown.setItemText(0, QtWidgets.QApplication.translate("TimeLord", "Select Task", None))
        self.project_dropdown.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#020202;\">Project Dropdown<br/></span><span style=\" color:#020202;\">Sets the project that will be clocked in to.  If you are already clocked in, it will display what you are currently clocked in to.</span></p></body></html>", None))
        self.project_dropdown.setItemText(0, QtWidgets.QApplication.translate("TimeLord", "Select Project", None))
        self.run_second_one.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Running Time Seconds</span><span style=\" color:#010101;\"><br/>The total seconds recorded on the current timesheet task</span></p></body></html>", None))
        self.end_ones_year.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">End Year</span><span style=\" color:#010101;\"><br/>The end year record of the current timesheet.</span></p></body></html>", None))
        self.time_minute.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#0b0b0b;\">Real Time Clock</span><span style=\" color:#0b0b0b;\"><br/>This is what time it is now.</span></p></body></html>", None))
        self.day_meter.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Daily Total Meter<br/></span><span style=\" color:#0a0a0a;\">Graphically displays the amount of hours worked so far.  Red line indicates Over Time.</span><span style=\" color:#0a0a0a;\"><br/>Today: %s hrs</span></p></body></html>", None))
        self.week_meter.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600;\">Weekly Total Meter</span><br/>Graphically displays the hours accumulated for the week.  A red line indicates over time<br/>Total: %s hrs</p></body></html>", None))
        self.start_clock_hour.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Current Task Start Time</span><span style=\" color:#010101;\"><br/>Shows the time of the latest timesheet start time</span><span style=\" color:#010101;\">. If you\'re not clocked in, this is the Current Time.</span></p></body></html>", None))
        self.end_clock_minute.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Current Timesheet Out Time</span><span style=\" color:#010101;\"><br/>Shows the out time of the latest timesheet. If you are Clocked in, this is the Current Time.</span></p></body></html>", None))
        self.output_trt.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Total Running Time</span><span style=\" color:#0a0a0a;\"><br/>Displays TRT for the current Timesheet.</span></p></body></html>", None))
        self.output_trt.setPlainText(QtWidgets.QApplication.translate("TimeLord", "TRT: 00:12:24\n"
"", None))
        self.output_start_end.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Current Start and End Times<br/></span><span style=\" color:#0a0a0a;\">Shows when the Current Timesheet Was clocked in and out.  If you are clocked in, the End is the current time.</span></p></body></html>", None))
        self.output_start_end.setPlainText(QtWidgets.QApplication.translate("TimeLord", "Start: 07/02/19\n"
"End:", None))
        self.output_user.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Clocked In Status</span></p></body></html>", None))
        self.output_user.setPlainText(QtWidgets.QApplication.translate("TimeLord", "USER CLOCKED IN", None))
        self.output_daily.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Daily Total</span><span style=\" color:#0a0a0a;\"><br/>Daily total of hours worked so far.</span></p></body></html>", None))
        self.output_daily.setPlainText(QtWidgets.QApplication.translate("TimeLord", "Daily Total: 6", None))
        self.output_weekly.setToolTip(QtWidgets.QApplication.translate("TimeLord", "<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Weekly Total</span><span style=\" color:#0a0a0a;\"><br/>Weekly Total of Hours worked so far.</span></p></body></html>", None))
        self.output_weekly.setPlainText(QtWidgets.QApplication.translate("TimeLord", "Weekly Total: 18", None))
        self.actionCrash_Computer.setText(QtWidgets.QApplication.translate("TimeLord", "Crash Computer", None))

from ui.resources import time_lord_resources_rc
