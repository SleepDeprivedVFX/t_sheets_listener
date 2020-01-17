# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\adamb\OneDrive\Documents\Scripts\Python\Utilities\time_lord\ui\time_lord_edit_timesheet.ui'
#
# Created: Thu Jan 16 13:43:10 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Editor(object):
    def setupUi(self, Editor):
        Editor.setObjectName("Editor")
        Editor.resize(285, 201)
        Editor.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout = QtGui.QVBoxLayout(Editor)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtGui.QLabel(Editor)
        self.title.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";")
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.project = QtGui.QLabel(Editor)
        self.project.setObjectName("project")
        self.verticalLayout.addWidget(self.project)
        self.entity = QtGui.QLabel(Editor)
        self.entity.setObjectName("entity")
        self.verticalLayout.addWidget(self.entity)
        self.task = QtGui.QLabel(Editor)
        self.task.setObjectName("task")
        self.verticalLayout.addWidget(self.task)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.start_label = QtGui.QLabel(Editor)
        self.start_label.setObjectName("start_label")
        self.horizontalLayout.addWidget(self.start_label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.start = QtGui.QDateTimeEdit(Editor)
        self.start.setCalendarPopup(True)
        self.start.setObjectName("start")
        self.horizontalLayout.addWidget(self.start)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.end_label = QtGui.QLabel(Editor)
        self.end_label.setObjectName("end_label")
        self.horizontalLayout_2.addWidget(self.end_label)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.end = QtGui.QDateTimeEdit(Editor)
        self.end.setObjectName("end")
        self.horizontalLayout_2.addWidget(self.end)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(Editor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Discard|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Editor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Editor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Editor.reject)
        QtCore.QMetaObject.connectSlotsByName(Editor)

    def retranslateUi(self, Editor):
        Editor.setWindowTitle(QtGui.QApplication.translate("Editor", "Timesheet Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("Editor", "Timesheet Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.project.setText(QtGui.QApplication.translate("Editor", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.entity.setText(QtGui.QApplication.translate("Editor", "Entity", None, QtGui.QApplication.UnicodeUTF8))
        self.task.setText(QtGui.QApplication.translate("Editor", "Task", None, QtGui.QApplication.UnicodeUTF8))
        self.start_label.setText(QtGui.QApplication.translate("Editor", "Start Time", None, QtGui.QApplication.UnicodeUTF8))
        self.end_label.setText(QtGui.QApplication.translate("Editor", "End Time", None, QtGui.QApplication.UnicodeUTF8))

