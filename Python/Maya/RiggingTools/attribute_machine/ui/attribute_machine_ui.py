# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\sleep\OneDrive\Documents\Scripts\Python\Maya\RiggingTools\attribute_machine\ui\attribute_machine_ui.ui'
#
# Created: Sun Sep 23 14:13:02 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_machine(object):
    def setupUi(self, machine):
        machine.setObjectName("machine")
        machine.setWindowModality(QtCore.Qt.WindowModal)
        machine.resize(731, 727)
        machine.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout_6 = QtGui.QVBoxLayout(machine)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.Title = QtGui.QLabel(machine)
        self.Title.setStyleSheet("font: 75 22pt \"BankGothic\";")
        self.Title.setObjectName("Title")
        self.verticalLayout_6.addWidget(self.Title)
        self.Descriptor = QtGui.QLabel(machine)
        self.Descriptor.setObjectName("Descriptor")
        self.verticalLayout_6.addWidget(self.Descriptor)
        self.modes_group = QtGui.QGroupBox(machine)
        self.modes_group.setMinimumSize(QtCore.QSize(0, 75))
        self.modes_group.setObjectName("modes_group")
        self.layoutWidget = QtGui.QWidget(self.modes_group)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 30, 481, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_mode = QtGui.QRadioButton(self.layoutWidget)
        self.add_mode.setChecked(True)
        self.add_mode.setObjectName("add_mode")
        self.horizontalLayout.addWidget(self.add_mode)
        self.set_mode = QtGui.QRadioButton(self.layoutWidget)
        self.set_mode.setObjectName("set_mode")
        self.horizontalLayout.addWidget(self.set_mode)
        self.connect_mode = QtGui.QRadioButton(self.layoutWidget)
        self.connect_mode.setObjectName("connect_mode")
        self.horizontalLayout.addWidget(self.connect_mode)
        self.command_mode = QtGui.QRadioButton(self.layoutWidget)
        self.command_mode.setObjectName("command_mode")
        self.horizontalLayout.addWidget(self.command_mode)
        self.verticalLayout_6.addWidget(self.modes_group)
        self.attr_type = QtGui.QGroupBox(machine)
        self.attr_type.setMinimumSize(QtCore.QSize(0, 100))
        self.attr_type.setObjectName("attr_type")
        self.widget = QtGui.QWidget(self.attr_type)
        self.widget.setGeometry(QtCore.QRect(30, 20, 641, 65))
        self.widget.setObjectName("widget")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.vector_btn = QtGui.QRadioButton(self.widget)
        self.vector_btn.setStyleSheet("QRadioButton:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QRadioButton:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.vector_btn.setObjectName("vector_btn")
        self.horizontalLayout_7.addWidget(self.vector_btn)
        self.int_btn = QtGui.QRadioButton(self.widget)
        self.int_btn.setStyleSheet("QRadioButton:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QRadioButton:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.int_btn.setObjectName("int_btn")
        self.horizontalLayout_7.addWidget(self.int_btn)
        self.string_btn = QtGui.QRadioButton(self.widget)
        self.string_btn.setStyleSheet("QRadioButton:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QRadioButton:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.string_btn.setObjectName("string_btn")
        self.horizontalLayout_7.addWidget(self.string_btn)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.float_btn = QtGui.QRadioButton(self.widget)
        self.float_btn.setStyleSheet("QRadioButton:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QRadioButton:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.float_btn.setObjectName("float_btn")
        self.horizontalLayout_6.addWidget(self.float_btn)
        self.bool_btn = QtGui.QRadioButton(self.widget)
        self.bool_btn.setStyleSheet("QRadioButton:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QRadioButton:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.bool_btn.setObjectName("bool_btn")
        self.horizontalLayout_6.addWidget(self.bool_btn)
        self.enum_btn = QtGui.QRadioButton(self.widget)
        self.enum_btn.setStyleSheet("QRadioButton:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QRadioButton:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.enum_btn.setObjectName("enum_btn")
        self.horizontalLayout_6.addWidget(self.enum_btn)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.verticalLayout_6.addWidget(self.attr_type)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.min_val_label = QtGui.QLabel(machine)
        self.min_val_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.min_val_label.setObjectName("min_val_label")
        self.verticalLayout.addWidget(self.min_val_label)
        self.min_val = QtGui.QLineEdit(machine)
        self.min_val.setEnabled(True)
        self.min_val.setStyleSheet("QLineEdit:disabled {\n"
"    color:rgb(117, 117, 117);\n"
"    border: rgb(100, 100, 100);\n"
"}\n"
"QLineEdit:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"    border: rgb(220, 220, 220);\n"
"}")
        self.min_val.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.min_val.setObjectName("min_val")
        self.verticalLayout.addWidget(self.min_val)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.max_val_label = QtGui.QLabel(machine)
        self.max_val_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.max_val_label.setObjectName("max_val_label")
        self.verticalLayout_2.addWidget(self.max_val_label)
        self.max_val = QtGui.QLineEdit(machine)
        self.max_val.setStyleSheet("QLineEdit:disabled {\n"
"    color:rgb(117, 117, 117);\n"
"    border: rgb(100, 100, 100);\n"
"}\n"
"QLineEdit:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"    border: rgb(220, 220, 220);\n"
"}")
        self.max_val.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.max_val.setObjectName("max_val")
        self.verticalLayout_2.addWidget(self.max_val)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.default_val_label = QtGui.QLabel(machine)
        self.default_val_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.default_val_label.setObjectName("default_val_label")
        self.verticalLayout_3.addWidget(self.default_val_label)
        self.default_val = QtGui.QLineEdit(machine)
        self.default_val.setStyleSheet("QLineEdit:disabled {\n"
"    color:rgb(117, 117, 117);\n"
"    border: rgb(100, 100, 100);\n"
"}\n"
"QLineEdit:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"    border: rgb(220, 220, 220);\n"
"}")
        self.default_val.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.default_val.setObjectName("default_val")
        self.verticalLayout_3.addWidget(self.default_val)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.enum_label = QtGui.QLabel(machine)
        self.enum_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.enum_label.setObjectName("enum_label")
        self.verticalLayout_4.addWidget(self.enum_label)
        self.enum_list = QtGui.QLineEdit(machine)
        self.enum_list.setStyleSheet("QLineEdit:disabled {\n"
"    color:rgb(117, 117, 117);\n"
"    border: rgb(100, 100, 100);\n"
"}\n"
"QLineEdit:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"    border: rgb(220, 220, 220);\n"
"}")
        self.enum_list.setObjectName("enum_list")
        self.verticalLayout_4.addWidget(self.enum_list)
        self.verticalLayout_6.addLayout(self.verticalLayout_4)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.out_attr_label = QtGui.QLabel(machine)
        self.out_attr_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.out_attr_label.setObjectName("out_attr_label")
        self.horizontalLayout_4.addWidget(self.out_attr_label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.in_attr_label = QtGui.QLabel(machine)
        self.in_attr_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.in_attr_label.setObjectName("in_attr_label")
        self.horizontalLayout_4.addWidget(self.in_attr_label)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.out_attrs = QtGui.QComboBox(machine)
        self.out_attrs.setStyleSheet("QComboBox:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QComboBox:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.out_attrs.setObjectName("out_attrs")
        self.horizontalLayout_2.addWidget(self.out_attrs)
        self.ConnectionLine = QtGui.QFrame(machine)
        self.ConnectionLine.setMaximumSize(QtCore.QSize(150, 16777215))
        self.ConnectionLine.setFrameShadow(QtGui.QFrame.Raised)
        self.ConnectionLine.setLineWidth(4)
        self.ConnectionLine.setObjectName("ConnectionLine")
        self.horizontalLayout_2.addWidget(self.ConnectionLine)
        self.in_attrs = QtGui.QComboBox(machine)
        self.in_attrs.setStyleSheet("QComboBox:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QComboBox:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.in_attrs.setObjectName("in_attrs")
        self.horizontalLayout_2.addWidget(self.in_attrs)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.value_label = QtGui.QLabel(machine)
        self.value_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.value_label.setObjectName("value_label")
        self.verticalLayout_6.addWidget(self.value_label)
        self.values = QtGui.QPlainTextEdit(machine)
        self.values.setStyleSheet("QPlainTextEdit:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QPlainTextEdit:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.values.setFrameShape(QtGui.QFrame.Box)
        self.values.setLineWidth(2)
        self.values.setDocumentTitle("")
        self.values.setPlainText("")
        self.values.setObjectName("values")
        self.verticalLayout_6.addWidget(self.values)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.dont_do_it = QtGui.QPushButton(machine)
        self.dont_do_it.setObjectName("dont_do_it")
        self.horizontalLayout_3.addWidget(self.dont_do_it)
        self.do_it = QtGui.QPushButton(machine)
        self.do_it.setObjectName("do_it")
        self.horizontalLayout_3.addWidget(self.do_it)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.retranslateUi(machine)
        QtCore.QMetaObject.connectSlotsByName(machine)

    def retranslateUi(self, machine):
        machine.setWindowTitle(QtGui.QApplication.translate("machine", "Attribute Machine", None))
        self.Title.setText(QtGui.QApplication.translate("machine", "Attribute Machine", None))
        self.Descriptor.setText(QtGui.QApplication.translate("machine", "Works on Parent -> Child selection set where necessary.", None))
        self.modes_group.setTitle(QtGui.QApplication.translate("machine", "Modes", None))
        self.add_mode.setText(QtGui.QApplication.translate("machine", "Add", None))
        self.set_mode.setText(QtGui.QApplication.translate("machine", "Set", None))
        self.connect_mode.setText(QtGui.QApplication.translate("machine", "Connect", None))
        self.command_mode.setText(QtGui.QApplication.translate("machine", "Command", None))
        self.attr_type.setTitle(QtGui.QApplication.translate("machine", "Attribute Type", None))
        self.vector_btn.setText(QtGui.QApplication.translate("machine", "Vector", None))
        self.int_btn.setText(QtGui.QApplication.translate("machine", "Integer", None))
        self.string_btn.setText(QtGui.QApplication.translate("machine", "String", None))
        self.float_btn.setText(QtGui.QApplication.translate("machine", "Float", None))
        self.bool_btn.setText(QtGui.QApplication.translate("machine", "Boolean", None))
        self.enum_btn.setText(QtGui.QApplication.translate("machine", "Enum", None))
        self.min_val_label.setText(QtGui.QApplication.translate("machine", "Min", None))
        self.min_val.setText(QtGui.QApplication.translate("machine", "0", None))
        self.max_val_label.setText(QtGui.QApplication.translate("machine", "Max", None))
        self.max_val.setText(QtGui.QApplication.translate("machine", "1", None))
        self.default_val_label.setText(QtGui.QApplication.translate("machine", "Default", None))
        self.default_val.setText(QtGui.QApplication.translate("machine", "0", None))
        self.enum_label.setText(QtGui.QApplication.translate("machine", "Enum List (Colon Delineated : )", None))
        self.enum_list.setText(QtGui.QApplication.translate("machine", "Hi:Low", None))
        self.out_attr_label.setText(QtGui.QApplication.translate("machine", "Out Attribute List", None))
        self.in_attr_label.setText(QtGui.QApplication.translate("machine", "In Attribute List", None))
        self.value_label.setText(QtGui.QApplication.translate("machine", "Values To Apply", None))
        self.dont_do_it.setText(QtGui.QApplication.translate("machine", "Done", None))
        self.do_it.setText(QtGui.QApplication.translate("machine", "Do It", None))

