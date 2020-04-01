# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'time_lord_reports.ui'
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


class Ui_Time_Lord_Reports(object):
    def setupUi(self, Time_Lord_Reports):
        if Time_Lord_Reports.objectName():
            Time_Lord_Reports.setObjectName(u"Time_Lord_Reports")
        Time_Lord_Reports.resize(1109, 662)
        Time_Lord_Reports.setStyleSheet(u"background-color: rgb(100, 100, 100);\n"
"alternate-background-color: rgb(120, 120, 120);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout_8 = QVBoxLayout(Time_Lord_Reports)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.Title = QLabel(Time_Lord_Reports)
        self.Title.setObjectName(u"Title")
        self.Title.setStyleSheet(u"font: 16pt \"MS Shell Dlg 2\";")

        self.verticalLayout_8.addWidget(self.Title)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.start_time_label = QLabel(Time_Lord_Reports)
        self.start_time_label.setObjectName(u"start_time_label")

        self.verticalLayout.addWidget(self.start_time_label)

        self.start_time = QDateEdit(Time_Lord_Reports)
        self.start_time.setObjectName(u"start_time")
        self.start_time.setCalendarPopup(True)

        self.verticalLayout.addWidget(self.start_time)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.end_time_label = QLabel(Time_Lord_Reports)
        self.end_time_label.setObjectName(u"end_time_label")

        self.verticalLayout_2.addWidget(self.end_time_label)

        self.end_time = QDateEdit(Time_Lord_Reports)
        self.end_time.setObjectName(u"end_time")
        self.end_time.setCalendarPopup(True)

        self.verticalLayout_2.addWidget(self.end_time)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.all_time = QCheckBox(Time_Lord_Reports)
        self.all_time.setObjectName(u"all_time")

        self.horizontalLayout_2.addWidget(self.all_time)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_8.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.primary_org_label = QLabel(Time_Lord_Reports)
        self.primary_org_label.setObjectName(u"primary_org_label")

        self.verticalLayout_3.addWidget(self.primary_org_label)

        self.primary_org = QComboBox(Time_Lord_Reports)
        self.primary_org.addItem("")
        self.primary_org.addItem("")
        self.primary_org.addItem("")
        self.primary_org.addItem("")
        self.primary_org.addItem("")
        self.primary_org.addItem("")
        self.primary_org.addItem("")
        self.primary_org.setObjectName(u"primary_org")

        self.verticalLayout_3.addWidget(self.primary_org)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer = QSpacerItem(5, 15, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.secondary_org = QComboBox(Time_Lord_Reports)
        self.secondary_org.addItem("")
        self.secondary_org.setObjectName(u"secondary_org")

        self.verticalLayout_4.addWidget(self.secondary_org)


        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_2 = QSpacerItem(5, 15, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.trinary_org = QComboBox(Time_Lord_Reports)
        self.trinary_org.addItem("")
        self.trinary_org.setObjectName(u"trinary_org")

        self.verticalLayout_5.addWidget(self.trinary_org)


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalSpacer_3 = QSpacerItem(5, 15, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)

        self.quaternary_org = QComboBox(Time_Lord_Reports)
        self.quaternary_org.addItem("")
        self.quaternary_org.setObjectName(u"quaternary_org")

        self.verticalLayout_6.addWidget(self.quaternary_org)


        self.horizontalLayout.addLayout(self.verticalLayout_6)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalSpacer_4 = QSpacerItem(5, 15, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_7.addItem(self.verticalSpacer_4)

        self.quinternary_org = QComboBox(Time_Lord_Reports)
        self.quinternary_org.addItem("")
        self.quinternary_org.setObjectName(u"quinternary_org")

        self.verticalLayout_7.addWidget(self.quinternary_org)


        self.horizontalLayout.addLayout(self.verticalLayout_7)

        self.run_btn = QPushButton(Time_Lord_Reports)
        self.run_btn.setObjectName(u"run_btn")

        self.horizontalLayout.addWidget(self.run_btn)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_8.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.output_path = QLineEdit(Time_Lord_Reports)
        self.output_path.setObjectName(u"output_path")

        self.horizontalLayout_3.addWidget(self.output_path)

        self.browse_btn = QPushButton(Time_Lord_Reports)
        self.browse_btn.setObjectName(u"browse_btn")

        self.horizontalLayout_3.addWidget(self.browse_btn)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.save_report_btn = QPushButton(Time_Lord_Reports)
        self.save_report_btn.setObjectName(u"save_report_btn")

        self.horizontalLayout_3.addWidget(self.save_report_btn)


        self.verticalLayout_8.addLayout(self.horizontalLayout_3)

        self.data_tree = QTreeWidget(Time_Lord_Reports)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(7, u"8");
        __qtreewidgetitem.setText(6, u"7");
        __qtreewidgetitem.setText(5, u"6");
        __qtreewidgetitem.setText(4, u"5");
        __qtreewidgetitem.setText(3, u"4");
        __qtreewidgetitem.setText(2, u"3");
        __qtreewidgetitem.setText(1, u"2");
        __qtreewidgetitem.setText(0, u"1");
        self.data_tree.setHeaderItem(__qtreewidgetitem)
        self.data_tree.setObjectName(u"data_tree")
        self.data_tree.setFrameShape(QFrame.NoFrame)
        self.data_tree.setAlternatingRowColors(True)
        self.data_tree.setSortingEnabled(True)
        self.data_tree.setAnimated(True)
        self.data_tree.setWordWrap(True)
        self.data_tree.setColumnCount(8)
        self.data_tree.header().setVisible(False)
        self.data_tree.header().setCascadingSectionResizes(True)
        self.data_tree.header().setDefaultSectionSize(120)
        self.data_tree.header().setHighlightSections(False)

        self.verticalLayout_8.addWidget(self.data_tree)


        self.retranslateUi(Time_Lord_Reports)

        QMetaObject.connectSlotsByName(Time_Lord_Reports)
    # setupUi

    def retranslateUi(self, Time_Lord_Reports):
        Time_Lord_Reports.setWindowTitle(QCoreApplication.translate("Time_Lord_Reports", u"Time Lord Reports", None))
        self.Title.setText(QCoreApplication.translate("Time_Lord_Reports", u"Time Lord Reports", None))
        self.start_time_label.setText(QCoreApplication.translate("Time_Lord_Reports", u"Start Time", None))
        self.end_time_label.setText(QCoreApplication.translate("Time_Lord_Reports", u"End Time", None))
        self.all_time.setText(QCoreApplication.translate("Time_Lord_Reports", u"All Time", None))
        self.primary_org_label.setText(QCoreApplication.translate("Time_Lord_Reports", u"Primary Organizer", None))
        self.primary_org.setItemText(0, QCoreApplication.translate("Time_Lord_Reports", u"None", None))
        self.primary_org.setItemText(1, QCoreApplication.translate("Time_Lord_Reports", u"Projects", None))
        self.primary_org.setItemText(2, QCoreApplication.translate("Time_Lord_Reports", u"Artists", None))
        self.primary_org.setItemText(3, QCoreApplication.translate("Time_Lord_Reports", u"Tasks", None))
        self.primary_org.setItemText(4, QCoreApplication.translate("Time_Lord_Reports", u"All Entities", None))
        self.primary_org.setItemText(5, QCoreApplication.translate("Time_Lord_Reports", u"Entities (Assets)", None))
        self.primary_org.setItemText(6, QCoreApplication.translate("Time_Lord_Reports", u"Entities (Shots)", None))

        self.secondary_org.setItemText(0, QCoreApplication.translate("Time_Lord_Reports", u"None", None))

        self.trinary_org.setItemText(0, QCoreApplication.translate("Time_Lord_Reports", u"None", None))

        self.quaternary_org.setItemText(0, QCoreApplication.translate("Time_Lord_Reports", u"None", None))

        self.quinternary_org.setItemText(0, QCoreApplication.translate("Time_Lord_Reports", u"None", None))

        self.run_btn.setText(QCoreApplication.translate("Time_Lord_Reports", u"Run", None))
        self.browse_btn.setText(QCoreApplication.translate("Time_Lord_Reports", u"Browse...", None))
        self.save_report_btn.setText(QCoreApplication.translate("Time_Lord_Reports", u"Save Report", None))
    # retranslateUi

