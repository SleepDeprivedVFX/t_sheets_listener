# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_alpha_payroll_collector.ui'
#
# Created: Wed Nov 13 10:57:01 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_QuickPayroll(object):
    def setupUi(self, QuickPayroll):
        QuickPayroll.setObjectName("QuickPayroll")
        QuickPayroll.setAutoFillBackground(False)
        QuickPayroll.setStyleSheet("background-color: rgb(64, 72, 53);\n"
"color: rgba(133, 208, 120, 200);\n"
"font: 75 16pt \"System\";")
        self.frame = QtGui.QFrame(QuickPayroll)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1081, 612))
        self.frame.setMinimumSize(QtCore.QSize(1081, 612))
        self.frame.setMaximumSize(QtCore.QSize(1081, 612))
        self.frame.setStyleSheet("QFrame {\n"
"    image: url(:/elements/elements/Alpha_Monitor_background_drk.png);\n"
"    \n"
"    border-color: rgb(0, 0, 0);\n"
"}")
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.main_title = QtGui.QLabel(self.frame)
        self.main_title.setStyleSheet("font: 75 18pt \"System\";\n"
"image: url(:/elements/elements/pixel.png);\n"
"background-color: rgba(83, 91, 74, 0);")
        self.main_title.setPixmap(QtGui.QPixmap(":/elements/elements/pixel.png"))
        self.main_title.setObjectName("main_title")
        self.verticalLayout_3.addWidget(self.main_title)
        self.dashed_line = QtGui.QLabel(self.frame)
        self.dashed_line.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/elements/elements/pixel.png);")
        self.dashed_line.setObjectName("dashed_line")
        self.verticalLayout_3.addWidget(self.dashed_line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.file_output_label = QtGui.QLabel(self.frame)
        self.file_output_label.setStyleSheet("\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/bg/pixel.png);")
        self.file_output_label.setObjectName("file_output_label")
        self.horizontalLayout.addWidget(self.file_output_label)
        self.file_output = QtGui.QLineEdit(self.frame)
        self.file_output.setStyleSheet("\n"
"QLineEdit {\n"
"    border: 2px dashed rgb(64, 72, 53);\n"
"    border-bottom-color: rgb(104, 208, 120);\n"
"    padding: 0 8px;\n"
"    background-color: rgba(64, 72, 53, 0);\n"
"    image: url(:/bg/pixel.png);\n"
"    selection-background-color: rgb(104, 208, 120);\n"
"}")
        self.file_output.setFrame(False)
        self.file_output.setObjectName("file_output")
        self.horizontalLayout.addWidget(self.file_output)
        self.file_output_btn = QtGui.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setFamily("System")
        font.setPointSize(16)
        font.setWeight(9)
        font.setItalic(False)
        font.setBold(False)
        self.file_output_btn.setFont(font)
        self.file_output_btn.setAutoFillBackground(False)
        self.file_output_btn.setStyleSheet("QPushButton{\n"
"    background-color: rgb(83, 91, 74);\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    background-color: rgba(83, 91, 74, 0);\n"
"    image: url(:/bg/pixel.png);\n"
"    border-color: rgb(133, 208, 120);\n"
"    border-radius: 7px;\n"
"    padding: 2px;\n"
"}")
        self.file_output_btn.setFlat(True)
        self.file_output_btn.setObjectName("file_output_btn")
        self.horizontalLayout.addWidget(self.file_output_btn)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.start_date_label = QtGui.QLabel(self.frame)
        self.start_date_label.setStyleSheet("\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/bg/pixel.png);")
        self.start_date_label.setObjectName("start_date_label")
        self.verticalLayout.addWidget(self.start_date_label)
        self.start_date = QtGui.QDateEdit(self.frame)
        self.start_date.setStyleSheet("border: 1px solid rgb(104, 208, 120);\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/bg/pixel.png);")
        self.start_date.setFrame(False)
        self.start_date.setCalendarPopup(True)
        self.start_date.setObjectName("start_date")
        self.verticalLayout.addWidget(self.start_date)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem3 = QtGui.QSpacerItem(100, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.end_date_label = QtGui.QLabel(self.frame)
        self.end_date_label.setStyleSheet("\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/bg/pixel.png);")
        self.end_date_label.setObjectName("end_date_label")
        self.verticalLayout_2.addWidget(self.end_date_label)
        self.end_date = QtGui.QDateEdit(self.frame)
        self.end_date.setStyleSheet("border: 1px solid rgb(104, 208, 120);\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/bg/pixel.png);")
        self.end_date.setFrame(False)
        self.end_date.setCalendarPopup(True)
        self.end_date.setObjectName("end_date")
        self.verticalLayout_2.addWidget(self.end_date)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.cancel_btn = QtGui.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setFamily("System")
        font.setPointSize(16)
        font.setWeight(9)
        font.setItalic(False)
        font.setBold(False)
        self.cancel_btn.setFont(font)
        self.cancel_btn.setAutoFillBackground(False)
        self.cancel_btn.setStyleSheet("QPushButton{\n"
"    background-color: rgba(83, 91, 74, 0);\n"
"    image: url(:/bg/pixel.png);\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-color: rgb(133, 208, 120);\n"
"    border-radius: 7px;\n"
"    padding: 2px;\n"
"}")
        self.cancel_btn.setFlat(True)
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_3.addWidget(self.cancel_btn)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.process_btn = QtGui.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setFamily("System")
        font.setPointSize(16)
        font.setWeight(9)
        font.setItalic(False)
        font.setBold(False)
        self.process_btn.setFont(font)
        self.process_btn.setAutoFillBackground(False)
        self.process_btn.setStyleSheet("QPushButton{\n"
"    background-color: rgba(83, 91, 74, 0);\n"
"    image: url(:/bg/pixel.png);\n"
"    border-style: solid;\n"
"    border-width: 2px;\n"
"    border-color: rgb(133, 208, 120);\n"
"    border-radius: 7px;\n"
"    padding: 2px;\n"
"}")
        self.process_btn.setFlat(True)
        self.process_btn.setObjectName("process_btn")
        self.horizontalLayout_3.addWidget(self.process_btn)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.dashed_line_2 = QtGui.QLabel(self.frame)
        self.dashed_line_2.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";\n"
"background-color: rgba(83, 91, 74, 0);\n"
"image: url(:/bg/pixel.png);")
        self.dashed_line_2.setObjectName("dashed_line_2")
        self.verticalLayout_3.addWidget(self.dashed_line_2)
        self.screen_output = QtGui.QTableWidget(self.frame)
        self.screen_output.setStyleSheet("image: url(:/elements/elements/pixel.png);\n"
"background-color: rgba(0, 0, 0, 0);")
        self.screen_output.setFrameShape(QtGui.QFrame.NoFrame)
        self.screen_output.setShowGrid(False)
        self.screen_output.setGridStyle(QtCore.Qt.NoPen)
        self.screen_output.setObjectName("screen_output")
        self.screen_output.setColumnCount(5)
        self.screen_output.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.screen_output.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.screen_output.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.screen_output.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.screen_output.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.screen_output.setHorizontalHeaderItem(4, item)
        self.screen_output.horizontalHeader().setVisible(False)
        self.screen_output.horizontalHeader().setStretchLastSection(False)
        self.screen_output.verticalHeader().setVisible(False)
        self.verticalLayout_3.addWidget(self.screen_output)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(QuickPayroll)
        QtCore.QMetaObject.connectSlotsByName(QuickPayroll)

    def retranslateUi(self, QuickPayroll):
        QuickPayroll.setWindowTitle(QtGui.QApplication.translate("QuickPayroll", "Time Lord Alpha Payroll Collector", None, QtGui.QApplication.UnicodeUTF8))
        self.main_title.setText(QtGui.QApplication.translate("QuickPayroll", "Time Lord Alpha Payroll Collector", None, QtGui.QApplication.UnicodeUTF8))
        self.dashed_line.setText(QtGui.QApplication.translate("QuickPayroll", "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", None, QtGui.QApplication.UnicodeUTF8))
        self.file_output_label.setText(QtGui.QApplication.translate("QuickPayroll", "File Output (.xls, .xlsx)", None, QtGui.QApplication.UnicodeUTF8))
        self.file_output_btn.setText(QtGui.QApplication.translate("QuickPayroll", "Save As...", None, QtGui.QApplication.UnicodeUTF8))
        self.start_date_label.setText(QtGui.QApplication.translate("QuickPayroll", "Start Date", None, QtGui.QApplication.UnicodeUTF8))
        self.end_date_label.setText(QtGui.QApplication.translate("QuickPayroll", "End Date", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_btn.setText(QtGui.QApplication.translate("QuickPayroll", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.process_btn.setText(QtGui.QApplication.translate("QuickPayroll", "Process and Save", None, QtGui.QApplication.UnicodeUTF8))
        self.dashed_line_2.setText(QtGui.QApplication.translate("QuickPayroll", "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -", None, QtGui.QApplication.UnicodeUTF8))
        self.screen_output.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("QuickPayroll", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.screen_output.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("QuickPayroll", "Level", None, QtGui.QApplication.UnicodeUTF8))
        self.screen_output.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("QuickPayroll", "New Column", None, QtGui.QApplication.UnicodeUTF8))
        self.screen_output.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("QuickPayroll", "Sep", None, QtGui.QApplication.UnicodeUTF8))
        self.screen_output.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("QuickPayroll", "Total", None, QtGui.QApplication.UnicodeUTF8))

from resources import alpha_monitor_resources_rc
