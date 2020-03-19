# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'time_lord_lunch.ui'
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


class Ui_lunch_form(object):
    def setupUi(self, lunch_form):
        if lunch_form.objectName():
            lunch_form.setObjectName(u"lunch_form")
        lunch_form.resize(557, 170)
        lunch_form.setStyleSheet(u"background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout = QVBoxLayout(lunch_form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lunch_title = QLabel(lunch_form)
        self.lunch_title.setObjectName(u"lunch_title")
        self.lunch_title.setStyleSheet(u"font: 24pt \"Algerian\";\n"
"border-color: rgb(24, 84, 148);\n"
"border-width: 4px;")

        self.horizontalLayout_3.addWidget(self.lunch_title)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.lunch_message = QLabel(lunch_form)
        self.lunch_message.setObjectName(u"lunch_message")
        self.lunch_message.setStyleSheet(u"padding: 5px;")
        self.lunch_message.setAlignment(Qt.AlignCenter)
        self.lunch_message.setWordWrap(True)

        self.verticalLayout.addWidget(self.lunch_message)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.from_label = QLabel(lunch_form)
        self.from_label.setObjectName(u"from_label")
        self.from_label.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.from_label)

        self.start_time = QTimeEdit(lunch_form)
        self.start_time.setObjectName(u"start_time")
        self.start_time.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.start_time)

        self.to_label = QLabel(lunch_form)
        self.to_label.setObjectName(u"to_label")
        self.to_label.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.to_label)

        self.end_time = QTimeEdit(lunch_form)
        self.end_time.setObjectName(u"end_time")
        self.end_time.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.end_time)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.skip_btn = QPushButton(lunch_form)
        self.skip_btn.setObjectName(u"skip_btn")
        self.skip_btn.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.skip_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.ok_btn = QPushButton(lunch_form)
        self.ok_btn.setObjectName(u"ok_btn")
        self.ok_btn.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.ok_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(lunch_form)

        QMetaObject.connectSlotsByName(lunch_form)
    # setupUi

    def retranslateUi(self, lunch_form):
        lunch_form.setWindowTitle(QCoreApplication.translate("lunch_form", u"The Lunch Line", None))
        self.lunch_title.setText(QCoreApplication.translate("lunch_form", u"LUNCH!", None))
        self.lunch_message.setText(QCoreApplication.translate("lunch_form", u"Hey %s, The system detected you were gone to lunch between the following times.  Is this correct?", None))
        self.from_label.setText(QCoreApplication.translate("lunch_form", u"From", None))
        self.to_label.setText(QCoreApplication.translate("lunch_form", u"To", None))
        self.skip_btn.setText(QCoreApplication.translate("lunch_form", u"No", None))
        self.ok_btn.setText(QCoreApplication.translate("lunch_form", u"Yes! I Took My Lunch", None))
    # retranslateUi

