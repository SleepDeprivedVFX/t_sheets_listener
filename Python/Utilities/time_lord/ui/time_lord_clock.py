# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'time_lord_clock.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

from .resources import time_lord_resources_rc

class Ui_TimeLord(object):
    def setupUi(self, TimeLord):
        if TimeLord.objectName():
            TimeLord.setObjectName(u"TimeLord")
        TimeLord.resize(978, 805)
        TimeLord.setMinimumSize(QSize(978, 805))
        TimeLord.setMaximumSize(QSize(978, 805))
        TimeLord.setStyleSheet(u"")
        self.actionCrash_Computer = QAction(TimeLord)
        self.actionCrash_Computer.setObjectName(u"actionCrash_Computer")
        self.centralwidget = QWidget(TimeLord)
        self.centralwidget.setObjectName(u"centralwidget")
        self.bg = QFrame(self.centralwidget)
        self.bg.setObjectName(u"bg")
        self.bg.setEnabled(True)
        self.bg.setGeometry(QRect(0, 0, 978, 805))
        self.bg.setStyleSheet(u"QFrame {\n"
"	image: url(:/backgrounds/time_lord_bg.png);\n"
"	\n"
"	border-color: rgb(0, 0, 0);\n"
"}")
        self.bg.setFrameShape(QFrame.Box)
        self.bg.setFrameShadow(QFrame.Plain)
        self.bg.setLineWidth(5)
        self.start_tens_month = QGraphicsView(self.bg)
        self.start_tens_month.setObjectName(u"start_tens_month")
        self.start_tens_month.setGeometry(QRect(463, 551, 31, 43))
        self.start_tens_month.setStyleSheet(u"background-image: url(:/roller_numbers/elements/start_m_tens_0.png);")
        self.start_tens_month.setFrameShape(QFrame.NoFrame)
        self.start_tens_month.setFrameShadow(QFrame.Plain)
        self.start_tens_year = QGraphicsView(self.bg)
        self.start_tens_year.setObjectName(u"start_tens_year")
        self.start_tens_year.setGeometry(QRect(602, 551, 21, 43))
        self.start_tens_year.setStyleSheet(u"background-image: url(:/roller_numbers/elements/start_y_tens_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_tens_year.setFrameShape(QFrame.NoFrame)
        self.start_tens_year.setFrameShadow(QFrame.Plain)
        self.end_date_button = QPushButton(self.bg)
        self.end_date_button.setObjectName(u"end_date_button")
        self.end_date_button.setGeometry(QRect(848, 508, 27, 28))
        self.end_date_button.setStyleSheet(u"background-image: url(:/lights buttons/elements/end_date_button.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_hour_one = QGraphicsView(self.bg)
        self.run_hour_one.setObjectName(u"run_hour_one")
        self.run_hour_one.setGeometry(QRect(341, 269, 41, 61))
        self.run_hour_one.setStyleSheet(u"background-image: url(:/vaccuum_tube_numbers/elements/vt_3.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_hour_one.setFrameShape(QFrame.NoFrame)
        self.run_hour_one.setFrameShadow(QFrame.Plain)
        self.red_light = QGraphicsView(self.bg)
        self.red_light.setObjectName(u"red_light")
        self.red_light.setGeometry(QRect(805, 352, 71, 61))
        self.red_light.setStyleSheet(u"background-image: url(:/lights buttons/elements/red_light_on.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.red_light.setFrameShape(QFrame.NoFrame)
        self.red_light.setFrameShadow(QFrame.Plain)
        self.start_ones_month = QGraphicsView(self.bg)
        self.start_ones_month.setObjectName(u"start_ones_month")
        self.start_ones_month.setGeometry(QRect(491, 551, 31, 42))
        self.start_ones_month.setStyleSheet(u"background-image: url(:/roller_numbers/elements/start_m_ones_6.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_ones_month.setFrameShape(QFrame.NoFrame)
        self.start_ones_month.setFrameShadow(QFrame.Plain)
        self.artist_label = QLabel(self.bg)
        self.artist_label.setObjectName(u"artist_label")
        self.artist_label.setGeometry(QRect(161, 440, 231, 40))
        font = QFont()
        font.setFamily(u"Calisto MT")
        font.setPointSize(22)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setKerning(True)
        self.artist_label.setFont(font)
        self.artist_label.setStyleSheet(u"background-image: url(:/backgrounds/elements/artist_name.png);\n"
"font:22pt \"Calisto MT\";\n"
"color: rgb(56, 9, 8);\n"
"background-repeat: none;\n"
"background-color: transparent;\n"
"image: none;")
        self.artist_label.setTextFormat(Qt.AutoText)
        self.artist_label.setMargin(0)
        self.start_tens_day = QGraphicsView(self.bg)
        self.start_tens_day.setObjectName(u"start_tens_day")
        self.start_tens_day.setGeometry(QRect(531, 550, 22, 45))
        self.start_tens_day.setStyleSheet(u"background-image: url(:/roller_numbers/elements/start_d_tens_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_tens_day.setFrameShape(QFrame.NoFrame)
        self.start_tens_day.setFrameShadow(QFrame.Plain)
        self.run_hour_ten = QGraphicsView(self.bg)
        self.run_hour_ten.setObjectName(u"run_hour_ten")
        self.run_hour_ten.setGeometry(QRect(281, 269, 41, 61))
        self.run_hour_ten.setStyleSheet(u"background-image: url(:/vaccuum_tube_numbers/elements/vt_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_hour_ten.setFrameShape(QFrame.NoFrame)
        self.run_hour_ten.setFrameShadow(QFrame.Plain)
        self.output_monitor = QPlainTextEdit(self.bg)
        self.output_monitor.setObjectName(u"output_monitor")
        self.output_monitor.setGeometry(QRect(694, 89, 205, 26))
        self.output_monitor.setStyleSheet(u"\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 7pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_monitor.setFrameShape(QFrame.NoFrame)
        self.output_monitor.setFrameShadow(QFrame.Plain)
        self.output_monitor.setLineWidth(0)
        self.output_monitor.setMidLineWidth(0)
        self.output_monitor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_monitor.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_monitor.setBackgroundVisible(False)
        self.end_ones_day = QGraphicsView(self.bg)
        self.end_ones_day.setObjectName(u"end_ones_day")
        self.end_ones_day.setGeometry(QRect(800, 551, 17, 40))
        self.end_ones_day.setStyleSheet(u"background-image: url(:/roller_numbers/elements/end_d_ones_4.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_ones_day.setFrameShape(QFrame.NoFrame)
        self.end_ones_day.setFrameShadow(QFrame.Plain)
        self.end_tens_month = QGraphicsView(self.bg)
        self.end_tens_month.setObjectName(u"end_tens_month")
        self.end_tens_month.setGeometry(QRect(702, 551, 32, 41))
        self.end_tens_month.setStyleSheet(u"background-image: url(:/roller_numbers/elements/end_m_tens_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_tens_month.setFrameShape(QFrame.NoFrame)
        self.end_tens_month.setFrameShadow(QFrame.Plain)
        self.run_minute_one = QGraphicsView(self.bg)
        self.run_minute_one.setObjectName(u"run_minute_one")
        self.run_minute_one.setGeometry(QRect(481, 269, 41, 61))
        self.run_minute_one.setStyleSheet(u"background-image: url(:/vaccuum_tube_numbers/elements/vt_9.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_minute_one.setFrameShape(QFrame.NoFrame)
        self.run_minute_one.setFrameShadow(QFrame.Plain)
        self.end_tens_day = QGraphicsView(self.bg)
        self.end_tens_day.setObjectName(u"end_tens_day")
        self.end_tens_day.setGeometry(QRect(771, 550, 21, 43))
        self.end_tens_day.setStyleSheet(u"background-image: url(:/roller_numbers/elements/end_d_tens_0.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_tens_day.setFrameShape(QFrame.NoFrame)
        self.end_tens_day.setFrameShadow(QFrame.Plain)
        self.run_second_ten = QGraphicsView(self.bg)
        self.run_second_ten.setObjectName(u"run_second_ten")
        self.run_second_ten.setGeometry(QRect(554, 269, 51, 61))
        self.run_second_ten.setStyleSheet(u"background-image: url(:/vaccuum_tube_numbers/elements/vt_2.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_second_ten.setFrameShape(QFrame.NoFrame)
        self.run_second_ten.setFrameShadow(QFrame.Plain)
        self.start_ones_year = QGraphicsView(self.bg)
        self.start_ones_year.setObjectName(u"start_ones_year")
        self.start_ones_year.setGeometry(QRect(632, 551, 20, 42))
        self.start_ones_year.setStyleSheet(u"background-image: url(:/roller_numbers/elements/start_y_ones_9.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_ones_year.setFrameShape(QFrame.NoFrame)
        self.start_ones_year.setFrameShadow(QFrame.Plain)
        self.start_ones_day = QGraphicsView(self.bg)
        self.start_ones_day.setObjectName(u"start_ones_day")
        self.start_ones_day.setGeometry(QRect(559, 551, 25, 40))
        self.start_ones_day.setStyleSheet(u"background-image: url(:/roller_numbers/elements/start_m_ones_4.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.start_ones_day.setFrameShape(QFrame.NoFrame)
        self.start_ones_day.setFrameShadow(QFrame.Plain)
        self.end_tens_year = QGraphicsView(self.bg)
        self.end_tens_year.setObjectName(u"end_tens_year")
        self.end_tens_year.setGeometry(QRect(831, 551, 31, 39))
        self.end_tens_year.setStyleSheet(u"background-image: url(:/roller_numbers/elements/end_y_tens_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_tens_year.setFrameShape(QFrame.NoFrame)
        self.end_tens_year.setFrameShadow(QFrame.Plain)
        self.clock_button = QPushButton(self.bg)
        self.clock_button.setObjectName(u"clock_button")
        self.clock_button.setGeometry(QRect(619, 626, 118, 119))
        self.clock_button.setStyleSheet(u"background-image: url(:/lights buttons/elements/clock_button_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);\n"
"border-color: rgba(0, 0, 0, 0);")
        self.run_minute_ten = QGraphicsView(self.bg)
        self.run_minute_ten.setObjectName(u"run_minute_ten")
        self.run_minute_ten.setGeometry(QRect(420, 267, 41, 61))
        self.run_minute_ten.setStyleSheet(u"background-image: url(:/vaccuum_tube_numbers/elements/vt_5.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_minute_ten.setFrameShape(QFrame.NoFrame)
        self.run_minute_ten.setFrameShadow(QFrame.Plain)
        self.start_date_button = QPushButton(self.bg)
        self.start_date_button.setObjectName(u"start_date_button")
        self.start_date_button.setGeometry(QRect(631, 509, 31, 28))
        self.start_date_button.setStyleSheet(u"background-image: url(:/lights buttons/elements/start_date_button.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.green_light = QGraphicsView(self.bg)
        self.green_light.setObjectName(u"green_light")
        self.green_light.setEnabled(True)
        self.green_light.setGeometry(QRect(720, 353, 61, 61))
        self.green_light.setStyleSheet(u"background-image: url(:/lights buttons/elements/green_light_on.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.green_light.setFrameShape(QFrame.NoFrame)
        self.green_light.setFrameShadow(QFrame.Plain)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.NoBrush)
        self.green_light.setBackgroundBrush(brush)
        self.lower_output = QPlainTextEdit(self.bg)
        self.lower_output.setObjectName(u"lower_output")
        self.lower_output.setGeometry(QRect(694, 187, 206, 152))
        self.lower_output.setStyleSheet(u"QPlainTextEdit{\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);\n"
"}\n"
"")
        self.lower_output.setFrameShape(QFrame.NoFrame)
        self.lower_output.setFrameShadow(QFrame.Plain)
        self.lower_output.setLineWidth(0)
        self.lower_output.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.lower_output.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.lower_output.setTextInteractionFlags(Qt.NoTextInteraction)
        self.entity_dropdown = QComboBox(self.bg)
        self.entity_dropdown.addItem("")
        self.entity_dropdown.setObjectName(u"entity_dropdown")
        self.entity_dropdown.setGeometry(QRect(151, 609, 242, 39))
        self.entity_dropdown.setStyleSheet(u"background-image: url(:/backgrounds/elements/entity_bg.png);\n"
"padding-left: 5px;\n"
"background-repeat: none;\n"
"background-color: rgba(118, 104, 79, 80);\n"
"font: 16pt \"Calisto MT\";\n"
"color: rgb(56, 9, 8);\n"
"subcontrol-origin: padding;\n"
"subcontrol-position: top right;\n"
"selection-background-color: rgba(118, 104, 79, 0);")
        self.entity_dropdown.setInsertPolicy(QComboBox.InsertAlphabetically)
        self.entity_dropdown.setFrame(False)
        self.end_ones_month = QGraphicsView(self.bg)
        self.end_ones_month.setObjectName(u"end_ones_month")
        self.end_ones_month.setGeometry(QRect(731, 551, 31, 39))
        self.end_ones_month.setStyleSheet(u"background-image: url(:/roller_numbers/elements/end_m_ones_6.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_ones_month.setFrameShape(QFrame.NoFrame)
        self.end_ones_month.setFrameShadow(QFrame.Plain)
        self.task_dropdown = QComboBox(self.bg)
        self.task_dropdown.addItem("")
        self.task_dropdown.setObjectName(u"task_dropdown")
        self.task_dropdown.setGeometry(QRect(151, 679, 242, 34))
        self.task_dropdown.setStyleSheet(u"background-image: url(:/backgrounds/elements/task_bg.png);\n"
"padding-left: 5px;\n"
"background-color: rgba(118, 104, 79, 80);\n"
"background-repeat: none;\n"
"font: 16pt \"Calisto MT\";\n"
"color: rgb(56, 9, 8);\n"
"subcontrol-origin: padding;\n"
"subcontrol-position: top right;\n"
"selection-background-color: rgba(118, 104, 79, 0);")
        self.task_dropdown.setInsertPolicy(QComboBox.InsertAlphabetically)
        self.task_dropdown.setFrame(False)
        self.project_dropdown = QComboBox(self.bg)
        icon = QIcon()
        icon.addFile(u":/backgrounds/elements/project_bg.png", QSize(), QIcon.Normal, QIcon.Off)
        icon.addFile(u":/backgrounds/elements/project_bg.png", QSize(), QIcon.Normal, QIcon.On)
        icon.addFile(u":/backgrounds/elements/project_bg.png", QSize(), QIcon.Active, QIcon.Off)
        icon.addFile(u":/backgrounds/elements/project_bg.png", QSize(), QIcon.Active, QIcon.On)
        icon.addFile(u":/backgrounds/elements/project_bg.png", QSize(), QIcon.Selected, QIcon.Off)
        icon.addFile(u":/backgrounds/elements/project_bg.png", QSize(), QIcon.Selected, QIcon.On)
        self.project_dropdown.addItem(icon, "")
        self.project_dropdown.setObjectName(u"project_dropdown")
        self.project_dropdown.setGeometry(QRect(153, 547, 240, 33))
        self.project_dropdown.setAutoFillBackground(False)
        self.project_dropdown.setStyleSheet(u"image: url(:/backgrounds/elements/project_bar.png);\n"
"padding-left: 5px;\n"
"background-color: rgba(118, 104, 79, 80);\n"
"background-repeat: none;\n"
"font: 16pt \"Calisto MT\";\n"
"color: rgb(56, 9, 8);\n"
"subcontrol-origin: padding;\n"
"subcontrol-position: top right;\n"
"selection-background-color: rgba(118, 104, 79, 0);")
        self.project_dropdown.setEditable(False)
        self.project_dropdown.setInsertPolicy(QComboBox.InsertAlphabetically)
        self.project_dropdown.setFrame(False)
        self.run_second_one = QGraphicsView(self.bg)
        self.run_second_one.setObjectName(u"run_second_one")
        self.run_second_one.setGeometry(QRect(611, 269, 41, 61))
        self.run_second_one.setStyleSheet(u"background-image: url(:/vaccuum_tube_numbers/elements/vt_1.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.run_second_one.setFrameShape(QFrame.NoFrame)
        self.run_second_one.setFrameShadow(QFrame.Plain)
        self.end_ones_year = QGraphicsView(self.bg)
        self.end_ones_year.setObjectName(u"end_ones_year")
        self.end_ones_year.setGeometry(QRect(859, 551, 33, 39))
        self.end_ones_year.setStyleSheet(u"background-image: url(:/roller_numbers/elements/end_y_ones_9.png);\n"
"background-repeat: none;\n"
"background-color: rgba(0, 0, 0, 0);")
        self.end_ones_year.setFrameShape(QFrame.NoFrame)
        self.end_ones_year.setFrameShadow(QFrame.Plain)
        self.time_hour = QLabel(self.bg)
        self.time_hour.setObjectName(u"time_hour")
        self.time_hour.setGeometry(QRect(110, 110, 168, 168))
        self.time_hour.setStyleSheet(u"image: none;")
        self.time_hour.setFrameShape(QFrame.NoFrame)
        self.time_hour.setTextFormat(Qt.PlainText)
        self.time_hour.setPixmap(QPixmap(u":/dial hands/elements/clock_1_hour.png"))
        self.time_hour.setScaledContents(False)
        self.time_hour.setAlignment(Qt.AlignCenter)
        self.time_minute = QLabel(self.bg)
        self.time_minute.setObjectName(u"time_minute")
        self.time_minute.setGeometry(QRect(110, 110, 168, 168))
        self.time_minute.setStyleSheet(u"image: none;")
        self.time_minute.setPixmap(QPixmap(u":/dial hands/elements/clock_1_minute.png"))
        self.time_minute.setAlignment(Qt.AlignCenter)
        self.day_meter = QLabel(self.bg)
        self.day_meter.setObjectName(u"day_meter")
        self.day_meter.setGeometry(QRect(305, 77, 192, 192))
        self.day_meter.setStyleSheet(u"image: none;")
        self.day_meter.setPixmap(QPixmap(u":/dial hands/elements/meter_1_needle.png"))
        self.day_meter.setScaledContents(False)
        self.day_meter.setAlignment(Qt.AlignCenter)
        self.week_meter = QLabel(self.bg)
        self.week_meter.setObjectName(u"week_meter")
        self.week_meter.setGeometry(QRect(481, 76, 192, 192))
        self.week_meter.setStyleSheet(u"image: none;")
        self.week_meter.setPixmap(QPixmap(u":/dial hands/elements/meter_1_needle.png"))
        self.week_meter.setAlignment(Qt.AlignCenter)
        self.start_clock_minute = QLabel(self.bg)
        self.start_clock_minute.setObjectName(u"start_clock_minute")
        self.start_clock_minute.setGeometry(QRect(512, 404, 115, 115))
        self.start_clock_minute.setStyleSheet(u"image: none;")
        self.start_clock_minute.setPixmap(QPixmap(u":/dial hands/elements/clock_2_minute.png"))
        self.start_clock_minute.setAlignment(Qt.AlignCenter)
        self.start_clock_hour = QLabel(self.bg)
        self.start_clock_hour.setObjectName(u"start_clock_hour")
        self.start_clock_hour.setGeometry(QRect(512, 404, 115, 115))
        self.start_clock_hour.setStyleSheet(u"image: none;")
        self.start_clock_hour.setPixmap(QPixmap(u":/dial hands/elements/clock_2_hour.png"))
        self.start_clock_hour.setAlignment(Qt.AlignCenter)
        self.end_clock_hour = QLabel(self.bg)
        self.end_clock_hour.setObjectName(u"end_clock_hour")
        self.end_clock_hour.setGeometry(QRect(724, 406, 115, 115))
        self.end_clock_hour.setStyleSheet(u"image: none;")
        self.end_clock_hour.setPixmap(QPixmap(u":/dial hands/elements/clock_3_hour.png"))
        self.end_clock_hour.setAlignment(Qt.AlignCenter)
        self.end_clock_minute = QLabel(self.bg)
        self.end_clock_minute.setObjectName(u"end_clock_minute")
        self.end_clock_minute.setGeometry(QRect(724, 406, 115, 115))
        self.end_clock_minute.setStyleSheet(u"image: none;")
        self.end_clock_minute.setPixmap(QPixmap(u":/dial hands/elements/clock_3_minute.png"))
        self.end_clock_minute.setAlignment(Qt.AlignCenter)
        self.output_trt = QPlainTextEdit(self.bg)
        self.output_trt.setObjectName(u"output_trt")
        self.output_trt.setGeometry(QRect(695, 111, 205, 17))
        self.output_trt.setStyleSheet(u"\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_trt.setFrameShape(QFrame.NoFrame)
        self.output_trt.setFrameShadow(QFrame.Plain)
        self.output_trt.setLineWidth(0)
        self.output_trt.setMidLineWidth(0)
        self.output_trt.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_trt.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_trt.setTextInteractionFlags(Qt.NoTextInteraction)
        self.output_trt.setBackgroundVisible(False)
        self.output_start_end = QPlainTextEdit(self.bg)
        self.output_start_end.setObjectName(u"output_start_end")
        self.output_start_end.setGeometry(QRect(695, 122, 204, 28))
        self.output_start_end.setStyleSheet(u"\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_start_end.setFrameShape(QFrame.NoFrame)
        self.output_start_end.setFrameShadow(QFrame.Plain)
        self.output_start_end.setLineWidth(0)
        self.output_start_end.setMidLineWidth(0)
        self.output_start_end.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_start_end.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_start_end.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.output_start_end.setTextInteractionFlags(Qt.NoTextInteraction)
        self.output_start_end.setBackgroundVisible(False)
        self.output_user = QPlainTextEdit(self.bg)
        self.output_user.setObjectName(u"output_user")
        self.output_user.setGeometry(QRect(695, 145, 204, 20))
        self.output_user.setStyleSheet(u"\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_user.setFrameShape(QFrame.NoFrame)
        self.output_user.setFrameShadow(QFrame.Plain)
        self.output_user.setLineWidth(0)
        self.output_user.setMidLineWidth(0)
        self.output_user.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_user.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_user.setTextInteractionFlags(Qt.NoTextInteraction)
        self.output_user.setBackgroundVisible(False)
        self.output_daily = QPlainTextEdit(self.bg)
        self.output_daily.setObjectName(u"output_daily")
        self.output_daily.setGeometry(QRect(695, 157, 204, 17))
        self.output_daily.setStyleSheet(u"\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_daily.setFrameShape(QFrame.NoFrame)
        self.output_daily.setFrameShadow(QFrame.Plain)
        self.output_daily.setLineWidth(0)
        self.output_daily.setMidLineWidth(0)
        self.output_daily.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_daily.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_daily.setTextInteractionFlags(Qt.NoTextInteraction)
        self.output_daily.setBackgroundVisible(False)
        self.output_weekly = QPlainTextEdit(self.bg)
        self.output_weekly.setObjectName(u"output_weekly")
        self.output_weekly.setGeometry(QRect(695, 170, 204, 17))
        self.output_weekly.setStyleSheet(u"\n"
"border-color: rgba(0, 0, 0, 0);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"font: 75 8pt \"MS UI Gothic\";\n"
"color: rgb(130, 231, 130);")
        self.output_weekly.setFrameShape(QFrame.NoFrame)
        self.output_weekly.setFrameShadow(QFrame.Plain)
        self.output_weekly.setLineWidth(0)
        self.output_weekly.setMidLineWidth(0)
        self.output_weekly.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_weekly.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_weekly.setTextInteractionFlags(Qt.NoTextInteraction)
        self.output_weekly.setBackgroundVisible(False)
        TimeLord.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.clock_button, self.project_dropdown)
        QWidget.setTabOrder(self.project_dropdown, self.entity_dropdown)
        QWidget.setTabOrder(self.entity_dropdown, self.task_dropdown)
        QWidget.setTabOrder(self.task_dropdown, self.start_date_button)
        QWidget.setTabOrder(self.start_date_button, self.end_date_button)
        QWidget.setTabOrder(self.end_date_button, self.run_hour_ten)
        QWidget.setTabOrder(self.run_hour_ten, self.run_hour_one)
        QWidget.setTabOrder(self.run_hour_one, self.run_minute_ten)
        QWidget.setTabOrder(self.run_minute_ten, self.run_minute_one)
        QWidget.setTabOrder(self.run_minute_one, self.run_second_ten)
        QWidget.setTabOrder(self.run_second_ten, self.run_second_one)
        QWidget.setTabOrder(self.run_second_one, self.start_tens_month)
        QWidget.setTabOrder(self.start_tens_month, self.start_ones_month)
        QWidget.setTabOrder(self.start_ones_month, self.start_tens_day)
        QWidget.setTabOrder(self.start_tens_day, self.start_ones_day)
        QWidget.setTabOrder(self.start_ones_day, self.start_tens_year)
        QWidget.setTabOrder(self.start_tens_year, self.start_ones_year)
        QWidget.setTabOrder(self.start_ones_year, self.end_tens_month)
        QWidget.setTabOrder(self.end_tens_month, self.end_ones_month)
        QWidget.setTabOrder(self.end_ones_month, self.end_tens_day)
        QWidget.setTabOrder(self.end_tens_day, self.end_ones_day)
        QWidget.setTabOrder(self.end_ones_day, self.end_tens_year)
        QWidget.setTabOrder(self.end_tens_year, self.end_ones_year)
        QWidget.setTabOrder(self.end_ones_year, self.red_light)
        QWidget.setTabOrder(self.red_light, self.green_light)
        QWidget.setTabOrder(self.green_light, self.output_monitor)
        QWidget.setTabOrder(self.output_monitor, self.lower_output)

        self.retranslateUi(TimeLord)

        QMetaObject.connectSlotsByName(TimeLord)
    # setupUi

    def retranslateUi(self, TimeLord):
        TimeLord.setWindowTitle(QCoreApplication.translate("TimeLord", u"Time Lord", None))
        self.actionCrash_Computer.setText(QCoreApplication.translate("TimeLord", u"Crash Computer", None))
#if QT_CONFIG(tooltip)
        self.start_tens_month.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Start Month</span><span style=\" color:#010101;\"><br/>The month record of the current timesheet.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.start_tens_year.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Start Year</span><span style=\" color:#010101;\"><br/>The year record of the current timesheet.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.end_date_button.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Set End Time Button</span><span style=\" color:#010101;\"><br/>This will manually set the end time for the latest timesheet.  If you are clocked in, it will clock you out at the time you set.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.end_date_button.setText("")
#if QT_CONFIG(tooltip)
        self.run_hour_one.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Running Time Hours</span><span style=\" color:#010101;\"><br/>The total hours recorded on the current timesheet task</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.red_light.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Error Light</span><span style=\" color:#010101;\"><br/>This light comes on when something is not kosher.  Either the selected Project/Entity/Task is not valid, or something has gone wrong!  See the Output Window.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.start_ones_month.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Start Month</span><span style=\" color:#010101;\"><br/>The month record of the current timesheet.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.artist_label.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Artist Name</span><span style=\" color:#010101;\"><br/>Set by the system by default. If you </span><span style=\" font-weight:600; color:#010101;\">do not</span><span style=\" color:#010101;\"> see your name here, chances are that this won't clock you in properly.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.artist_label.setText(QCoreApplication.translate("TimeLord", u"Artist", None))
#if QT_CONFIG(tooltip)
        self.start_tens_day.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Start Day</span><span style=\" color:#010101;\"><br/>The day record of the current timesheet.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.run_hour_ten.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Running Time Hours</span><span style=\" color:#010101;\"><br/>The total hours recorded on the current timesheet task</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.output_monitor.setPlainText(QCoreApplication.translate("TimeLord", u"OUTPUT MONITOR\n"
"------------------------------------", None))
#if QT_CONFIG(tooltip)
        self.end_ones_day.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">End Day</span><span style=\" color:#010101;\"><br/>The end day record of the current timesheet.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.end_tens_month.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">End Month</span><span style=\" color:#010101;\"><br/>The end month record of the current timesheet.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.run_minute_one.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Running Time Minutes</span><span style=\" color:#010101;\"><br/>The total minutes recorded on the current timesheet task</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.end_tens_day.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">End Day</span><span style=\" color:#010101;\"><br/>The end day record of the current timesheet.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.run_second_ten.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Running Time Seconds</span><span style=\" color:#010101;\"><br/>The total seconds recorded on the current timesheet task</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.start_ones_year.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Start Year</span><span style=\" color:#010101;\"><br/>The year record of the current timesheet.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.start_ones_day.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#030303;\">Start Day</span><span style=\" color:#030303;\"><br/>The day record of the current timesheet.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.end_tens_year.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">End Year</span><span style=\" color:#010101;\"><br/>The end year record of the current timesheet.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.clock_button.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600;\">Clock In/Out/Switch Button<br/></span>This button clocks you in, out or switches your timesheet</p><p><span style=\" font-weight:600; color:#00aa00;\">Green</span><span style=\" font-weight:600;\">:  </span><span style=\" font-style:italic;\">Clock in<br/></span><span style=\" font-weight:600; color:#ce0000;\">Red</span><span style=\" font-weight:600;\">:      </span><span style=\" font-style:italic;\">Clock Out<br/></span><span style=\" font-weight:600; color:#b1b100;\">Yellow</span><span style=\" font-weight:600;\">: </span><span style=\" font-style:italic;\">Switch Tasks</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.clock_button.setText("")
#if QT_CONFIG(tooltip)
        self.run_minute_ten.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Running Time Minutes</span><span style=\" color:#010101;\"><br/>The total minutes recorded on the current timesheet task</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.start_date_button.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Set Start Time Button<br/></span><span style=\" color:#010101;\">This will manually set the start time. If you are clocked in, it will adjust the current timesheet. If you are clocked out, it will set the time you would like to clock in to.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.start_date_button.setText("")
#if QT_CONFIG(tooltip)
        self.green_light.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Activity Light</span><span style=\" color:#0a0a0a;\"><br/>Will be steady on, or flashing when things are either being processed, or are going well.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.lower_output.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Output Window<br/></span><span style=\" color:#0a0a0a;\">This displays functional information from under the hood of the Time Lord. Error and status messages can be found here.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.lower_output.setDocumentTitle("")
        self.lower_output.setPlainText(QCoreApplication.translate("TimeLord", u"Raw Data Ouput", None))
        self.entity_dropdown.setItemText(0, QCoreApplication.translate("TimeLord", u"Select Asset/Shot", None))

#if QT_CONFIG(tooltip)
        self.entity_dropdown.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Entity Dropdown</span><span style=\" color:#010101;\"><br/>Sets either the Asset Entity or Shot entity that you are working on. Displays current values if you are clocked in.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.end_ones_month.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">End Month</span><span style=\" color:#010101;\"><br/>The end month record of the current timesheet.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.task_dropdown.setItemText(0, QCoreApplication.translate("TimeLord", u"Select Task", None))

#if QT_CONFIG(tooltip)
        self.task_dropdown.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Task Dropdown</span><span style=\" color:#010101;\"><br/>The actual task you are working on.  If you are clocked in, it displays the current task.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.project_dropdown.setItemText(0, QCoreApplication.translate("TimeLord", u"Select Project", None))

#if QT_CONFIG(tooltip)
        self.project_dropdown.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#020202;\">Project Dropdown<br/></span><span style=\" color:#020202;\">Sets the project that will be clocked in to.  If you are already clocked in, it will display what you are currently clocked in to.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.run_second_one.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Running Time Seconds</span><span style=\" color:#010101;\"><br/>The total seconds recorded on the current timesheet task</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.end_ones_year.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">End Year</span><span style=\" color:#010101;\"><br/>The end year record of the current timesheet.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.time_hour.setText("")
#if QT_CONFIG(tooltip)
        self.time_minute.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#0b0b0b;\">Real Time Clock</span><span style=\" color:#0b0b0b;\"><br/>This is what time it is now.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.time_minute.setText("")
#if QT_CONFIG(tooltip)
        self.day_meter.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Daily Total Meter<br/></span><span style=\" color:#0a0a0a;\">Graphically displays the amount of hours worked so far.  Red line indicates Over Time.</span><span style=\" color:#0a0a0a;\"><br/>Today: %s hrs</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.day_meter.setText("")
#if QT_CONFIG(tooltip)
        self.week_meter.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600;\">Weekly Total Meter</span><br/>Graphically displays the hours accumulated for the week.  A red line indicates over time<br/>Total: %s hrs</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.week_meter.setText("")
        self.start_clock_minute.setText("")
#if QT_CONFIG(tooltip)
        self.start_clock_hour.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Current Task Start Time</span><span style=\" color:#010101;\"><br/>Shows the time of the latest timesheet start time</span><span style=\" color:#010101;\">. If you're not clocked in, this is the Current Time.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.start_clock_hour.setText("")
        self.end_clock_hour.setText("")
#if QT_CONFIG(tooltip)
        self.end_clock_minute.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#010101;\">Current Timesheet Out Time</span><span style=\" color:#010101;\"><br/>Shows the out time of the latest timesheet. If you are Clocked in, this is the Current Time.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.end_clock_minute.setText("")
#if QT_CONFIG(tooltip)
        self.output_trt.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Total Running Time</span><span style=\" color:#0a0a0a;\"><br/>Displays TRT for the current Timesheet.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.output_trt.setPlainText(QCoreApplication.translate("TimeLord", u"TRT: 00:12:24\n"
"", None))
#if QT_CONFIG(tooltip)
        self.output_start_end.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Current Start and End Times<br/></span><span style=\" color:#0a0a0a;\">Shows when the Current Timesheet Was clocked in and out.  If you are clocked in, the End is the current time.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.output_start_end.setPlainText(QCoreApplication.translate("TimeLord", u"Start: 07/02/19\n"
"End:", None))
#if QT_CONFIG(tooltip)
        self.output_user.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Clocked In Status</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.output_user.setPlainText(QCoreApplication.translate("TimeLord", u"USER CLOCKED IN", None))
#if QT_CONFIG(tooltip)
        self.output_daily.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Daily Total</span><span style=\" color:#0a0a0a;\"><br/>Daily total of hours worked so far.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.output_daily.setPlainText(QCoreApplication.translate("TimeLord", u"Daily Total: 6", None))
#if QT_CONFIG(tooltip)
        self.output_weekly.setToolTip(QCoreApplication.translate("TimeLord", u"<html><head/><body><p><span style=\" font-weight:600; color:#0a0a0a;\">Weekly Total</span><span style=\" color:#0a0a0a;\"><br/>Weekly Total of Hours worked so far.</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.output_weekly.setPlainText(QCoreApplication.translate("TimeLord", u"Weekly Total: 18", None))
    # retranslateUi

