# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_clock.ui'
#
# Created: Fri Jul 19 12:15:52 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_TimeLord(object):
    def setupUi(self, TimeLord):
        TimeLord.setObjectName("TimeLord")
        TimeLord.resize(978, 805)
        TimeLord.setMinimumSize(QtCore.QSize(978, 805))
        TimeLord.setMaximumSize(QtCore.QSize(978, 805))
        TimeLord.setStyleSheet("")
        self.centralwidget = QtGui.QWidget(TimeLord)
        self.centralwidget.setObjectName("centralwidget")
        self.bg = QtGui.QFrame(self.centralwidget)
        self.bg.setGeometry(QtCore.QRect(0, 0, 978, 805))
        self.bg.setStyleSheet("QFrame {\n"
"    image: url(:/backgrounds/time_lord_bg.png);\n"
"    \n"
"    border-color: rgb(0, 0, 0);\n"
"}")
        self.bg.setFrameShape(QtGui.QFrame.Box)
        self.bg.setFrameShadow(QtGui.QFrame.Plain)
        self.bg.setLineWidth(5)
        self.bg.setObjectName("bg")
        self.start_tens_month = QtGui.QGraphicsView(self.bg)
        self.start_tens_month.setGeometry(QtCore.QRect(463, 551, 31, 43))
        self.start_tens_month.setStyleSheet("background-image: url(:/roller_numbers/elements/start_m_tens_0.png);")
        self.start_tens_month.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_tens_month.setFrameShadow(QtGui.QFrame.Plain)
        self.start_tens_month.setObjectName("start_tens_month")
        self.start_tens_year = QtGui.QGraphicsView(self.bg)
        self.start_tens_year.setGeometry(QtCore.QRect(602, 551, 21, 43))
        self.start_tens_year.setStyleSheet("background-image: url(:/roller_numbers/elements/start_y_tens_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_tens_year.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_tens_year.setFrameShadow(QtGui.QFrame.Plain)
        self.start_tens_year.setObjectName("start_tens_year")
        self.end_date_button = QtGui.QPushButton(self.bg)
        self.end_date_button.setGeometry(QtCore.QRect(848, 508, 27, 28))
        self.end_date_button.setStyleSheet("background-image: url(:/lights buttons/elements/end_date_button.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_date_button.setText("")
        self.end_date_button.setObjectName("end_date_button")
        self.run_hour_one = QtGui.QGraphicsView(self.bg)
        self.run_hour_one.setGeometry(QtCore.QRect(341, 269, 41, 61))
        self.run_hour_one.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/vt_3.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_hour_one.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_hour_one.setFrameShadow(QtGui.QFrame.Plain)
        self.run_hour_one.setObjectName("run_hour_one")
        self.red_light = QtGui.QGraphicsView(self.bg)
        self.red_light.setGeometry(QtCore.QRect(805, 352, 71, 61))
        self.red_light.setStyleSheet("background-image: url(:/lights buttons/elements/red_light_on.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.red_light.setFrameShape(QtGui.QFrame.NoFrame)
        self.red_light.setFrameShadow(QtGui.QFrame.Plain)
        self.red_light.setObjectName("red_light")
        self.start_ones_month = QtGui.QGraphicsView(self.bg)
        self.start_ones_month.setGeometry(QtCore.QRect(491, 551, 31, 42))
        self.start_ones_month.setStyleSheet("background-image: url(:/roller_numbers/elements/start_m_ones_6.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_ones_month.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_ones_month.setFrameShadow(QtGui.QFrame.Plain)
        self.start_ones_month.setObjectName("start_ones_month")

        # Timesheet ID
        self.timesheet_id = QtGui.QLabel(self.bg)
        self.timesheet_id.setGeometry(QtCore.QRect(819, 730, 97, 20))
        self.timesheet_id.setTextFormat(QtCore.Qt.AutoText)
        self.timesheet_id.setObjectName('timesheet_id')
        self.timesheet_id.setText('12345')
        self.timesheet_id.hide()

        # Task ID
        self.task_id = QtGui.QLabel(self.bg)
        self.task_id.setGeometry(QtCore.QRect(819, 700, 97, 20))
        self.task_id.setTextFormat(QtCore.Qt.AutoText)
        self.task_id.setObjectName('task_id')
        self.task_id.setText('1')
        self.task_id.hide()

        self.artist_label = QtGui.QLabel(self.bg)
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
        self.start_tens_day = QtGui.QGraphicsView(self.bg)
        self.start_tens_day.setGeometry(QtCore.QRect(531, 550, 22, 45))
        self.start_tens_day.setStyleSheet("background-image: url(:/roller_numbers/elements/start_d_tens_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_tens_day.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_tens_day.setFrameShadow(QtGui.QFrame.Plain)
        self.start_tens_day.setObjectName("start_tens_day")
        self.run_hour_ten = QtGui.QGraphicsView(self.bg)
        self.run_hour_ten.setGeometry(QtCore.QRect(281, 269, 41, 61))
        self.run_hour_ten.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/vt_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_hour_ten.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_hour_ten.setFrameShadow(QtGui.QFrame.Plain)
        self.run_hour_ten.setObjectName("run_hour_ten")
        self.output_monitor = QtGui.QPlainTextEdit(self.bg)
        self.output_monitor.setGeometry(QtCore.QRect(694, 89, 205, 26))
        self.output_monitor.setStyleSheet("\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 10pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_monitor.setFrameShape(QtGui.QFrame.NoFrame)
        self.output_monitor.setFrameShadow(QtGui.QFrame.Plain)
        self.output_monitor.setLineWidth(0)
        self.output_monitor.setMidLineWidth(0)
        self.output_monitor.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_monitor.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_monitor.setBackgroundVisible(False)
        self.output_monitor.setObjectName("output_monitor")
        self.end_ones_day = QtGui.QGraphicsView(self.bg)
        self.end_ones_day.setGeometry(QtCore.QRect(800, 551, 17, 40))
        self.end_ones_day.setStyleSheet("background-image: url(:/roller_numbers/elements/end_d_ones_4.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_ones_day.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_ones_day.setFrameShadow(QtGui.QFrame.Plain)
        self.end_ones_day.setObjectName("end_ones_day")
        self.end_tens_month = QtGui.QGraphicsView(self.bg)
        self.end_tens_month.setGeometry(QtCore.QRect(702, 551, 32, 41))
        self.end_tens_month.setStyleSheet("background-image: url(:/roller_numbers/elements/end_m_tens_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_tens_month.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_tens_month.setFrameShadow(QtGui.QFrame.Plain)
        self.end_tens_month.setObjectName("end_tens_month")
        self.run_minute_one = QtGui.QGraphicsView(self.bg)
        self.run_minute_one.setGeometry(QtCore.QRect(481, 269, 41, 61))
        self.run_minute_one.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/vt_9.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_minute_one.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_minute_one.setFrameShadow(QtGui.QFrame.Plain)
        self.run_minute_one.setObjectName("run_minute_one")
        self.end_tens_day = QtGui.QGraphicsView(self.bg)
        self.end_tens_day.setGeometry(QtCore.QRect(771, 550, 21, 43))
        self.end_tens_day.setStyleSheet("background-image: url(:/roller_numbers/elements/end_d_tens_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_tens_day.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_tens_day.setFrameShadow(QtGui.QFrame.Plain)
        self.end_tens_day.setObjectName("end_tens_day")
        self.run_second_ten = QtGui.QGraphicsView(self.bg)
        self.run_second_ten.setGeometry(QtCore.QRect(554, 269, 51, 61))
        self.run_second_ten.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/vt_2.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_second_ten.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_second_ten.setFrameShadow(QtGui.QFrame.Plain)
        self.run_second_ten.setObjectName("run_second_ten")
        self.start_ones_year = QtGui.QGraphicsView(self.bg)
        self.start_ones_year.setGeometry(QtCore.QRect(632, 551, 20, 42))
        self.start_ones_year.setStyleSheet("background-image: url(:/roller_numbers/elements/start_y_ones_9.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_ones_year.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_ones_year.setFrameShadow(QtGui.QFrame.Plain)
        self.start_ones_year.setObjectName("start_ones_year")
        self.start_ones_day = QtGui.QGraphicsView(self.bg)
        self.start_ones_day.setGeometry(QtCore.QRect(559, 551, 25, 40))
        self.start_ones_day.setStyleSheet("background-image: url(:/roller_numbers/elements/start_m_ones_4.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_ones_day.setFrameShape(QtGui.QFrame.NoFrame)
        self.start_ones_day.setFrameShadow(QtGui.QFrame.Plain)
        self.start_ones_day.setObjectName("start_ones_day")
        self.end_tens_year = QtGui.QGraphicsView(self.bg)
        self.end_tens_year.setGeometry(QtCore.QRect(831, 551, 31, 39))
        self.end_tens_year.setStyleSheet("background-image: url(:/roller_numbers/elements/end_y_tens_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_tens_year.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_tens_year.setFrameShadow(QtGui.QFrame.Plain)
        self.end_tens_year.setObjectName("end_tens_year")
        self.clock_button = QtGui.QPushButton(self.bg)
        self.clock_button.setGeometry(QtCore.QRect(619, 626, 118, 119))
        self.clock_button.setStyleSheet("background-image: url(:/lights buttons/elements/clock_button_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border-color: rgba(0, 0, 0, 0);")
        self.clock_button.setText("")
        self.clock_button.setObjectName("clock_button")
        self.run_minute_ten = QtGui.QGraphicsView(self.bg)
        self.run_minute_ten.setGeometry(QtCore.QRect(420, 267, 41, 61))
        self.run_minute_ten.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/vt_5.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_minute_ten.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_minute_ten.setFrameShadow(QtGui.QFrame.Plain)
        self.run_minute_ten.setObjectName("run_minute_ten")
        self.start_date_button = QtGui.QPushButton(self.bg)
        self.start_date_button.setGeometry(QtCore.QRect(631, 509, 31, 28))
        self.start_date_button.setStyleSheet("background-image: url(:/lights buttons/elements/start_date_button.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_date_button.setText("")
        self.start_date_button.setObjectName("start_date_button")
        self.green_light = QtGui.QGraphicsView(self.bg)
        self.green_light.setEnabled(True)
        self.green_light.setGeometry(QtCore.QRect(720, 353, 61, 61))
        self.green_light.setStyleSheet("background-image: url(:/lights buttons/elements/green_light_on.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.green_light.setFrameShape(QtGui.QFrame.NoFrame)
        self.green_light.setFrameShadow(QtGui.QFrame.Plain)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.green_light.setBackgroundBrush(brush)
        self.green_light.setObjectName("green_light")
        self.lower_output_sep = QtGui.QPlainTextEdit(self.bg)
        self.lower_output_sep.setGeometry(QtCore.QRect(694, 210, 206, 30))
        self.lower_output_sep.setStyleSheet("QPlainTextEdit{\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);\n"
"}\n"
"")
        self.lower_output_sep.setFrameShape(QtGui.QFrame.NoFrame)
        self.lower_output_sep.setFrameShadow(QtGui.QFrame.Plain)
        self.lower_output_sep.setLineWidth(0)
        self.lower_output_sep.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lower_output_sep.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lower_output_sep.setDocumentTitle("")
        self.lower_output_sep.setObjectName("lower_output_sep")
        self.lower_output = QtGui.QPlainTextEdit(self.bg)
        self.lower_output.setGeometry(QtCore.QRect(694, 222, 206, 108))
        self.lower_output.setStyleSheet("QPlainTextEdit{\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);\n"
"}\n"
"")
        self.lower_output.setFrameShape(QtGui.QFrame.NoFrame)
        self.lower_output.setFrameShadow(QtGui.QFrame.Plain)
        self.lower_output.setLineWidth(0)
        self.lower_output.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lower_output.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lower_output.setDocumentTitle("")
        self.lower_output.setObjectName("lower_output")
        self.entity_dropdown = QtGui.QComboBox(self.bg)
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
        self.entity_dropdown.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.entity_dropdown.setFrame(False)
        self.entity_dropdown.setObjectName("entity_dropdown")
        self.entity_dropdown.addItem("")
        self.end_ones_month = QtGui.QGraphicsView(self.bg)
        self.end_ones_month.setGeometry(QtCore.QRect(731, 551, 31, 39))
        self.end_ones_month.setStyleSheet("background-image: url(:/roller_numbers/elements/end_m_ones_6.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_ones_month.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_ones_month.setFrameShadow(QtGui.QFrame.Plain)
        self.end_ones_month.setObjectName("end_ones_month")
        self.task_dropdown = QtGui.QComboBox(self.bg)
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
        self.task_dropdown.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.task_dropdown.setFrame(False)
        self.task_dropdown.setObjectName("task_dropdown")
        self.task_dropdown.addItem("")
        self.project_dropdown = QtGui.QComboBox(self.bg)
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
        self.project_dropdown.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
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
        self.run_second_one = QtGui.QGraphicsView(self.bg)
        self.run_second_one.setGeometry(QtCore.QRect(611, 269, 41, 61))
        self.run_second_one.setStyleSheet("background-image: url(:/vaccuum_tube_numbers/elements/vt_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_second_one.setFrameShape(QtGui.QFrame.NoFrame)
        self.run_second_one.setFrameShadow(QtGui.QFrame.Plain)
        self.run_second_one.setObjectName("run_second_one")
        self.end_ones_year = QtGui.QGraphicsView(self.bg)
        self.end_ones_year.setGeometry(QtCore.QRect(859, 551, 33, 39))
        self.end_ones_year.setStyleSheet("background-image: url(:/roller_numbers/elements/end_y_ones_9.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_ones_year.setFrameShape(QtGui.QFrame.NoFrame)
        self.end_ones_year.setFrameShadow(QtGui.QFrame.Plain)
        self.end_ones_year.setObjectName("end_ones_year")
        self.time_hour = QtGui.QLabel(self.bg)
        self.time_hour.setGeometry(QtCore.QRect(110, 110, 168, 168))
        self.time_hour.setStyleSheet("image: none;")
        self.time_hour.setFrameShape(QtGui.QFrame.NoFrame)
        self.time_hour.setText("")
        self.time_hour.setTextFormat(QtCore.Qt.PlainText)
        self.time_hour.setPixmap(QtGui.QPixmap(":/dial hands/elements/clock_1_hour.png"))
        self.time_hour.setScaledContents(False)
        self.time_hour.setAlignment(QtCore.Qt.AlignCenter)
        self.time_hour.setObjectName("time_hour")
        self.time_minute = QtGui.QLabel(self.bg)
        self.time_minute.setGeometry(QtCore.QRect(110, 110, 168, 168))
        self.time_minute.setStyleSheet("image: none;")
        self.time_minute.setText("")
        self.time_minute.setPixmap(QtGui.QPixmap(":/dial hands/elements/clock_1_minute.png"))
        self.time_minute.setAlignment(QtCore.Qt.AlignCenter)
        self.time_minute.setObjectName("time_minute")
        self.day_meter = QtGui.QLabel(self.bg)
        self.day_meter.setGeometry(QtCore.QRect(305, 77, 192, 192))
        self.day_meter.setStyleSheet("image: none;")
        self.day_meter.setText("")
        self.day_meter.setPixmap(QtGui.QPixmap(":/dial hands/elements/meter_1_needle.png"))
        self.day_meter.setScaledContents(False)
        self.day_meter.setAlignment(QtCore.Qt.AlignCenter)
        self.day_meter.setObjectName("day_meter")
        self.week_meter = QtGui.QLabel(self.bg)
        self.week_meter.setGeometry(QtCore.QRect(481, 76, 192, 192))
        self.week_meter.setStyleSheet("image: none;")
        self.week_meter.setText("")
        self.week_meter.setPixmap(QtGui.QPixmap(":/dial hands/elements/meter_1_needle.png"))
        self.week_meter.setAlignment(QtCore.Qt.AlignCenter)
        self.week_meter.setObjectName("week_meter")
        self.start_clock_minute = QtGui.QLabel(self.bg)
        self.start_clock_minute.setGeometry(QtCore.QRect(512, 404, 115, 115))
        self.start_clock_minute.setStyleSheet("image: none;")
        self.start_clock_minute.setText("")
        self.start_clock_minute.setPixmap(QtGui.QPixmap(":/dial hands/elements/clock_2_minute.png"))
        self.start_clock_minute.setAlignment(QtCore.Qt.AlignCenter)
        self.start_clock_minute.setObjectName("start_clock_minute")
        self.start_clock_hour = QtGui.QLabel(self.bg)
        self.start_clock_hour.setGeometry(QtCore.QRect(512, 404, 115, 115))
        self.start_clock_hour.setStyleSheet("image: none;")
        self.start_clock_hour.setText("")
        self.start_clock_hour.setPixmap(QtGui.QPixmap(":/dial hands/elements/clock_2_hour.png"))
        self.start_clock_hour.setAlignment(QtCore.Qt.AlignCenter)
        self.start_clock_hour.setObjectName("start_clock_hour")
        self.end_clock_hour = QtGui.QLabel(self.bg)
        self.end_clock_hour.setGeometry(QtCore.QRect(724, 406, 115, 115))
        self.end_clock_hour.setStyleSheet("image: none;")
        self.end_clock_hour.setText("")
        self.end_clock_hour.setPixmap(QtGui.QPixmap(":/dial hands/elements/clock_3_hour.png"))
        self.end_clock_hour.setAlignment(QtCore.Qt.AlignCenter)
        self.end_clock_hour.setObjectName("end_clock_hour")
        self.end_clock_minute = QtGui.QLabel(self.bg)
        self.end_clock_minute.setGeometry(QtCore.QRect(724, 406, 115, 115))
        self.end_clock_minute.setStyleSheet("image: none;")
        self.end_clock_minute.setText("")
        self.end_clock_minute.setPixmap(QtGui.QPixmap(":/dial hands/elements/clock_3_minute.png"))
        self.end_clock_minute.setAlignment(QtCore.Qt.AlignCenter)
        self.end_clock_minute.setObjectName("end_clock_minute")
        self.output_trt = QtGui.QPlainTextEdit(self.bg)
        self.output_trt.setGeometry(QtCore.QRect(695, 114, 205, 17))
        self.output_trt.setStyleSheet("\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 10pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_trt.setFrameShape(QtGui.QFrame.NoFrame)
        self.output_trt.setFrameShadow(QtGui.QFrame.Plain)
        self.output_trt.setLineWidth(0)
        self.output_trt.setMidLineWidth(0)
        self.output_trt.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_trt.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_trt.setBackgroundVisible(False)
        self.output_trt.setObjectName("output_trt")
        self.output_start_end = QtGui.QPlainTextEdit(self.bg)
        self.output_start_end.setGeometry(QtCore.QRect(695, 130, 204, 30))
        self.output_start_end.setStyleSheet("\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 10pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_start_end.setFrameShape(QtGui.QFrame.NoFrame)
        self.output_start_end.setFrameShadow(QtGui.QFrame.Plain)
        self.output_start_end.setLineWidth(0)
        self.output_start_end.setMidLineWidth(0)
        self.output_start_end.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_start_end.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_start_end.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.output_start_end.setBackgroundVisible(False)
        self.output_start_end.setObjectName("output_start_end")
        self.output_user = QtGui.QPlainTextEdit(self.bg)
        self.output_user.setGeometry(QtCore.QRect(695, 160, 204, 17))
        self.output_user.setStyleSheet("\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 10pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_user.setFrameShape(QtGui.QFrame.NoFrame)
        self.output_user.setFrameShadow(QtGui.QFrame.Plain)
        self.output_user.setLineWidth(0)
        self.output_user.setMidLineWidth(0)
        self.output_user.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_user.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_user.setBackgroundVisible(False)
        self.output_user.setObjectName("output_user")
        self.output_daily = QtGui.QPlainTextEdit(self.bg)
        self.output_daily.setGeometry(QtCore.QRect(695, 176, 204, 17))
        self.output_daily.setStyleSheet("\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 10pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_daily.setFrameShape(QtGui.QFrame.NoFrame)
        self.output_daily.setFrameShadow(QtGui.QFrame.Plain)
        self.output_daily.setLineWidth(0)
        self.output_daily.setMidLineWidth(0)
        self.output_daily.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_daily.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_daily.setBackgroundVisible(False)
        self.output_daily.setObjectName("output_daily")
        self.output_weekly = QtGui.QPlainTextEdit(self.bg)
        self.output_weekly.setGeometry(QtCore.QRect(695, 192, 204, 17))
        self.output_weekly.setStyleSheet("\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 10pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_weekly.setFrameShape(QtGui.QFrame.NoFrame)
        self.output_weekly.setFrameShadow(QtGui.QFrame.Plain)
        self.output_weekly.setLineWidth(0)
        self.output_weekly.setMidLineWidth(0)
        self.output_weekly.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_weekly.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.output_weekly.setBackgroundVisible(False)
        self.output_weekly.setObjectName("output_weekly")
        TimeLord.setCentralWidget(self.centralwidget)
        self.actionCrash_Computer = QtGui.QAction(TimeLord)
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
        TimeLord.setWindowTitle(QtGui.QApplication.translate("TimeLord", "Time Lord", None, QtGui.QApplication.UnicodeUTF8))
        self.artist_label.setText(QtGui.QApplication.translate("TimeLord", "Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.output_monitor.setPlainText(QtGui.QApplication.translate("TimeLord", "OUTPUT MONITOR\n"
"------------------------------------", None, QtGui.QApplication.UnicodeUTF8))
        self.lower_output_sep.setPlainText(QtGui.QApplication.translate("TimeLord", "-------------------------------", None, QtGui.QApplication.UnicodeUTF8))
        self.lower_output.setPlainText(QtGui.QApplication.translate("TimeLord", "Raw Data Ouput", None, QtGui.QApplication.UnicodeUTF8))
        self.entity_dropdown.setItemText(0, QtGui.QApplication.translate("TimeLord", "Select Asset/Shot", None, QtGui.QApplication.UnicodeUTF8))
        self.task_dropdown.setItemText(0, QtGui.QApplication.translate("TimeLord", "Select Task", None, QtGui.QApplication.UnicodeUTF8))
        self.project_dropdown.setItemText(0, QtGui.QApplication.translate("TimeLord", "Select Project", None, QtGui.QApplication.UnicodeUTF8))
        self.output_trt.setPlainText(QtGui.QApplication.translate("TimeLord", "TRT: 00:12:24\n"
"", None, QtGui.QApplication.UnicodeUTF8))
        self.output_start_end.setPlainText(QtGui.QApplication.translate("TimeLord", "Start: 07/02/19\n"
"End:", None, QtGui.QApplication.UnicodeUTF8))
        self.output_user.setPlainText(QtGui.QApplication.translate("TimeLord", "USER CLOCKED IN", None, QtGui.QApplication.UnicodeUTF8))
        self.output_daily.setPlainText(QtGui.QApplication.translate("TimeLord", "Daily Total: 0", None, QtGui.QApplication.UnicodeUTF8))
        self.output_weekly.setPlainText(QtGui.QApplication.translate("TimeLord", "Weekly Total: 0  ", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCrash_Computer.setText(QtGui.QApplication.translate("TimeLord", "Crash Computer", None, QtGui.QApplication.UnicodeUTF8))

from resources import time_lord_resources_rc
