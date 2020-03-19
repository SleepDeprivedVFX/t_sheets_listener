# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'time_lord_edit_timesheet.ui'
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


class Ui_Editor(object):
    def setupUi(self, Editor):
        if Editor.objectName():
            Editor.setObjectName(u"Editor")
        Editor.resize(303, 336)
        Editor.setStyleSheet(u"background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout_2 = QVBoxLayout(Editor)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.title = QLabel(Editor)
        self.title.setObjectName(u"title")
        self.title.setStyleSheet(u"font: 16pt \"MS Shell Dlg 2\";")

        self.verticalLayout_2.addWidget(self.title)

        self.tid = QLabel(Editor)
        self.tid.setObjectName(u"tid")

        self.verticalLayout_2.addWidget(self.tid)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.project = QLabel(Editor)
        self.project.setObjectName(u"project")

        self.horizontalLayout_4.addWidget(self.project)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)

        self.project_dd = QComboBox(Editor)
        self.project_dd.setObjectName(u"project_dd")
        self.project_dd.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_4.addWidget(self.project_dd)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.entity = QLabel(Editor)
        self.entity.setObjectName(u"entity")

        self.horizontalLayout_5.addWidget(self.entity)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)

        self.entity_dd = QComboBox(Editor)
        self.entity_dd.setObjectName(u"entity_dd")
        self.entity_dd.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_5.addWidget(self.entity_dd)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.task = QLabel(Editor)
        self.task.setObjectName(u"task")

        self.horizontalLayout_6.addWidget(self.task)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_8)

        self.task_dd = QComboBox(Editor)
        self.task_dd.setObjectName(u"task_dd")
        self.task_dd.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_6.addWidget(self.task_dd)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.start_label = QLabel(Editor)
        self.start_label.setObjectName(u"start_label")

        self.horizontalLayout.addWidget(self.start_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.start_date = QDateEdit(Editor)
        self.start_date.setObjectName(u"start_date")
        self.start_date.setFrame(False)
        self.start_date.setCalendarPopup(True)

        self.horizontalLayout.addWidget(self.start_date)

        self.start_time = QTimeEdit(Editor)
        self.start_time.setObjectName(u"start_time")
        self.start_time.setCalendarPopup(False)

        self.horizontalLayout.addWidget(self.start_time)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.end_label = QLabel(Editor)
        self.end_label.setObjectName(u"end_label")

        self.horizontalLayout_2.addWidget(self.end_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.end_date = QDateEdit(Editor)
        self.end_date.setObjectName(u"end_date")
        self.end_date.setCalendarPopup(True)

        self.horizontalLayout_2.addWidget(self.end_date)

        self.end_time = QTimeEdit(Editor)
        self.end_time.setObjectName(u"end_time")

        self.horizontalLayout_2.addWidget(self.end_time)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.groupBox = QGroupBox(Editor)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.reason = QPlainTextEdit(self.groupBox)
        self.reason.setObjectName(u"reason")
        self.reason.setMaximumSize(QSize(16777215, 50))
        self.reason.setFrameShape(QFrame.NoFrame)
        self.reason.setFrameShadow(QFrame.Plain)

        self.verticalLayout.addWidget(self.reason)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.verticalSpacer_2 = QSpacerItem(20, 91, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.update_btn = QPushButton(Editor)
        self.update_btn.setObjectName(u"update_btn")

        self.horizontalLayout_3.addWidget(self.update_btn)

        self.delete_btn = QPushButton(Editor)
        self.delete_btn.setObjectName(u"delete_btn")

        self.horizontalLayout_3.addWidget(self.delete_btn)

        self.cancel_btn = QPushButton(Editor)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.horizontalLayout_3.addWidget(self.cancel_btn)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Editor)

        QMetaObject.connectSlotsByName(Editor)
    # setupUi

    def retranslateUi(self, Editor):
        Editor.setWindowTitle(QCoreApplication.translate("Editor", u"Timesheet Editor", None))
        self.title.setText(QCoreApplication.translate("Editor", u"Timesheet Editor", None))
        self.tid.setText(QCoreApplication.translate("Editor", u"TID:", None))
        self.project.setText(QCoreApplication.translate("Editor", u"PRJ:", None))
        self.entity.setText(QCoreApplication.translate("Editor", u"ENT:", None))
        self.task.setText(QCoreApplication.translate("Editor", u"TSK:", None))
        self.start_label.setText(QCoreApplication.translate("Editor", u"Start Time", None))
        self.end_label.setText(QCoreApplication.translate("Editor", u"End Time", None))
        self.groupBox.setTitle(QCoreApplication.translate("Editor", u"Reason for the change?", None))
        self.update_btn.setText(QCoreApplication.translate("Editor", u"Update", None))
        self.delete_btn.setText(QCoreApplication.translate("Editor", u"Delete", None))
        self.cancel_btn.setText(QCoreApplication.translate("Editor", u"Cancel", None))
    # retranslateUi

