# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_scope.ui'
#
# Created: Fri Dec 20 14:10:57 2019
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
        self.question = QtGui.QLabel(WhosWorking)
        self.question.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.question.setObjectName("question")
        self.verticalLayout.addWidget(self.question)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.stay_on_top = QtGui.QCheckBox(WhosWorking)
        self.stay_on_top.setObjectName("stay_on_top")
        self.horizontalLayout.addWidget(self.stay_on_top)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.slave_list = QtGui.QTableWidget(WhosWorking)
        self.slave_list.setStyleSheet("QHeaderView::section{\n"
"    \n"
"    background-color: rgb(97, 97, 97);\n"
"}\n"
"QTableView::item{\n"
"    border: 0px;\n"
"    padding: 5px;\n"
"}")
        self.slave_list.setAlternatingRowColors(False)
        self.slave_list.setObjectName("slave_list")
        self.slave_list.setColumnCount(5)
        self.slave_list.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.slave_list.setHorizontalHeaderItem(4, item)
        self.slave_list.horizontalHeader().setVisible(True)
        self.slave_list.horizontalHeader().setCascadingSectionResizes(True)
        self.slave_list.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.slave_list)

        self.retranslateUi(WhosWorking)
        QtCore.QMetaObject.connectSlotsByName(WhosWorking)

    def retranslateUi(self, WhosWorking):
        WhosWorking.setWindowTitle(QtGui.QApplication.translate("WhosWorking", "Time Lord Scope", None, QtGui.QApplication.UnicodeUTF8))
        self.Title.setText(QtGui.QApplication.translate("WhosWorking", "Time Scope", None, QtGui.QApplication.UnicodeUTF8))
        self.question.setText(QtGui.QApplication.translate("WhosWorking", "Who\'s working on what?", None, QtGui.QApplication.UnicodeUTF8))
        self.stay_on_top.setText(QtGui.QApplication.translate("WhosWorking", "Keep On Top", None, QtGui.QApplication.UnicodeUTF8))
        self.slave_list.setSortingEnabled(True)
        self.slave_list.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("WhosWorking", "Artist", None, QtGui.QApplication.UnicodeUTF8))
        self.slave_list.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("WhosWorking", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.slave_list.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("WhosWorking", "Task", None, QtGui.QApplication.UnicodeUTF8))
        self.slave_list.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("WhosWorking", "Time", None, QtGui.QApplication.UnicodeUTF8))
        self.slave_list.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("WhosWorking", "Edit", None, QtGui.QApplication.UnicodeUTF8))

