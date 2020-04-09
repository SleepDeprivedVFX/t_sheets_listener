# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_ot_alert.ui'
#
# Created: Mon Nov 04 18:41:21 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtGui, QtCore, QtWidgets

class Ui_OT(object):
    def setupUi(self, OT):
        OT.setObjectName("OT")
        OT.resize(400, 198)
        OT.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout_2 = QtGui.QVBoxLayout(OT)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.title = QtGui.QLabel(OT)
        self.title.setStyleSheet("font: 22pt \"Chiller\";")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.verticalLayout_2.addWidget(self.title)
        self.message1 = QtGui.QLabel(OT)
        self.message1.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.message1.setAlignment(QtCore.Qt.AlignCenter)
        self.message1.setObjectName("message1")
        self.verticalLayout_2.addWidget(self.message1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.minutes = QtGui.QLCDNumber(OT)
        self.minutes.setFrameShape(QtGui.QFrame.Panel)
        self.minutes.setFrameShadow(QtGui.QFrame.Sunken)
        self.minutes.setSmallDecimalPoint(False)
        self.minutes.setNumDigits(3)
        self.minutes.setProperty("intValue", 55)
        self.minutes.setObjectName("minutes")
        self.horizontalLayout.addWidget(self.minutes)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtGui.QLabel(OT)
        self.label_3.setStyleSheet("font: 30pt \"MS Shell Dlg 2\";")
        self.label_3.setTextFormat(QtCore.Qt.PlainText)
        self.label_3.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.seconds = QtGui.QLCDNumber(OT)
        self.seconds.setStyleSheet("")
        self.seconds.setFrameShape(QtGui.QFrame.Panel)
        self.seconds.setFrameShadow(QtGui.QFrame.Sunken)
        self.seconds.setSmallDecimalPoint(False)
        self.seconds.setNumDigits(2)
        self.seconds.setProperty("intValue", 55)
        self.seconds.setObjectName("seconds")
        self.horizontalLayout.addWidget(self.seconds)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.message2 = QtGui.QLabel(OT)
        self.message2.setAlignment(QtCore.Qt.AlignCenter)
        self.message2.setWordWrap(True)
        self.message2.setObjectName("message2")
        self.verticalLayout_2.addWidget(self.message2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.variable_btn = QtGui.QPushButton(OT)
        self.variable_btn.setObjectName("variable_btn")
        self.horizontalLayout_2.addWidget(self.variable_btn)
        self.or_sep = QtGui.QLabel(OT)
        self.or_sep.setObjectName("or_sep")
        self.horizontalLayout_2.addWidget(self.or_sep)
        self.requestOT_btn = QtGui.QPushButton(OT)
        self.requestOT_btn.setObjectName("requestOT_btn")
        self.horizontalLayout_2.addWidget(self.requestOT_btn)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(OT)
        QtCore.QMetaObject.connectSlotsByName(OT)

    def retranslateUi(self, OT):
        OT.setWindowTitle(QtGui.QApplication.translate("OT", "Overtime Form", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("OT", "OVERTIME ALERT!", None, QtGui.QApplication.UnicodeUTF8))
        self.message1.setText(QtGui.QApplication.translate("OT", "You are about to go into overtime!", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("OT", ":", None, QtGui.QApplication.UnicodeUTF8))
        self.message2.setText(QtGui.QApplication.translate("OT", "If you need to stay longer you can request overtime approval.  This is not a guarantee of overtime approval, just a request.", None, QtGui.QApplication.UnicodeUTF8))
        self.variable_btn.setText(QtGui.QApplication.translate("OT", "Thanks for the Reminder", None, QtGui.QApplication.UnicodeUTF8))
        self.or_sep.setText(QtGui.QApplication.translate("OT", "OR", None, QtGui.QApplication.UnicodeUTF8))
        self.requestOT_btn.setText(QtGui.QApplication.translate("OT", "Request OT", None, QtGui.QApplication.UnicodeUTF8))

