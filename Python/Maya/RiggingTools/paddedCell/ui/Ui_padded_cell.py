# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Adam\OneDrive\Documents\Scripts\Python\Maya\RiggingTools\paddedCell\ui\Ui_padded_cell.ui'
#
# Created: Sun Oct 01 23:05:51 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_paddedCellForm(object):
    def setupUi(self, paddedCellForm):
        paddedCellForm.setObjectName("paddedCellForm")
        paddedCellForm.setWindowModality(QtCore.Qt.ApplicationModal)
        paddedCellForm.resize(1085, 545)
        paddedCellForm.setMinimumSize(QtCore.QSize(1085, 545))
        paddedCellForm.setWindowOpacity(1.0)
        paddedCellForm.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.525, cy:0.54, radius:0.886, fx:0.525, fy:0.534, stop:0.407563 rgba(0, 0, 0, 255), stop:1 rgba(198, 86, 0, 255));\n"
"border-color: rgba(0, 0, 0, 0);\n"
"selection-background-color: rgb(255, 106, 0);\n"
"selection-color: rgb(255, 106, 0);")
        self.verticalLayout_6 = QtGui.QVBoxLayout(paddedCellForm)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.column_1 = QtGui.QFrame(paddedCellForm)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.column_1.sizePolicy().hasHeightForWidth())
        self.column_1.setSizePolicy(sizePolicy)
        self.column_1.setMaximumSize(QtCore.QSize(400, 16777215))
        self.column_1.setStyleSheet("font: 75 12pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.column_1.setObjectName("column_1")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.column_1)
        self.verticalLayout_5.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.title = QtGui.QLabel(self.column_1)
        self.title.setMinimumSize(QtCore.QSize(350, 60))
        self.title.setMaximumSize(QtCore.QSize(400, 16777215))
        self.title.setStyleSheet("font: 75 24pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.title.setObjectName("title")
        self.verticalLayout_5.addWidget(self.title)
        self.subtitle = QtGui.QLabel(self.column_1)
        self.subtitle.setMaximumSize(QtCore.QSize(400, 45))
        self.subtitle.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.subtitle.setObjectName("subtitle")
        self.verticalLayout_5.addWidget(self.subtitle)
        self.Build_Padding = QtGui.QGroupBox(self.column_1)
        self.Build_Padding.setMinimumSize(QtCore.QSize(491, 0))
        self.Build_Padding.setStyleSheet("font: 75 12pt \"Orbitron\";\n"
"border-color: rgb(255, 129, 2);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.Build_Padding.setCheckable(True)
        self.Build_Padding.setObjectName("Build_Padding")
        self.verticalLayout = QtGui.QVBoxLayout(self.Build_Padding)
        self.verticalLayout.setContentsMargins(-1, 20, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.build_controls = QtGui.QGroupBox(self.Build_Padding)
        self.build_controls.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);\n"
"border: rgb(198, 86, 0);")
        self.build_controls.setObjectName("build_controls")
        self.build_padding_layout = QtGui.QGridLayout(self.build_controls)
        self.build_padding_layout.setObjectName("build_padding_layout")
        self.pad_diagram = QtGui.QFrame(self.build_controls)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pad_diagram.sizePolicy().hasHeightForWidth())
        self.pad_diagram.setSizePolicy(sizePolicy)
        self.pad_diagram.setMinimumSize(QtCore.QSize(230, 145))
        self.pad_diagram.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"background-image: url(:/icons/folder_diagram.png);\n"
"background-repeat: none;")
        self.pad_diagram.setFrameShape(QtGui.QFrame.StyledPanel)
        self.pad_diagram.setFrameShadow(QtGui.QFrame.Raised)
        self.pad_diagram.setObjectName("pad_diagram")
        self.pad_label = QtGui.QLabel(self.pad_diagram)
        self.pad_label.setGeometry(QtCore.QRect(50, 70, 43, 25))
        self.pad_label.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);\n"
"background-image: url(:/icons/spacer.png);")
        self.pad_label.setObjectName("pad_label")
        self.offset_label = QtGui.QLabel(self.pad_diagram)
        self.offset_label.setGeometry(QtCore.QRect(30, 30, 69, 25))
        self.offset_label.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-image: url(:/icons/spacer.png);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.offset_label.setObjectName("offset_label")
        self.offset_name = QtGui.QLineEdit(self.pad_diagram)
        self.offset_name.setGeometry(QtCore.QRect(100, 30, 111, 32))
        self.offset_name.setStyleSheet("font: 75 12pt \"Orbitron\";\n"
"background-image: url(:/icons/spacer.png);\n"
"alternate-background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 106, 0);\n"
"background-color: rgba(255, 106, 0, 75);\n"
"selection-background-color: rgb(0, 0, 0);\n"
"selection-color: rgba(0, 0, 0, 0);\n"
"border: None;")
        self.offset_name.setObjectName("offset_name")
        self.your_object = QtGui.QLabel(self.pad_diagram)
        self.your_object.setGeometry(QtCore.QRect(70, 110, 130, 25))
        self.your_object.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);\n"
"background-image: url(:/icons/spacer.png);")
        self.your_object.setObjectName("your_object")
        self.pad_name = QtGui.QLineEdit(self.pad_diagram)
        self.pad_name.setGeometry(QtCore.QRect(100, 70, 111, 32))
        self.pad_name.setStyleSheet("font: 75 12pt \"Orbitron\";\n"
"alternate-background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 106, 0);\n"
"background-color: rgba(255, 106, 0, 75);\n"
"selection-background-color: rgb(0, 0, 0);\n"
"selection-color: rgba(0, 0, 0, 0);\n"
"border: None;\n"
"background-image: url(:/icons/spacer.png);")
        self.pad_name.setObjectName("pad_name")
        self.build_padding_layout.addWidget(self.pad_diagram, 0, 0, 2, 1)
        spacerItem = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.build_padding_layout.addItem(spacerItem, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.build_controls)
        self.build_output = QtGui.QVBoxLayout()
        self.build_output.setObjectName("build_output")
        self.new_offset_layout = QtGui.QHBoxLayout()
        self.new_offset_layout.setObjectName("new_offset_layout")
        self.new_offset_label = QtGui.QLabel(self.Build_Padding)
        self.new_offset_label.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.new_offset_label.setObjectName("new_offset_label")
        self.new_offset_layout.addWidget(self.new_offset_label)
        self.new_offset_name = QtGui.QLabel(self.Build_Padding)
        self.new_offset_name.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);\n"
"font-weight: bold;")
        self.new_offset_name.setObjectName("new_offset_name")
        self.new_offset_layout.addWidget(self.new_offset_name)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.new_offset_layout.addItem(spacerItem1)
        self.build_output.addLayout(self.new_offset_layout)
        self.new_name_layout = QtGui.QHBoxLayout()
        self.new_name_layout.setObjectName("new_name_layout")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.new_name_layout.addItem(spacerItem2)
        self.new_pad_label = QtGui.QLabel(self.Build_Padding)
        self.new_pad_label.setMaximumSize(QtCore.QSize(150, 16777215))
        self.new_pad_label.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.new_pad_label.setObjectName("new_pad_label")
        self.new_name_layout.addWidget(self.new_pad_label)
        self.new_pad_name = QtGui.QLabel(self.Build_Padding)
        self.new_pad_name.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);\n"
"font-weight: bold;")
        self.new_pad_name.setObjectName("new_pad_name")
        self.new_name_layout.addWidget(self.new_pad_name)
        self.build_output.addLayout(self.new_name_layout)
        self.verticalLayout.addLayout(self.build_output)
        self.verticalLayout_5.addWidget(self.Build_Padding)
        self.horizontalLayout_5.addWidget(self.column_1)
        self.column_2 = QtGui.QFrame(paddedCellForm)
        self.column_2.setStyleSheet("font: 75 12pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.column_2.setObjectName("column_2")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.column_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtGui.QGroupBox(self.column_2)
        self.groupBox.setStyleSheet("font: 75 12pt \"Orbitron\";\n"
"border-color: rgb(255, 129, 2);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.groupBox.setCheckable(True)
        self.groupBox.setChecked(False)
        self.groupBox.setObjectName("groupBox")
        self.widget = QtGui.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(10, 50, 497, 131))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.addapad_ = QtGui.QLabel(self.widget)
        self.addapad_.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.addapad_.setWordWrap(True)
        self.addapad_.setObjectName("addapad_")
        self.verticalLayout_2.addWidget(self.addapad_)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.suffix_name = QtGui.QLabel(self.widget)
        self.suffix_name.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.suffix_name.setObjectName("suffix_name")
        self.horizontalLayout.addWidget(self.suffix_name)
        self.addapad_name = QtGui.QLineEdit(self.widget)
        self.addapad_name.setStyleSheet("font: 75 12pt \"Orbitron\";\n"
"alternate-background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 106, 0);\n"
"background-color: rgba(255, 106, 0, 75);\n"
"selection-background-color: rgb(0, 0, 0);\n"
"selection-color: rgba(0, 0, 0, 0);\n"
"border: None;")
        self.addapad_name.setObjectName("addapad_name")
        self.horizontalLayout.addWidget(self.addapad_name)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.addapad_out_label = QtGui.QLabel(self.widget)
        self.addapad_out_label.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.addapad_out_label.setObjectName("addapad_out_label")
        self.horizontalLayout_2.addWidget(self.addapad_out_label)
        self.addapad_output = QtGui.QLabel(self.widget)
        self.addapad_output.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);\n"
"font-weight: bold;")
        self.addapad_output.setObjectName("addapad_output")
        self.horizontalLayout_2.addWidget(self.addapad_output)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.column_2)
        self.groupBox_2.setStyleSheet("font: 75 12pt \"Orbitron\";\n"
"border-color: rgb(255, 129, 2);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.groupBox_2.setCheckable(True)
        self.groupBox_2.setChecked(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.widget1 = QtGui.QWidget(self.groupBox_2)
        self.widget1.setGeometry(QtCore.QRect(10, 50, 508, 129))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.widget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.instructions = QtGui.QLabel(self.widget1)
        self.instructions.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.instructions.setObjectName("instructions")
        self.verticalLayout_3.addWidget(self.instructions)
        self.match_child = QtGui.QCheckBox(self.widget1)
        self.match_child.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.match_child.setObjectName("match_child")
        self.verticalLayout_3.addWidget(self.match_child)
        self.match_parent = QtGui.QCheckBox(self.widget1)
        self.match_parent.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.match_parent.setObjectName("match_parent")
        self.verticalLayout_3.addWidget(self.match_parent)
        self.freeze_trans = QtGui.QCheckBox(self.widget1)
        self.freeze_trans.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.freeze_trans.setObjectName("freeze_trans")
        self.verticalLayout_3.addWidget(self.freeze_trans)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.horizontalLayout_5.addWidget(self.column_2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cancel_btn = QtGui.QPushButton(paddedCellForm)
        self.cancel_btn.setStyleSheet("background-color: rgb(255, 106, 0);\n"
"font: 75 8pt \"Orbitron\";\n"
"color: rgb(0, 0, 0);\n"
"padding: 5px;")
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_4.addWidget(self.cancel_btn)
        self.reset_btn = QtGui.QPushButton(paddedCellForm)
        self.reset_btn.setStyleSheet("background-color: rgb(255, 106, 0);\n"
"font: 75 8pt \"Orbitron\";\n"
"color: rgb(0, 0, 0);\n"
"padding: 5px;")
        self.reset_btn.setObjectName("reset_btn")
        self.horizontalLayout_4.addWidget(self.reset_btn)
        self.build_btn = QtGui.QPushButton(paddedCellForm)
        self.build_btn.setStyleSheet("background-color: rgb(255, 106, 0);\n"
"font: 75 8pt \"Orbitron\";\n"
"color: rgb(0, 0, 0);\n"
"padding: 5px;")
        self.build_btn.setObjectName("build_btn")
        self.horizontalLayout_4.addWidget(self.build_btn)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.retranslateUi(paddedCellForm)
        QtCore.QMetaObject.connectSlotsByName(paddedCellForm)

    def retranslateUi(self, paddedCellForm):
        paddedCellForm.setWindowTitle(QtGui.QApplication.translate("paddedCellForm", "Padded Cell", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setText(QtGui.QApplication.translate("paddedCellForm", "Padded Cell", None, QtGui.QApplication.UnicodeUTF8))
        self.subtitle.setText(QtGui.QApplication.translate("paddedCellForm", "Fight hierarchy padding insanity", None, QtGui.QApplication.UnicodeUTF8))
        self.Build_Padding.setTitle(QtGui.QApplication.translate("paddedCellForm", "Build Standard Group Pads", None, QtGui.QApplication.UnicodeUTF8))
        self.pad_label.setText(QtGui.QApplication.translate("paddedCellForm", "Pad", None, QtGui.QApplication.UnicodeUTF8))
        self.offset_label.setText(QtGui.QApplication.translate("paddedCellForm", "Offset", None, QtGui.QApplication.UnicodeUTF8))
        self.offset_name.setText(QtGui.QApplication.translate("paddedCellForm", "OFF", None, QtGui.QApplication.UnicodeUTF8))
        self.your_object.setText(QtGui.QApplication.translate("paddedCellForm", "Your Object", None, QtGui.QApplication.UnicodeUTF8))
        self.pad_name.setText(QtGui.QApplication.translate("paddedCellForm", "PAD", None, QtGui.QApplication.UnicodeUTF8))
        self.new_offset_label.setText(QtGui.QApplication.translate("paddedCellForm", "New Offset:", None, QtGui.QApplication.UnicodeUTF8))
        self.new_offset_name.setText(QtGui.QApplication.translate("paddedCellForm", "your_object_OFF", None, QtGui.QApplication.UnicodeUTF8))
        self.new_pad_label.setText(QtGui.QApplication.translate("paddedCellForm", "New Pad:", None, QtGui.QApplication.UnicodeUTF8))
        self.new_pad_name.setText(QtGui.QApplication.translate("paddedCellForm", "your_object_PAD", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("paddedCellForm", "Add-a-Pad", None, QtGui.QApplication.UnicodeUTF8))
        self.addapad_.setText(QtGui.QApplication.translate("paddedCellForm", "Insert a pad above your currently selected object.", None, QtGui.QApplication.UnicodeUTF8))
        self.suffix_name.setText(QtGui.QApplication.translate("paddedCellForm", "Suffix/Tag Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.addapad_name.setText(QtGui.QApplication.translate("paddedCellForm", "ANIM", None, QtGui.QApplication.UnicodeUTF8))
        self.addapad_out_label.setText(QtGui.QApplication.translate("paddedCellForm", "New Pad:", None, QtGui.QApplication.UnicodeUTF8))
        self.addapad_output.setText(QtGui.QApplication.translate("paddedCellForm", "your_object_ANIM", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("paddedCellForm", "Patch-a-Pad", None, QtGui.QApplication.UnicodeUTF8))
        self.instructions.setText(QtGui.QApplication.translate("paddedCellForm", "Fix existing pad pivots and freeze translations", None, QtGui.QApplication.UnicodeUTF8))
        self.match_child.setText(QtGui.QApplication.translate("paddedCellForm", "Match Pivot to Child", None, QtGui.QApplication.UnicodeUTF8))
        self.match_parent.setText(QtGui.QApplication.translate("paddedCellForm", "Match Pivot to Parent", None, QtGui.QApplication.UnicodeUTF8))
        self.freeze_trans.setText(QtGui.QApplication.translate("paddedCellForm", "Freeze Transforms", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_btn.setText(QtGui.QApplication.translate("paddedCellForm", "Cancel\n"
"Close", None, QtGui.QApplication.UnicodeUTF8))
        self.reset_btn.setText(QtGui.QApplication.translate("paddedCellForm", "Reset\n"
"Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.build_btn.setText(QtGui.QApplication.translate("paddedCellForm", "Build\n"
"Padding", None, QtGui.QApplication.UnicodeUTF8))

import bgs_rc
