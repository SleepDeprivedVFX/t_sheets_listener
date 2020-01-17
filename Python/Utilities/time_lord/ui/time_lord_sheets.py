# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_sheets.ui'
#
# Created: Thu Jan 16 14:06:22 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_TimeSheets(object):
    def setupUi(self, TimeSheets):
        TimeSheets.setObjectName("TimeSheets")
        TimeSheets.resize(1083, 651)
        TimeSheets.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout_4 = QtGui.QVBoxLayout(TimeSheets)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.title = QtGui.QLabel(TimeSheets)
        self.title.setToolTip("")
        self.title.setStyleSheet("font: 24pt \"SeriaSansPro\";")
        self.title.setObjectName("title")
        self.verticalLayout_4.addWidget(self.title)
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
        self.whose_timesheets = QtGui.QComboBox(self.time_sheets_tab)
        self.whose_timesheets.setObjectName("whose_timesheets")
        self.whose_timesheets.addItem("")
        self.horizontalLayout.addWidget(self.whose_timesheets)
        self.sort_by = QtGui.QGroupBox(self.time_sheets_tab)
        self.sort_by.setFlat(True)
        self.sort_by.setObjectName("sort_by")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.sort_by)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.person_rdo = QtGui.QRadioButton(self.sort_by)
        self.person_rdo.setChecked(True)
        self.person_rdo.setObjectName("person_rdo")
        self.horizontalLayout_2.addWidget(self.person_rdo)
        self.date_rdo = QtGui.QRadioButton(self.sort_by)
        self.date_rdo.setChecked(False)
        self.date_rdo.setObjectName("date_rdo")
        self.horizontalLayout_2.addWidget(self.date_rdo)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.order = QtGui.QComboBox(self.sort_by)
        self.order.setObjectName("order")
        self.order.addItem("")
        self.order.addItem("")
        self.horizontalLayout_3.addWidget(self.order)
        self.horizontalLayout.addWidget(self.sort_by)
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
        self.sheet_tree.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"alternate-background-color: rgb(120, 120, 120);")
        self.sheet_tree.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.sheet_tree.setColumnCount(8)
        self.sheet_tree.setObjectName("sheet_tree")
        self.sheet_tree.headerItem().setText(1, "Project")
        self.sheet_tree.headerItem().setText(2, "Entity")
        self.sheet_tree.headerItem().setText(3, "Task")
        self.sheet_tree.headerItem().setText(4, "Start")
        self.sheet_tree.headerItem().setText(5, "End")
        self.sheet_tree.headerItem().setText(6, "Duration")
        self.sheet_tree.headerItem().setText(7, "Edit")
        self.sheet_tree.header().setVisible(False)
        self.sheet_tree.header().setCascadingSectionResizes(True)
        self.sheet_tree.header().setDefaultSectionSize(120)
        self.sheet_tree.header().setMinimumSectionSize(26)
        self.verticalLayout.addWidget(self.sheet_tree)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.editor_status = QtGui.QLabel(self.time_sheets_tab)
        self.editor_status.setObjectName("editor_status")
        self.verticalLayout_2.addWidget(self.editor_status)
        self.editor_progress = QtGui.QProgressBar(self.time_sheets_tab)
        self.editor_progress.setStatusTip("")
        self.editor_progress.setStyleSheet("QProgressBar {\n"
"    text-align: center;\n"
"    color: rgb(90, 90, 90);\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(224, 149, 0);\n"
"    width: 20px;\n"
"    margin: 1px;\n"
"}")
        self.editor_progress.setProperty("value", 24)
        self.editor_progress.setInvertedAppearance(False)
        self.editor_progress.setObjectName("editor_progress")
        self.verticalLayout_2.addWidget(self.editor_progress)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.excel_rdo = QtGui.QRadioButton(self.time_sheets_tab)
        self.excel_rdo.setChecked(True)
        self.excel_rdo.setObjectName("excel_rdo")
        self.horizontalLayout_5.addWidget(self.excel_rdo)
        self.csv_rdo = QtGui.QRadioButton(self.time_sheets_tab)
        self.csv_rdo.setObjectName("csv_rdo")
        self.horizontalLayout_5.addWidget(self.csv_rdo)
        self.txt_rdo = QtGui.QRadioButton(self.time_sheets_tab)
        self.txt_rdo.setObjectName("txt_rdo")
        self.horizontalLayout_5.addWidget(self.txt_rdo)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_5)
        self.export_btn = QtGui.QPushButton(self.time_sheets_tab)
        self.export_btn.setObjectName("export_btn")
        self.horizontalLayout_4.addWidget(self.export_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
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
        self.verticalLayout_4.addWidget(self.tabs)

        self.retranslateUi(TimeSheets)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(TimeSheets)

    def retranslateUi(self, TimeSheets):
        TimeSheets.setWindowTitle(QtGui.QApplication.translate("TimeSheets", "Time Sheets", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("TimeSheets", "Time Lord Sheets", None, QtGui.QApplication.UnicodeUTF8))
        self.artist_name.setText(QtGui.QApplication.translate("TimeSheets", "Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.whose_timesheets.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#000000;\">List of available people and time sheets</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.whose_timesheets.setItemText(0, QtGui.QApplication.translate("TimeSheets", "My Timesheets", None, QtGui.QApplication.UnicodeUTF8))
        self.sort_by.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#0a0a0a;\">Sorting Options</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.sort_by.setTitle(QtGui.QApplication.translate("TimeSheets", "Sort By", None, QtGui.QApplication.UnicodeUTF8))
        self.person_rdo.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#0b0b0b;\">Sort By Person/Date</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.person_rdo.setText(QtGui.QApplication.translate("TimeSheets", "Person", None, QtGui.QApplication.UnicodeUTF8))
        self.date_rdo.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#0b0b0b;\">Sort By Date/Person</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.date_rdo.setText(QtGui.QApplication.translate("TimeSheets", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.order.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#0a0a0a;\">Dates in Ascending or Descending Order</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.order.setItemText(0, QtGui.QApplication.translate("TimeSheets", "Ascending", None, QtGui.QApplication.UnicodeUTF8))
        self.order.setItemText(1, QtGui.QApplication.translate("TimeSheets", "Decending", None, QtGui.QApplication.UnicodeUTF8))
        self.start_date_label.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#0a0a0a;\">Start Search Date</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.start_date_label.setText(QtGui.QApplication.translate("TimeSheets", "Start Date", None, QtGui.QApplication.UnicodeUTF8))
        self.start_date.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#0a0a0a;\">Start Search Date</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.end_date_label.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#0a0a0a;\">End Search Date</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.end_date_label.setText(QtGui.QApplication.translate("TimeSheets", "End Date", None, QtGui.QApplication.UnicodeUTF8))
        self.end_date.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#0a0a0a;\">End Search Date</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.update_btn.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#0b0b0b;\">Update the Sheets</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.update_btn.setText(QtGui.QApplication.translate("TimeSheets", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.sheet_tree.headerItem().setText(0, QtGui.QApplication.translate("TimeSheets", "Timesheet", None, QtGui.QApplication.UnicodeUTF8))
        self.editor_status.setText(QtGui.QApplication.translate("TimeSheets", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.excel_rdo.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#0a0a0a;\">Export EXCEL sheet</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.excel_rdo.setText(QtGui.QApplication.translate("TimeSheets", "Excel", None, QtGui.QApplication.UnicodeUTF8))
        self.csv_rdo.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#0a0a0a;\">Export CSV Sheet</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.csv_rdo.setText(QtGui.QApplication.translate("TimeSheets", "CSV", None, QtGui.QApplication.UnicodeUTF8))
        self.txt_rdo.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#0a0a0a;\">Export TXT File</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.txt_rdo.setText(QtGui.QApplication.translate("TimeSheets", "TXT", None, QtGui.QApplication.UnicodeUTF8))
        self.export_btn.setToolTip(QtGui.QApplication.translate("TimeSheets", "<html><head/><body><p><span style=\" color:#0a0a0a;\">Run the export</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.export_btn.setText(QtGui.QApplication.translate("TimeSheets", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.time_sheets_tab), QtGui.QApplication.translate("TimeSheets", "Time Sheets", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("TimeSheets", "Coming Eventually!", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.manual_time), QtGui.QApplication.translate("TimeSheets", "Manual Time Card", None, QtGui.QApplication.UnicodeUTF8))

