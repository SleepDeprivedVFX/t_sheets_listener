# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'time_lord_scope.ui'
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


class Ui_WhosWorking(object):
    def setupUi(self, WhosWorking):
        if WhosWorking.objectName():
            WhosWorking.setObjectName(u"WhosWorking")
        WhosWorking.resize(820, 520)
        WhosWorking.setMinimumSize(QSize(820, 481))
        WhosWorking.setStyleSheet(u"background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout = QVBoxLayout(WhosWorking)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Title = QLabel(WhosWorking)
        self.Title.setObjectName(u"Title")
        self.Title.setStyleSheet(u"font: 75 16pt \"MS Shell Dlg 2\";")

        self.verticalLayout.addWidget(self.Title)

        self.question = QLabel(WhosWorking)
        self.question.setObjectName(u"question")
        self.question.setStyleSheet(u"font: 12pt \"MS Shell Dlg 2\";")

        self.verticalLayout.addWidget(self.question)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.stay_on_top = QCheckBox(WhosWorking)
        self.stay_on_top.setObjectName(u"stay_on_top")

        self.horizontalLayout.addWidget(self.stay_on_top)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.slave_list = QTableWidget(WhosWorking)
        if (self.slave_list.columnCount() < 8):
            self.slave_list.setColumnCount(8)
        __qtablewidgetitem = QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        self.slave_list.setObjectName(u"slave_list")
        self.slave_list.setStyleSheet(u"QHeaderView::section{\n"
"	\n"
"	background-color: rgb(97, 97, 97);\n"
"}\n"
"QTableView::item{\n"
"	border: 0px;\n"
"	padding: 5px;\n"
"}")
        self.slave_list.setAlternatingRowColors(False)
        self.slave_list.setSortingEnabled(True)
        self.slave_list.horizontalHeader().setVisible(True)
        self.slave_list.horizontalHeader().setCascadingSectionResizes(True)
        self.slave_list.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.slave_list)


        self.retranslateUi(WhosWorking)

        QMetaObject.connectSlotsByName(WhosWorking)
    # setupUi

    def retranslateUi(self, WhosWorking):
        WhosWorking.setWindowTitle(QCoreApplication.translate("WhosWorking", u"Time Lord Scope", None))
        self.Title.setText(QCoreApplication.translate("WhosWorking", u"Time Scope", None))
        self.question.setText(QCoreApplication.translate("WhosWorking", u"Who's working on what?", None))
        self.stay_on_top.setText(QCoreApplication.translate("WhosWorking", u"Keep On Top", None))
        ___qtablewidgetitem = self.slave_list.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("WhosWorking", u"Artist", None));
        ___qtablewidgetitem1 = self.slave_list.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("WhosWorking", u"Project", None));
        ___qtablewidgetitem2 = self.slave_list.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("WhosWorking", u"Entity", None));
        ___qtablewidgetitem3 = self.slave_list.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("WhosWorking", u"Task", None));
        ___qtablewidgetitem4 = self.slave_list.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("WhosWorking", u"Time", None));
        ___qtablewidgetitem5 = self.slave_list.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("WhosWorking", u"Total", None));
        ___qtablewidgetitem6 = self.slave_list.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("WhosWorking", u"Lunch", None));
        ___qtablewidgetitem7 = self.slave_list.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("WhosWorking", u"Edit", None));
    # retranslateUi

