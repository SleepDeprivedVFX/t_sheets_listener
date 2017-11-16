# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '\\hal\tools\shotgun\mastertemplate_clone\install\manual\tk-t-sheets\v1.0.0\resources\lunch_break_dialog.ui'
#
# Created: Thu Nov 16 13:53:10 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(356, 166)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.employee_name = QtGui.QLabel(Dialog)
        self.employee_name.setStyleSheet("font: 75 14pt \"Arial\";")
        self.employee_name.setObjectName("employee_name")
        self.verticalLayout_3.addWidget(self.employee_name)
        self.question = QtGui.QLabel(Dialog)
        self.question.setStyleSheet("font: 75 12pt \"Arial\";")
        self.question.setObjectName("question")
        self.verticalLayout_3.addWidget(self.question)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.start_label = QtGui.QLabel(Dialog)
        self.start_label.setObjectName("start_label")
        self.verticalLayout_2.addWidget(self.start_label)
        self.start_time = QtGui.QTimeEdit(Dialog)
        self.start_time.setObjectName("start_time")
        self.verticalLayout_2.addWidget(self.start_time)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.end_label = QtGui.QLabel(Dialog)
        self.end_label.setObjectName("end_label")
        self.verticalLayout.addWidget(self.end_label)
        self.end_time = QtGui.QTimeEdit(Dialog)
        self.end_time.setObjectName("end_time")
        self.verticalLayout.addWidget(self.end_time)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.yes_btn = QtGui.QPushButton(Dialog)
        self.yes_btn.setStyleSheet("background-color: rgb(85, 170, 0);font: 75 10pt \"Arial\";")
        self.yes_btn.setObjectName("yes_btn")
        self.horizontalLayout.addWidget(self.yes_btn)
        self.no_btn = QtGui.QPushButton(Dialog)
        self.no_btn.setStyleSheet("background-color: rgb(170, 0, 0);")
        self.no_btn.setObjectName("no_btn")
        self.horizontalLayout.addWidget(self.no_btn)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "T-Sheets Lunch Break Utility", None, QtGui.QApplication.UnicodeUTF8))
        self.employee_name.setText(QtGui.QApplication.translate("Dialog", "Employee Name", None, QtGui.QApplication.UnicodeUTF8))
        self.question.setText(QtGui.QApplication.translate("Dialog", "Is this lunch break correct?", None, QtGui.QApplication.UnicodeUTF8))
        self.start_label.setText(QtGui.QApplication.translate("Dialog", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.end_label.setText(QtGui.QApplication.translate("Dialog", "End", None, QtGui.QApplication.UnicodeUTF8))
        self.yes_btn.setText(QtGui.QApplication.translate("Dialog", "Yes", None, QtGui.QApplication.UnicodeUTF8))
        self.no_btn.setText(QtGui.QApplication.translate("Dialog", "No", None, QtGui.QApplication.UnicodeUTF8))

