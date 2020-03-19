# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'time_lord_sheets.ui'
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


class Ui_TimeSheets(object):
    def setupUi(self, TimeSheets):
        if TimeSheets.objectName():
            TimeSheets.setObjectName(u"TimeSheets")
        TimeSheets.resize(1014, 571)
        TimeSheets.setStyleSheet(u"background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout_5 = QVBoxLayout(TimeSheets)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.title = QLabel(TimeSheets)
        self.title.setObjectName(u"title")
        self.title.setStyleSheet(u"font: 24pt \"SeriaSansPro\";")

        self.horizontalLayout_8.addWidget(self.title)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.todays_total_label = QLabel(TimeSheets)
        self.todays_total_label.setObjectName(u"todays_total_label")

        self.horizontalLayout_6.addWidget(self.todays_total_label)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

        self.todays_total = QLabel(TimeSheets)
        self.todays_total.setObjectName(u"todays_total")
        self.todays_total.setStyleSheet(u"font: 75 8pt \"MS Shell Dlg 2\";")

        self.horizontalLayout_6.addWidget(self.todays_total)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.weeks_total_label = QLabel(TimeSheets)
        self.weeks_total_label.setObjectName(u"weeks_total_label")

        self.horizontalLayout_7.addWidget(self.weeks_total_label)

        self.horizontalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)

        self.weeks_total = QLabel(TimeSheets)
        self.weeks_total.setObjectName(u"weeks_total")

        self.horizontalLayout_7.addWidget(self.weeks_total)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_8.addLayout(self.verticalLayout_4)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_17)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.tabs = QTabWidget(TimeSheets)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setStyleSheet(u"QTabWidget::pane { /* The tab widget frame */\n"
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
"	color: rgb(100, 100, 100);\n"
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
"	color: rgb(255, 255"
                        ", 255);\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    border-color:rgb(80, 80, 80);\n"
"	\n"
"	color: rgb(210, 210, 210);\n"
"    border-bottom-color: rgb(80, 80, 80); /* same as pane color */\n"
"}\n"
"\n"
"QTabBar::tab:!selected {\n"
"    margin-top: 2px; /* make non-selected tabs look smaller */\n"
"}\n"
"")
        self.time_sheets_tab = QWidget()
        self.time_sheets_tab.setObjectName(u"time_sheets_tab")
        self.verticalLayout = QVBoxLayout(self.time_sheets_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.artist_name = QLabel(self.time_sheets_tab)
        self.artist_name.setObjectName(u"artist_name")
        self.artist_name.setStyleSheet(u"font: 18pt \"SeriaSansPro\";")

        self.horizontalLayout.addWidget(self.artist_name)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.whose_timesheets = QComboBox(self.time_sheets_tab)
        self.whose_timesheets.addItem("")
        self.whose_timesheets.setObjectName(u"whose_timesheets")

        self.horizontalLayout.addWidget(self.whose_timesheets)

        self.sort_by = QGroupBox(self.time_sheets_tab)
        self.sort_by.setObjectName(u"sort_by")
        self.sort_by.setFlat(True)
        self.horizontalLayout_3 = QHBoxLayout(self.sort_by)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.person_rdo = QRadioButton(self.sort_by)
        self.person_rdo.setObjectName(u"person_rdo")
        self.person_rdo.setChecked(True)

        self.horizontalLayout_2.addWidget(self.person_rdo)

        self.date_rdo = QRadioButton(self.sort_by)
        self.date_rdo.setObjectName(u"date_rdo")
        self.date_rdo.setChecked(False)

        self.horizontalLayout_2.addWidget(self.date_rdo)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)

        self.order = QComboBox(self.sort_by)
        self.order.addItem("")
        self.order.addItem("")
        self.order.setObjectName(u"order")

        self.horizontalLayout_3.addWidget(self.order)


        self.horizontalLayout.addWidget(self.sort_by)

        self.start_date_label = QLabel(self.time_sheets_tab)
        self.start_date_label.setObjectName(u"start_date_label")

        self.horizontalLayout.addWidget(self.start_date_label)

        self.start_date = QDateEdit(self.time_sheets_tab)
        self.start_date.setObjectName(u"start_date")
        self.start_date.setCalendarPopup(True)

        self.horizontalLayout.addWidget(self.start_date)

        self.end_date_label = QLabel(self.time_sheets_tab)
        self.end_date_label.setObjectName(u"end_date_label")

        self.horizontalLayout.addWidget(self.end_date_label)

        self.end_date = QDateEdit(self.time_sheets_tab)
        self.end_date.setObjectName(u"end_date")
        self.end_date.setCalendarPopup(True)

        self.horizontalLayout.addWidget(self.end_date)

        self.update_btn = QPushButton(self.time_sheets_tab)
        self.update_btn.setObjectName(u"update_btn")

        self.horizontalLayout.addWidget(self.update_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.sheet_tree = QTreeWidget(self.time_sheets_tab)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(7, u"Edit");
        __qtreewidgetitem.setText(6, u"Duration");
        __qtreewidgetitem.setText(5, u"End");
        __qtreewidgetitem.setText(4, u"Start");
        __qtreewidgetitem.setText(3, u"Task");
        __qtreewidgetitem.setText(2, u"Entity");
        __qtreewidgetitem.setText(1, u"Project");
        self.sheet_tree.setHeaderItem(__qtreewidgetitem)
        self.sheet_tree.setObjectName(u"sheet_tree")
        self.sheet_tree.setStyleSheet(u"background-color: rgb(100, 100, 100);\n"
"alternate-background-color: rgb(120, 120, 120);")
        self.sheet_tree.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.sheet_tree.setColumnCount(8)
        self.sheet_tree.header().setVisible(False)
        self.sheet_tree.header().setCascadingSectionResizes(True)
        self.sheet_tree.header().setMinimumSectionSize(26)
        self.sheet_tree.header().setDefaultSectionSize(120)

        self.verticalLayout.addWidget(self.sheet_tree)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.editor_status = QLabel(self.time_sheets_tab)
        self.editor_status.setObjectName(u"editor_status")

        self.verticalLayout_2.addWidget(self.editor_status)

        self.editor_progress = QProgressBar(self.time_sheets_tab)
        self.editor_progress.setObjectName(u"editor_progress")
        self.editor_progress.setStyleSheet(u"QProgressBar {\n"
"    text-align: center;\n"
"	color: rgb(90, 90, 90);\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: rgb(224, 149, 0);\n"
"    width: 20px;\n"
"	margin: 1px;\n"
"}")
        self.editor_progress.setValue(24)
        self.editor_progress.setInvertedAppearance(False)

        self.verticalLayout_2.addWidget(self.editor_progress)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.excel_rdo = QRadioButton(self.time_sheets_tab)
        self.excel_rdo.setObjectName(u"excel_rdo")
        self.excel_rdo.setChecked(True)

        self.horizontalLayout_5.addWidget(self.excel_rdo)

        self.csv_rdo = QRadioButton(self.time_sheets_tab)
        self.csv_rdo.setObjectName(u"csv_rdo")

        self.horizontalLayout_5.addWidget(self.csv_rdo)

        self.txt_rdo = QRadioButton(self.time_sheets_tab)
        self.txt_rdo.setObjectName(u"txt_rdo")

        self.horizontalLayout_5.addWidget(self.txt_rdo)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_5)

        self.export_btn = QPushButton(self.time_sheets_tab)
        self.export_btn.setObjectName(u"export_btn")

        self.horizontalLayout_4.addWidget(self.export_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.tabs.addTab(self.time_sheets_tab, "")
        self.manual_time = QWidget()
        self.manual_time.setObjectName(u"manual_time")
        self.verticalLayout_3 = QVBoxLayout(self.manual_time)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.new_artist_label = QLabel(self.manual_time)
        self.new_artist_label.setObjectName(u"new_artist_label")
        self.new_artist_label.setStyleSheet(u"font: 16pt \"MS Shell Dlg 2\";")

        self.verticalLayout_3.addWidget(self.new_artist_label)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.new_project_label = QLabel(self.manual_time)
        self.new_project_label.setObjectName(u"new_project_label")

        self.horizontalLayout_9.addWidget(self.new_project_label)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_7)

        self.new_project = QComboBox(self.manual_time)
        self.new_project.setObjectName(u"new_project")
        self.new_project.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_9.addWidget(self.new_project)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_16)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.new_entity_label = QLabel(self.manual_time)
        self.new_entity_label.setObjectName(u"new_entity_label")

        self.horizontalLayout_10.addWidget(self.new_entity_label)

        self.horizontalSpacer_8 = QSpacerItem(45, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_8)

        self.new_entity = QComboBox(self.manual_time)
        self.new_entity.setObjectName(u"new_entity")
        self.new_entity.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_10.addWidget(self.new_entity)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_15)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.new_task_label = QLabel(self.manual_time)
        self.new_task_label.setObjectName(u"new_task_label")

        self.horizontalLayout_11.addWidget(self.new_task_label)

        self.horizontalSpacer_9 = QSpacerItem(51, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_9)

        self.new_task = QComboBox(self.manual_time)
        self.new_task.setObjectName(u"new_task")
        self.new_task.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_11.addWidget(self.new_task)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_14)


        self.verticalLayout_3.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.new_start_time_label = QLabel(self.manual_time)
        self.new_start_time_label.setObjectName(u"new_start_time_label")

        self.horizontalLayout_12.addWidget(self.new_start_time_label)

        self.horizontalSpacer_12 = QSpacerItem(46, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_12)

        self.new_start_date = QDateEdit(self.manual_time)
        self.new_start_date.setObjectName(u"new_start_date")
        self.new_start_date.setCalendarPopup(True)

        self.horizontalLayout_12.addWidget(self.new_start_date)

        self.new_start_time = QTimeEdit(self.manual_time)
        self.new_start_time.setObjectName(u"new_start_time")

        self.horizontalLayout_12.addWidget(self.new_start_time)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_10)


        self.verticalLayout_3.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.new_end_label = QLabel(self.manual_time)
        self.new_end_label.setObjectName(u"new_end_label")

        self.horizontalLayout_13.addWidget(self.new_end_label)

        self.horizontalSpacer_13 = QSpacerItem(52, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_13)

        self.new_end_date = QDateEdit(self.manual_time)
        self.new_end_date.setObjectName(u"new_end_date")
        self.new_end_date.setCalendarPopup(True)

        self.horizontalLayout_13.addWidget(self.new_end_date)

        self.new_end_time = QTimeEdit(self.manual_time)
        self.new_end_time.setObjectName(u"new_end_time")

        self.horizontalLayout_13.addWidget(self.new_end_time)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_11)


        self.verticalLayout_3.addLayout(self.horizontalLayout_13)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_6)

        self.add_time_btn = QPushButton(self.manual_time)
        self.add_time_btn.setObjectName(u"add_time_btn")

        self.horizontalLayout_14.addWidget(self.add_time_btn)

        self.cancel_btn = QPushButton(self.manual_time)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.horizontalLayout_14.addWidget(self.cancel_btn)


        self.verticalLayout_3.addLayout(self.horizontalLayout_14)

        self.tabs.addTab(self.manual_time, "")

        self.verticalLayout_5.addWidget(self.tabs)


        self.retranslateUi(TimeSheets)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(TimeSheets)
    # setupUi

    def retranslateUi(self, TimeSheets):
        TimeSheets.setWindowTitle(QCoreApplication.translate("TimeSheets", u"Time Sheets", None))
#if QT_CONFIG(tooltip)
        self.title.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.title.setText(QCoreApplication.translate("TimeSheets", u"Time Lord Sheets", None))
        self.todays_total_label.setText(QCoreApplication.translate("TimeSheets", u"Today's Hours:", None))
        self.todays_total.setText(QCoreApplication.translate("TimeSheets", u"%0.2f", None))
        self.weeks_total_label.setText(QCoreApplication.translate("TimeSheets", u"Week's Hours: ", None))
        self.weeks_total.setText(QCoreApplication.translate("TimeSheets", u"%0.2f", None))
        self.artist_name.setText(QCoreApplication.translate("TimeSheets", u"Artist", None))
        self.whose_timesheets.setItemText(0, QCoreApplication.translate("TimeSheets", u"My Timesheets", None))

#if QT_CONFIG(tooltip)
        self.whose_timesheets.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#000000;\">List of available people and time sheets</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.sort_by.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#0a0a0a;\">Sorting Options</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.sort_by.setTitle(QCoreApplication.translate("TimeSheets", u"Sort By", None))
#if QT_CONFIG(tooltip)
        self.person_rdo.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#0b0b0b;\">Sort By Person/Date</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.person_rdo.setText(QCoreApplication.translate("TimeSheets", u"Person", None))
#if QT_CONFIG(tooltip)
        self.date_rdo.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#0b0b0b;\">Sort By Date/Person</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.date_rdo.setText(QCoreApplication.translate("TimeSheets", u"Date", None))
        self.order.setItemText(0, QCoreApplication.translate("TimeSheets", u"Ascending", None))
        self.order.setItemText(1, QCoreApplication.translate("TimeSheets", u"Decending", None))

#if QT_CONFIG(tooltip)
        self.order.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#0a0a0a;\">Dates in Ascending or Descending Order</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.start_date_label.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#0a0a0a;\">Start Search Date</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.start_date_label.setText(QCoreApplication.translate("TimeSheets", u"Start Date", None))
#if QT_CONFIG(tooltip)
        self.start_date.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#0a0a0a;\">Start Search Date</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.end_date_label.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#0a0a0a;\">End Search Date</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.end_date_label.setText(QCoreApplication.translate("TimeSheets", u"End Date", None))
#if QT_CONFIG(tooltip)
        self.end_date.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#0a0a0a;\">End Search Date</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.update_btn.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#0b0b0b;\">Update the Sheets</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.update_btn.setText(QCoreApplication.translate("TimeSheets", u"Update", None))
        ___qtreewidgetitem = self.sheet_tree.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("TimeSheets", u"Timesheet", None));
        self.editor_status.setText(QCoreApplication.translate("TimeSheets", u"TextLabel", None))
#if QT_CONFIG(statustip)
        self.editor_progress.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(tooltip)
        self.excel_rdo.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#0a0a0a;\">Export EXCEL sheet</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.excel_rdo.setText(QCoreApplication.translate("TimeSheets", u"Excel", None))
#if QT_CONFIG(tooltip)
        self.csv_rdo.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#0a0a0a;\">Export CSV Sheet</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.csv_rdo.setText(QCoreApplication.translate("TimeSheets", u"CSV", None))
#if QT_CONFIG(tooltip)
        self.txt_rdo.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#0a0a0a;\">Export TXT File</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.txt_rdo.setText(QCoreApplication.translate("TimeSheets", u"TXT", None))
#if QT_CONFIG(tooltip)
        self.export_btn.setToolTip(QCoreApplication.translate("TimeSheets", u"<html><head/><body><p><span style=\" color:#0a0a0a;\">Run the export</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.export_btn.setText(QCoreApplication.translate("TimeSheets", u"Export", None))
        self.tabs.setTabText(self.tabs.indexOf(self.time_sheets_tab), QCoreApplication.translate("TimeSheets", u"Time Sheets", None))
        self.new_artist_label.setText(QCoreApplication.translate("TimeSheets", u"Artist", None))
        self.new_project_label.setText(QCoreApplication.translate("TimeSheets", u"Project", None))
        self.new_entity_label.setText(QCoreApplication.translate("TimeSheets", u"Entity", None))
        self.new_task_label.setText(QCoreApplication.translate("TimeSheets", u"Task", None))
        self.new_start_time_label.setText(QCoreApplication.translate("TimeSheets", u"Start", None))
        self.new_end_label.setText(QCoreApplication.translate("TimeSheets", u"End", None))
        self.add_time_btn.setText(QCoreApplication.translate("TimeSheets", u"Add", None))
        self.cancel_btn.setText(QCoreApplication.translate("TimeSheets", u"Cancel", None))
        self.tabs.setTabText(self.tabs.indexOf(self.manual_time), QCoreApplication.translate("TimeSheets", u"Manual Time Card", None))
    # retranslateUi

