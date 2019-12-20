# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_scope.ui'
#
# Created: Wed Dec 18 18:23:38 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_WhosWorking(object):
    def setupUi(self, WhosWorking):
        WhosWorking.setObjectName("WhosWorking")
        WhosWorking.resize(566, 683)
        WhosWorking.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout = QtGui.QVBoxLayout(WhosWorking)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Title = QtGui.QLabel(WhosWorking)
        self.Title.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";")
        self.Title.setObjectName("Title")
        self.verticalLayout.addWidget(self.Title)
        self.slave_list = QtGui.QTableWidget(WhosWorking)
        self.slave_list.setObjectName("slave_list")
        self.slave_list.setColumnCount(4)
        self.slave_list.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setItem(0, 2, item)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setItem(0, 3, item)
        self.slave_list.horizontalHeader().setVisible(False)
        self.slave_list.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.slave_list)

        self.retranslateUi(WhosWorking)
        QtCore.QMetaObject.connectSlotsByName(WhosWorking)

    def retranslateUi(self, WhosWorking):
        WhosWorking.setWindowTitle(QtGui.QApplication.translate("WhosWorking", "Time Lord Scope", None, QtGui.QApplication.UnicodeUTF8))
        self.Title.setText(QtGui.QApplication.translate("WhosWorking", "Who\'s Working On What?", None, QtGui.QApplication.UnicodeUTF8))
        self.slave_list.verticalHeaderItem(0).setText(QtGui.QApplication.translate("WhosWorking", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.slave_list.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("WhosWorking", "Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.slave_list.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("WhosWorking", "Task", None, QtGui.QApplication.UnicodeUTF8))
        self.slave_list.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("WhosWorking", "Time", None, QtGui.QApplication.UnicodeUTF8))
        self.slave_list.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("WhosWorking", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.slave_list.isSortingEnabled()
        self.slave_list.setSortingEnabled(False)
        self.slave_list.setSortingEnabled(__sortingEnabled)

