# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '\\hal\tools\shotgun\mastertemplate_clone\install\manual\tk-t-sheets\v1.0.0\resources\alert_dialog.ui'
#
# Created: Thu Nov 16 13:53:28 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtGui, QtCore

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(321, 200)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.employee_name = QtGui.QLabel(Dialog)
        self.employee_name.setStyleSheet("font: 75 14pt \"Arial\";")
        self.employee_name.setObjectName("employee_name")
        self.verticalLayout.addWidget(self.employee_name)
        self.alert = QtGui.QLabel(Dialog)
        self.alert.setStyleSheet("font: 75 14pt \"Arial\";\n"
"color: rgb(255, 0, 0);\n"
"")
        self.alert.setAlignment(QtCore.Qt.AlignCenter)
        self.alert.setObjectName("alert")
        self.verticalLayout.addWidget(self.alert)
        self.statement = QtGui.QLabel(Dialog)
        self.statement.setStyleSheet("font: 75 12pt \"Arial\";")
        self.statement.setObjectName("statement")
        self.verticalLayout.addWidget(self.statement)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.eod_timer = QtGui.QTimeEdit(Dialog)
        self.eod_timer.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.eod_timer.setObjectName("eod_timer")
        self.horizontalLayout_2.addWidget(self.eod_timer)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.statement_2 = QtGui.QLabel(Dialog)
        self.statement_2.setStyleSheet("font: 75 10pt \"Arial\";")
        self.statement_2.setObjectName("statement_2")
        self.verticalLayout.addWidget(self.statement_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.ok_btn = QtGui.QPushButton(Dialog)
        self.ok_btn.setStyleSheet("background-color: rgb(85, 170, 0);\n"
"font: 75 10pt \"Arial\";")
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout.addWidget(self.ok_btn)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "T-Sheets Alert!", None, QtGui.QApplication.UnicodeUTF8))
        self.employee_name.setText(QtGui.QApplication.translate("Dialog", "Employee Name", None, QtGui.QApplication.UnicodeUTF8))
        self.alert.setText(QtGui.QApplication.translate("Dialog", "Heads up!", None, QtGui.QApplication.UnicodeUTF8))
        self.statement.setText(QtGui.QApplication.translate("Dialog", "You will be in Overtime in just a few minutes!", None, QtGui.QApplication.UnicodeUTF8))
        self.eod_timer.setDisplayFormat(QtGui.QApplication.translate("Dialog", "h:mm:ss", None, QtGui.QApplication.UnicodeUTF8))
        self.statement_2.setText(QtGui.QApplication.translate("Dialog", "Be sure to let the boss know!", None, QtGui.QApplication.UnicodeUTF8))
        self.ok_btn.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))

