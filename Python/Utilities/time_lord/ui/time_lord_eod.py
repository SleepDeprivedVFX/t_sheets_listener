# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_eod.ui'
#
# Created: Thu Aug 08 10:42:19 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_endofday(object):
    def setupUi(self, endofday):
        endofday.setObjectName("endofday")
        endofday.resize(344, 187)
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
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.last_time_label = QtGui.QLabel(endofday)
        self.last_time_label.setObjectName("last_time_label")
        self.horizontalLayout_2.addWidget(self.last_time_label)
        self.last_time = QtGui.QDateTimeEdit(endofday)
        self.last_time.setObjectName("last_time")
        self.horizontalLayout_2.addWidget(self.last_time)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.yes_btn = QtGui.QPushButton(endofday)
        self.yes_btn.setObjectName("yes_btn")
        self.horizontalLayout.addWidget(self.yes_btn)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.no_btn = QtGui.QPushButton(endofday)
        self.no_btn.setObjectName("no_btn")
        self.horizontalLayout.addWidget(self.no_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(endofday)
        QtCore.QMetaObject.connectSlotsByName(endofday)

    def retranslateUi(self, endofday):
        endofday.setWindowTitle(QtGui.QApplication.translate("endofday", "End of Day", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("endofday", "It\'s Over!", None, QtGui.QApplication.UnicodeUTF8))
        self.question.setText(QtGui.QApplication.translate("endofday", "The day is done, and it looks like you haven\'t touched the computer in a while.  Are you still working?", None, QtGui.QApplication.UnicodeUTF8))
        self.last_time_label.setText(QtGui.QApplication.translate("endofday", "Last Detected Time:", None, QtGui.QApplication.UnicodeUTF8))
        self.yes_btn.setText(QtGui.QApplication.translate("endofday", "Still Working", None, QtGui.QApplication.UnicodeUTF8))
        self.no_btn.setText(QtGui.QApplication.translate("endofday", "Clock Out: 00:00:00", None, QtGui.QApplication.UnicodeUTF8))

