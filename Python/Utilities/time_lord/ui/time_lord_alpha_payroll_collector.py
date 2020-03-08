# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'time_lord_alpha_payroll_collector.ui'
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

from .resources import alpha_monitor_resources_rc

class Ui_QuickPayroll(object):
    def setupUi(self, QuickPayroll):
        if QuickPayroll.objectName():
            QuickPayroll.setObjectName(u"QuickPayroll")
        QuickPayroll.setMinimumSize(QSize(1081, 611))
        QuickPayroll.setMaximumSize(QSize(1081, 611))
        QuickPayroll.setAutoFillBackground(False)
        QuickPayroll.setStyleSheet(u"background-color: rgb(64, 72, 53);\n"
"color: rgba(133, 208, 120, 200);\n"
"font: 75 16pt \"System\";")
        self.frame = QFrame(QuickPayroll)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 1081, 612))
        self.frame.setMinimumSize(QSize(1081, 612))
        self.frame.setMaximumSize(QSize(1081, 612))
        self.frame.setStyleSheet(u"QFrame {\n"
"	image: url(:/elements/elements/Alpha_Monitor_background_drk.png);\n"
"	\n"
"	border-color: rgb(0, 0, 0);\n"
"}")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.main_title = QLabel(self.frame)
        self.main_title.setObjectName(u"main_title")
        self.main_title.setStyleSheet(u"font: 75 18pt \"System\";\n"
"image: url(:/elements/elements/pixel.png);\n"
"background-color: rgba(83, 91, 74, 0);")
        self.main_title.setPixmap(QPixmap(u":/elements/elements/pixel.png"))

        self.verticalLayout_3.addWidget(self.main_title)

        self.dashed_line = QLabel(self.frame)
        self.dashed_line.setObjectName(u"dashed_line")
        self.dashed_line.setStyleSheet(u"font: 16pt \"MS Shell Dlg 2\";\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/elements/elements/pixel.png);")

        self.verticalLayout_3.addWidget(self.dashed_line)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_7 = QSpacerItem(10, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_7)

        self.file_output_label = QLabel(self.frame)
        self.file_output_label.setObjectName(u"file_output_label")
        self.file_output_label.setStyleSheet(u"\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/bg/pixel.png);")

        self.horizontalLayout.addWidget(self.file_output_label)

        self.file_output = QLineEdit(self.frame)
        self.file_output.setObjectName(u"file_output")
        self.file_output.setStyleSheet(u"\n"
"QLineEdit {\n"
"    border: 2px dashed rgb(64, 72, 53);\n"
"	border-bottom-color: rgb(104, 208, 120);\n"
"    padding: 0 8px;\n"
"	background-color: rgba(64, 72, 53, 0);\n"
"	image: url(:/bg/pixel.png);\n"
"    selection-background-color: rgb(104, 208, 120);\n"
"}")
        self.file_output.setFrame(False)

        self.horizontalLayout.addWidget(self.file_output)

        self.file_output_btn = QPushButton(self.frame)
        self.file_output_btn.setObjectName(u"file_output_btn")
        font = QFont()
        font.setFamily(u"System")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.file_output_btn.setFont(font)
        self.file_output_btn.setAutoFillBackground(False)
        self.file_output_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: rgb(83, 91, 74);\n"
"	border-style: solid;\n"
"	border-width: 2px;\n"
"	image: url(:/bg/pixel.png);\n"
"	background-color: rgba(83, 91, 74, 0);\n"
"	border-color: rgb(133, 208, 120);\n"
"	border-radius: 7px;\n"
"	padding: 2px;\n"
"}")
        self.file_output_btn.setFlat(True)

        self.horizontalLayout.addWidget(self.file_output_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.start_date_label = QLabel(self.frame)
        self.start_date_label.setObjectName(u"start_date_label")
        self.start_date_label.setStyleSheet(u"\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/bg/pixel.png);")

        self.verticalLayout.addWidget(self.start_date_label)

        self.start_date = QDateEdit(self.frame)
        self.start_date.setObjectName(u"start_date")
        self.start_date.setStyleSheet(u"border: 1px solid rgb(104, 208, 120);\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/bg/pixel.png);")
        self.start_date.setFrame(False)
        self.start_date.setCalendarPopup(True)

        self.verticalLayout.addWidget(self.start_date)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalSpacer_2 = QSpacerItem(100, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.end_date_label = QLabel(self.frame)
        self.end_date_label.setObjectName(u"end_date_label")
        self.end_date_label.setStyleSheet(u"\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/bg/pixel.png);")

        self.verticalLayout_2.addWidget(self.end_date_label)

        self.end_date = QDateEdit(self.frame)
        self.end_date.setObjectName(u"end_date")
        self.end_date.setStyleSheet(u"border: 1px solid rgb(104, 208, 120);\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/bg/pixel.png);")
        self.end_date.setFrame(False)
        self.end_date.setCalendarPopup(True)

        self.verticalLayout_2.addWidget(self.end_date)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.cancel_btn = QPushButton(self.frame)
        self.cancel_btn.setObjectName(u"cancel_btn")
        self.cancel_btn.setFont(font)
        self.cancel_btn.setAutoFillBackground(False)
        self.cancel_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: rgba(83, 91, 74, 0);\n"
"	image: url(:/bg/pixel.png);\n"
"	border-style: solid;\n"
"	border-width: 2px;\n"
"	border-color: rgb(133, 208, 120);\n"
"	border-radius: 7px;\n"
"	padding: 2px;\n"
"}")
        self.cancel_btn.setFlat(True)

        self.horizontalLayout_3.addWidget(self.cancel_btn)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.process_btn = QPushButton(self.frame)
        self.process_btn.setObjectName(u"process_btn")
        self.process_btn.setFont(font)
        self.process_btn.setAutoFillBackground(False)
        self.process_btn.setStyleSheet(u"QPushButton{\n"
"	background-color: rgba(83, 91, 74, 0);\n"
"	image: url(:/bg/pixel.png);\n"
"	border-style: solid;\n"
"	border-width: 2px;\n"
"	border-color: rgb(133, 208, 120);\n"
"	border-radius: 7px;\n"
"	padding: 2px;\n"
"}")
        self.process_btn.setFlat(True)

        self.horizontalLayout_3.addWidget(self.process_btn)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_8)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.dashed_line_2 = QLabel(self.frame)
        self.dashed_line_2.setObjectName(u"dashed_line_2")
        self.dashed_line_2.setStyleSheet(u"font: 16pt \"MS Shell Dlg 2\";\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/bg/pixel.png);")

        self.verticalLayout_3.addWidget(self.dashed_line_2)

        self.screen_output = QTableWidget(self.frame)
        if (self.screen_output.columnCount() < 5):
            self.screen_output.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.screen_output.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.screen_output.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.screen_output.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.screen_output.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.screen_output.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.screen_output.setObjectName(u"screen_output")
        self.screen_output.setStyleSheet(u"image: url(:/elements/elements/pixel.png);\n"
"background-color: rgba(0, 0, 0, 0);")
        self.screen_output.setFrameShape(QFrame.NoFrame)
        self.screen_output.setShowGrid(False)
        self.screen_output.setGridStyle(Qt.NoPen)
        self.screen_output.horizontalHeader().setVisible(False)
        self.screen_output.horizontalHeader().setStretchLastSection(False)
        self.screen_output.verticalHeader().setVisible(False)

        self.verticalLayout_3.addWidget(self.screen_output)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.frame.raise_()
        self.file_output_btn.raise_()
        self.file_output.raise_()
        self.start_date_label.raise_()
        self.start_date.raise_()
        self.end_date_label.raise_()
        self.end_date.raise_()
        self.process_btn.raise_()
        self.cancel_btn.raise_()
        self.file_output_label.raise_()

        self.retranslateUi(QuickPayroll)

        QMetaObject.connectSlotsByName(QuickPayroll)
    # setupUi

    def retranslateUi(self, QuickPayroll):
        QuickPayroll.setWindowTitle(QCoreApplication.translate("QuickPayroll", u"Time Lord Alpha Payroll Collector", None))
        self.main_title.setText(QCoreApplication.translate("QuickPayroll", u"Time Lord Alpha Payroll Collector", None))
        self.dashed_line.setText(QCoreApplication.translate("QuickPayroll", u"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", None))
        self.file_output_label.setText(QCoreApplication.translate("QuickPayroll", u"File Output (.xls, .xlsx)", None))
        self.file_output_btn.setText(QCoreApplication.translate("QuickPayroll", u"Save As...", None))
        self.start_date_label.setText(QCoreApplication.translate("QuickPayroll", u"Start Date", None))
        self.end_date_label.setText(QCoreApplication.translate("QuickPayroll", u"End Date", None))
        self.cancel_btn.setText(QCoreApplication.translate("QuickPayroll", u"Close", None))
        self.process_btn.setText(QCoreApplication.translate("QuickPayroll", u"Process and Save", None))
        self.dashed_line_2.setText(QCoreApplication.translate("QuickPayroll", u"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", None))
        ___qtablewidgetitem = self.screen_output.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("QuickPayroll", u"Name", None));
        ___qtablewidgetitem1 = self.screen_output.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("QuickPayroll", u"Level", None));
        ___qtablewidgetitem2 = self.screen_output.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("QuickPayroll", u"New Column", None));
        ___qtablewidgetitem3 = self.screen_output.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("QuickPayroll", u"Sep", None));
        ___qtablewidgetitem4 = self.screen_output.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("QuickPayroll", u"Total", None));
    # retranslateUi

