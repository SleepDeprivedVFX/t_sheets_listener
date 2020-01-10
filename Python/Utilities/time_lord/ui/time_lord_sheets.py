# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_sheets.ui'
#
# Created: Thu Jan 09 19:07:36 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_TimeSheets(object):
    def setupUi(self, TimeSheets):
        TimeSheets.setObjectName("TimeSheets")
        TimeSheets.resize(1148, 665)
        TimeSheets.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout_2 = QtGui.QVBoxLayout(TimeSheets)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title = QtGui.QLabel(TimeSheets)
        self.title.setStyleSheet("font: 24pt \"SeriaSansPro\";")
        self.title.setObjectName("title")
        self.verticalLayout_2.addWidget(self.title)
        self.tabs = QtGui.QTabWidget(TimeSheets)
        self.tabs.setStyleSheet("QTabWidget::pane { /* The tab widget frame */\n"
"    border-top: 2px solid rgb(65, 65, 65);\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    left: 5px; /* move to the right by 5px */\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 rgb(65, 65, 65), stop: 0.4 rgb(70, 70, 70),\n"
"                                stop: 0.5 rgb(75, 75, 75), stop: 1.0 rgb(80, 80, 80));\n"
"    border: 2px solid  rgb(65, 65, 65);\n"
"    color: rgb(100, 100, 100);\n"
"    border-bottom-color: rgb(65, 65, 65);\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 8ex;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                stop: 0 rgb(80, 80, 80), stop: 0.4 rgb(85, 85, 85),\n"
"                                stop: 0.5 rgb(90, 90, 90), stop: 1.0 rgb(100, 100, 100));\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    border-color:rgb(80, 80, 80);\n"
"    \n"
"    color: rgb(210, 210, 210);\n"
"    border-bottom-color: rgb(80, 80, 80); /* same as pane color */\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 2px; /* make non-selected tabs look smaller */\n"
"}\n"
"")
        self.tabs.setObjectName("tabs")
        self.time_sheets_tab = QtGui.QWidget()
        self.time_sheets_tab.setObjectName("time_sheets_tab")
        self.verticalLayout = QtGui.QVBoxLayout(self.time_sheets_tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.artist_name = QtGui.QLabel(self.time_sheets_tab)
        self.artist_name.setStyleSheet("font: 18pt \"SeriaSansPro\";")
        self.artist_name.setObjectName("artist_name")
        self.horizontalLayout.addWidget(self.artist_name)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.start_date_label = QtGui.QLabel(self.time_sheets_tab)
        self.start_date_label.setObjectName("start_date_label")
        self.horizontalLayout.addWidget(self.start_date_label)
        self.start_date = QtGui.QDateEdit(self.time_sheets_tab)
        self.start_date.setCalendarPopup(True)
        self.start_date.setObjectName("start_date")
        self.horizontalLayout.addWidget(self.start_date)
        self.end_date_label = QtGui.QLabel(self.time_sheets_tab)
        self.end_date_label.setObjectName("end_date_label")
        self.horizontalLayout.addWidget(self.end_date_label)
        self.end_date = QtGui.QDateEdit(self.time_sheets_tab)
        self.end_date.setCalendarPopup(True)
        self.end_date.setObjectName("end_date")
        self.horizontalLayout.addWidget(self.end_date)
        self.update_btn = QtGui.QPushButton(self.time_sheets_tab)
        self.update_btn.setObjectName("update_btn")
        self.horizontalLayout.addWidget(self.update_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.sheet_tree = QtGui.QTreeWidget(self.time_sheets_tab)
        self.sheet_tree.setObjectName("sheet_tree")
        self.sheet_tree.header().setVisible(False)
        self.verticalLayout.addWidget(self.sheet_tree)
        self.tabs.addTab(self.time_sheets_tab, "")
        self.manual_time = QtGui.QWidget()
        self.manual_time.setObjectName("manual_time")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.manual_time)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtGui.QLabel(self.manual_time)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.tabs.addTab(self.manual_time, "")
        self.verticalLayout_2.addWidget(self.tabs)

        self.retranslateUi(TimeSheets)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TimeSheets)

    def retranslateUi(self, TimeSheets):
        TimeSheets.setWindowTitle(QtGui.QApplication.translate("TimeSheets", "Time Sheets", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("TimeSheets", "Time Lord Sheets", None, QtGui.QApplication.UnicodeUTF8))
        self.artist_name.setText(QtGui.QApplication.translate("TimeSheets", "Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.start_date_label.setText(QtGui.QApplication.translate("TimeSheets", "Start Date", None, QtGui.QApplication.UnicodeUTF8))
        self.end_date_label.setText(QtGui.QApplication.translate("TimeSheets", "End Date", None, QtGui.QApplication.UnicodeUTF8))
        self.update_btn.setText(QtGui.QApplication.translate("TimeSheets", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.sheet_tree.headerItem().setText(0, QtGui.QApplication.translate("TimeSheets", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.time_sheets_tab), QtGui.QApplication.translate("TimeSheets", "Time Sheets", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("TimeSheets", "Coming Eventually!", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.manual_time), QtGui.QApplication.translate("TimeSheets", "Manual Time Card", None, QtGui.QApplication.UnicodeUTF8))

