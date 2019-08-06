# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_lunch.ui'
#
# Created: Tue Aug 06 12:29:20 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_lunch_form(object):
    def setupUi(self, lunch_form):
        lunch_form.setObjectName("lunch_form")
        lunch_form.resize(561, 145)
        lunch_form.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(238, 29, 35);")
        self.verticalLayout = QtGui.QVBoxLayout(lunch_form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lunch_title = QtGui.QLabel(lunch_form)
        self.lunch_title.setStyleSheet("font: 24pt \"Algerian\";\n"
"color: rgb(239, 30, 36);\n"
"border-color: rgb(24, 84, 148);\n"
"border-width: 4px;")
        self.lunch_title.setObjectName("lunch_title")
        self.horizontalLayout_3.addWidget(self.lunch_title)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.lunch_message = QtGui.QLabel(lunch_form)
        self.lunch_message.setStyleSheet("background-color: rgb(250, 175, 24);\n"
"font: 12pt \"Arial Rounded MT Bold\";\n"
"color: rgb(255, 255, 255);")
        self.lunch_message.setAlignment(QtCore.Qt.AlignCenter)
        self.lunch_message.setWordWrap(True)
        self.lunch_message.setObjectName("lunch_message")
        self.verticalLayout.addWidget(self.lunch_message)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.from_label = QtGui.QLabel(lunch_form)
        self.from_label.setStyleSheet("color: rgb(24, 84, 148);")
        self.from_label.setObjectName("from_label")
        self.horizontalLayout.addWidget(self.from_label)
        self.start_time = QtGui.QTimeEdit(lunch_form)
        self.start_time.setStyleSheet("color: rgb(24, 84, 148);")
        self.start_time.setObjectName("start_time")
        self.horizontalLayout.addWidget(self.start_time)
        self.to_label = QtGui.QLabel(lunch_form)
        self.to_label.setStyleSheet("color: rgb(24, 84, 148);")
        self.to_label.setObjectName("to_label")
        self.horizontalLayout.addWidget(self.to_label)
        self.end_time = QtGui.QTimeEdit(lunch_form)
        self.end_time.setStyleSheet("color: rgb(24, 84, 148);")
        self.end_time.setObjectName("end_time")
        self.horizontalLayout.addWidget(self.end_time)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.skip_btn = QtGui.QPushButton(lunch_form)
        self.skip_btn.setStyleSheet("background-color: rgb(24, 84, 148);\n"
"color: rgb(250, 175, 24);")
        self.skip_btn.setObjectName("skip_btn")
        self.horizontalLayout_2.addWidget(self.skip_btn)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.ok_btn = QtGui.QPushButton(lunch_form)
        self.ok_btn.setStyleSheet("background-color: rgb(24, 84, 148);\n"
"color: rgb(250, 175, 24);")
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout_2.addWidget(self.ok_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(lunch_form)
        QtCore.QMetaObject.connectSlotsByName(lunch_form)

    def retranslateUi(self, lunch_form):
        lunch_form.setWindowTitle(QtGui.QApplication.translate("lunch_form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.lunch_title.setText(QtGui.QApplication.translate("lunch_form", "LUNCH!", None, QtGui.QApplication.UnicodeUTF8))
        self.lunch_message.setText(QtGui.QApplication.translate("lunch_form", "Hey %s, were you at lunch at the following times?", None, QtGui.QApplication.UnicodeUTF8))
        self.from_label.setText(QtGui.QApplication.translate("lunch_form", "From", None, QtGui.QApplication.UnicodeUTF8))
        self.to_label.setText(QtGui.QApplication.translate("lunch_form", "To", None, QtGui.QApplication.UnicodeUTF8))
        self.skip_btn.setText(QtGui.QApplication.translate("lunch_form", "I Skipped Lunch", None, QtGui.QApplication.UnicodeUTF8))
        self.ok_btn.setText(QtGui.QApplication.translate("lunch_form", "I Took My Lunch", None, QtGui.QApplication.UnicodeUTF8))

