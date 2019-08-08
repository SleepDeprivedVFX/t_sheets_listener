# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_eod.ui'
#
# Created: Wed Aug 07 17:49:42 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_endofday(object):
    def setupUi(self, endofday):
        endofday.setObjectName("endofday")
        endofday.resize(344, 143)
        endofday.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout = QtGui.QVBoxLayout(endofday)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtGui.QLabel(endofday)
        self.title.setStyleSheet("font: 22pt \"Chiller\";")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.question = QtGui.QLabel(endofday)
        self.question.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.question.setWordWrap(True)
        self.question.setObjectName("question")
        self.verticalLayout.addWidget(self.question)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_2 = QtGui.QPushButton(endofday)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(endofday)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(endofday)
        QtCore.QMetaObject.connectSlotsByName(endofday)

    def retranslateUi(self, endofday):
        endofday.setWindowTitle(QtGui.QApplication.translate("endofday", "End of Day", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("endofday", "It\'s Over!", None, QtGui.QApplication.UnicodeUTF8))
        self.question.setText(QtGui.QApplication.translate("endofday", "The day is done, and it looks like you haven\'t touched the computer in a while.  Are you still working?", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("endofday", "No!  I\'m done.", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("endofday", "Yes I am!", None, QtGui.QApplication.UnicodeUTF8))

