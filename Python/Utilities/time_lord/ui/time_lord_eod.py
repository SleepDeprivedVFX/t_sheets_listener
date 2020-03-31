# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'time_lord_eod.ui'
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


class Ui_endofday(object):
    def setupUi(self, endofday):
        if endofday.objectName():
            endofday.setObjectName(u"endofday")
        endofday.resize(286, 191)
        endofday.setMinimumSize(QSize(286, 191))
        endofday.setStyleSheet(u"background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout = QVBoxLayout(endofday)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.title = QLabel(endofday)
        self.title.setObjectName(u"title")
        self.title.setStyleSheet(u"font: 22pt \"Chiller\";")
        self.title.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.title)

        self.question = QLabel(endofday)
        self.question.setObjectName(u"question")
        self.question.setStyleSheet(u"font: 10pt \"MS Shell Dlg 2\";")
        self.question.setWordWrap(True)

        self.verticalLayout.addWidget(self.question)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.last_time_label = QLabel(endofday)
        self.last_time_label.setObjectName(u"last_time_label")

        self.horizontalLayout_2.addWidget(self.last_time_label)

        self.last_time = QTimeEdit(endofday)
        self.last_time.setObjectName(u"last_time")

        self.horizontalLayout_2.addWidget(self.last_time)

        self.last_date = QDateEdit(endofday)
        self.last_date.setObjectName(u"last_date")
        self.last_date.setCalendarPopup(True)

        self.horizontalLayout_2.addWidget(self.last_date)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.yes_btn = QPushButton(endofday)
        self.yes_btn.setObjectName(u"yes_btn")

        self.horizontalLayout.addWidget(self.yes_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.no_btn = QPushButton(endofday)
        self.no_btn.setObjectName(u"no_btn")

        self.horizontalLayout.addWidget(self.no_btn)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(endofday)

        QMetaObject.connectSlotsByName(endofday)
    # setupUi

    def retranslateUi(self, endofday):
        endofday.setWindowTitle(QCoreApplication.translate("endofday", u"End of Day", None))
        self.title.setText(QCoreApplication.translate("endofday", u"It's Over!", None))
        self.question.setText(QCoreApplication.translate("endofday", u"The day is done, and it looks like you haven't touched the computer in a while.  Are you still working?", None))
        self.last_time_label.setText(QCoreApplication.translate("endofday", u"Last Detected Time:", None))
        self.yes_btn.setText(QCoreApplication.translate("endofday", u"Yes I am!", None))
        self.no_btn.setText(QCoreApplication.translate("endofday", u"No!  I'm done.", None))
    # retranslateUi

