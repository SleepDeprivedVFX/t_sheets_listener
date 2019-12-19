# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_scope.ui'
#
# Created: Wed Dec 18 18:02:14 2019
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
        self.label = QtGui.QLabel(WhosWorking)
        self.label.setStyleSheet("font: 75 16pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tableWidget = QtGui.QTableWidget(WhosWorking)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setItem(0, 3, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslateUi(WhosWorking)
        QtCore.QMetaObject.connectSlotsByName(WhosWorking)

    def retranslateUi(self, WhosWorking):
        WhosWorking.setWindowTitle(QtGui.QApplication.translate("WhosWorking", "Time Lord Scope", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("WhosWorking", "Who\'s Working On What?", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.verticalHeaderItem(0).setText(QtGui.QApplication.translate("WhosWorking", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("WhosWorking", "Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("WhosWorking", "Task", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("WhosWorking", "Time", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("WhosWorking", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.item(0, 0).setText(QtGui.QApplication.translate("WhosWorking", "Adam Benson", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.item(0, 1).setText(QtGui.QApplication.translate("WhosWorking", "WeVR\\nThing\\nTask", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.item(0, 2).setText(QtGui.QApplication.translate("WhosWorking", "00:12:15", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.item(0, 3).setText(QtGui.QApplication.translate("WhosWorking", "BUTTON", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setSortingEnabled(__sortingEnabled)

