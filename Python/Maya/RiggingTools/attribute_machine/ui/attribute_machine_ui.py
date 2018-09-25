# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\sleep\OneDrive\Documents\Scripts\Python\Maya\RiggingTools\attribute_machine\ui\attribute_machine_ui.ui'
#
# Created: Tue Sep 25 13:48:25 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!
try:
    from PySide import QtCore, QtGui
    from shiboken import wrapInstance
    from pysideuic import compileUi
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
    from pyside2uic import compileUi

import sys

if 'pyside2uic' in sys.modules:
    qtGUI = QtWidgets
elif 'pysideuic' in sys.modules:
    qtGUI = QtGui
else:
    qtGUI = None
    print 'FUCK!!!'


class Ui_machine(object):
    def setupUi(self, machine):
        machine.setObjectName("machine")
        machine.setWindowModality(QtCore.Qt.WindowModal)
        machine.resize(537, 729)
        machine.setMinimumSize(QtCore.QSize(537, 729))
        machine.setStyleSheet("background-color: rgb(73, 73, 73);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout_6 = qtGUI.QVBoxLayout(machine)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.Title = qtGUI.QLabel(machine)
        self.Title.setStyleSheet("font: 75 22pt \"BankGothic\";")
        self.Title.setObjectName("Title")
        self.verticalLayout_6.addWidget(self.Title)
        self.Descriptor = qtGUI.QLabel(machine)
        self.Descriptor.setObjectName("Descriptor")
        self.verticalLayout_6.addWidget(self.Descriptor)
        self.modes_group = qtGUI.QGroupBox(machine)
        self.modes_group.setMinimumSize(QtCore.QSize(0, 75))
        self.modes_group.setStyleSheet("background-color: rgb(73, 73, 73);\n"
"color: rgb(230, 230, 230);")
        self.modes_group.setObjectName("modes_group")
        self.layoutWidget = qtGUI.QWidget(self.modes_group)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 491, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setStyleSheet("background-color: rgb(73, 73, 73);\n"
"color: rgb(230, 230, 230);")
        self.horizontalLayout = qtGUI.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_mode = qtGUI.QRadioButton(self.layoutWidget)
        self.add_mode.setChecked(True)
        self.add_mode.setObjectName("add_mode")
        self.horizontalLayout.addWidget(self.add_mode)
        self.set_mode = qtGUI.QRadioButton(self.layoutWidget)
        self.set_mode.setObjectName("set_mode")
        self.horizontalLayout.addWidget(self.set_mode)
        self.connect_mode = qtGUI.QRadioButton(self.layoutWidget)
        self.connect_mode.setObjectName("connect_mode")
        self.horizontalLayout.addWidget(self.connect_mode)
        self.command_mode = qtGUI.QRadioButton(self.layoutWidget)
        self.command_mode.setObjectName("command_mode")
        self.horizontalLayout.addWidget(self.command_mode)
        self.python_mode = qtGUI.QRadioButton(self.layoutWidget)
        self.python_mode.setObjectName("python_mode")
        self.horizontalLayout.addWidget(self.python_mode)
        self.verticalLayout_6.addWidget(self.modes_group)
        self.attr_type = qtGUI.QGroupBox(machine)
        self.attr_type.setMinimumSize(QtCore.QSize(0, 100))
        self.attr_type.setStyleSheet("background-color: rgb(73, 73, 73);\n"
"color: rgb(230, 230, 230);\n"
"")
        self.attr_type.setObjectName("attr_type")
        self.layoutWidget1 = qtGUI.QWidget(self.attr_type)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 491, 65))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_5 = qtGUI.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_7 = qtGUI.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.vector_btn = qtGUI.QRadioButton(self.layoutWidget1)
        self.vector_btn.setStyleSheet("QRadioButton:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QRadioButton:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.vector_btn.setObjectName("vector_btn")
        self.horizontalLayout_7.addWidget(self.vector_btn)
        self.int_btn = qtGUI.QRadioButton(self.layoutWidget1)
        self.int_btn.setStyleSheet("QRadioButton:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QRadioButton:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.int_btn.setObjectName("int_btn")
        self.horizontalLayout_7.addWidget(self.int_btn)
        self.string_btn = qtGUI.QRadioButton(self.layoutWidget1)
        self.string_btn.setStyleSheet("QRadioButton:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QRadioButton:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.string_btn.setObjectName("string_btn")
        self.horizontalLayout_7.addWidget(self.string_btn)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = qtGUI.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.float_btn = qtGUI.QRadioButton(self.layoutWidget1)
        self.float_btn.setStyleSheet("QRadioButton:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QRadioButton:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.float_btn.setObjectName("float_btn")
        self.horizontalLayout_6.addWidget(self.float_btn)
        self.bool_btn = qtGUI.QRadioButton(self.layoutWidget1)
        self.bool_btn.setStyleSheet("QRadioButton:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QRadioButton:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.bool_btn.setObjectName("bool_btn")
        self.horizontalLayout_6.addWidget(self.bool_btn)
        self.enum_btn = qtGUI.QRadioButton(self.layoutWidget1)
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
        self.horizontalLayout_8 = qtGUI.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.keyable = qtGUI.QCheckBox(machine)
        self.keyable.setStyleSheet("QCheckBox:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QCheckBox:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.keyable.setChecked(True)
        self.keyable.setObjectName("keyable")
        self.horizontalLayout_8.addWidget(self.keyable)
        self.hidden = qtGUI.QCheckBox(machine)
        self.hidden.setStyleSheet("QCheckBox:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QCheckBox:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.hidden.setObjectName("hidden")
        self.horizontalLayout_8.addWidget(self.hidden)
        spacerItem = qtGUI.QSpacerItem(40, 20, qtGUI.QSizePolicy.Expanding, qtGUI.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.verticalLayout_6.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_5 = qtGUI.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout = qtGUI.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.min_val_label = qtGUI.QLabel(machine)
        self.min_val_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.min_val_label.setObjectName("min_val_label")
        self.verticalLayout.addWidget(self.min_val_label)
        self.min_val = qtGUI.QLineEdit(machine)
        self.min_val.setEnabled(True)
        self.min_val.setStyleSheet("QLineEdit:disabled {\n"
"    color:rgb(117, 117, 117);\n"
"    border: rgb(100, 100, 100);\nbackground-color: rgb(100, 100, 100);\n"
"}\n"
"QLineEdit:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"    border: rgb(220, 220, 220);\nbackground-color: rgb(100, 100, 100);\n"
"}")
        self.min_val.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.min_val.setObjectName("min_val")
        self.verticalLayout.addWidget(self.min_val)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.verticalLayout_2 = qtGUI.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.max_val_label = qtGUI.QLabel(machine)
        self.max_val_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.max_val_label.setObjectName("max_val_label")
        self.verticalLayout_2.addWidget(self.max_val_label)
        self.max_val = qtGUI.QLineEdit(machine)
        self.max_val.setStyleSheet("QLineEdit:disabled {\n"
"    color:rgb(117, 117, 117);\n"
"    border: rgb(100, 100, 100);\nbackground-color: rgb(100, 100, 100);\n"
"}\n"
"QLineEdit:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"    border: rgb(220, 220, 220);\nbackground-color: rgb(100, 100, 100);\n"
"}")
        self.max_val.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.max_val.setObjectName("max_val")
        self.verticalLayout_2.addWidget(self.max_val)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = qtGUI.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.default_val_label = qtGUI.QLabel(machine)
        self.default_val_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.default_val_label.setObjectName("default_val_label")
        self.verticalLayout_3.addWidget(self.default_val_label)
        self.default_val = qtGUI.QLineEdit(machine)
        self.default_val.setStyleSheet("QLineEdit:disabled {\n"
"    color:rgb(117, 117, 117);\n"
"    border: rgb(100, 100, 100);\nbackground-color: rgb(100, 100, 100);\n"
"}\n"
"QLineEdit:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"    border: rgb(220, 220, 220);\nbackground-color: rgb(100, 100, 100);\n"
"}")
        self.default_val.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.default_val.setObjectName("default_val")
        self.verticalLayout_3.addWidget(self.default_val)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.verticalLayout_4 = qtGUI.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.enum_label = qtGUI.QLabel(machine)
        self.enum_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.enum_label.setObjectName("enum_label")
        self.verticalLayout_4.addWidget(self.enum_label)
        self.enum_list = qtGUI.QLineEdit(machine)
        self.enum_list.setStyleSheet("QLineEdit:disabled {\n"
"    color:rgb(117, 117, 117);\n"
"    border: rgb(100, 100, 100);\nbackground-color: rgb(100, 100, 100);\n"
"}\n"
"QLineEdit:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"    border: rgb(220, 220, 220);\nbackground-color: rgb(100, 100, 100);\n"
"}")
        self.enum_list.setObjectName("enum_list")
        self.verticalLayout_4.addWidget(self.enum_list)
        self.verticalLayout_6.addLayout(self.verticalLayout_4)
        self.horizontalLayout_4 = qtGUI.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.out_attr_label = qtGUI.QLabel(machine)
        self.out_attr_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.out_attr_label.setObjectName("out_attr_label")
        self.horizontalLayout_4.addWidget(self.out_attr_label)
        spacerItem1 = qtGUI.QSpacerItem(40, 20, qtGUI.QSizePolicy.Expanding, qtGUI.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.in_attr_label = qtGUI.QLabel(machine)
        self.in_attr_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.in_attr_label.setObjectName("in_attr_label")
        self.horizontalLayout_4.addWidget(self.in_attr_label)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_2 = qtGUI.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.out_attrs = qtGUI.QComboBox(machine)
        self.out_attrs.setStyleSheet("QComboBox:disabled {\n"
"    color: rgb(117, 117, 177);\nbackground-color: rgb(100, 100, 100);\n"
"}\n"
"QComboBox:enabled {\n"
"    color: rgb(255, 255, 255);\nbackground-color: rgb(100, 100, 100);"
"}")
        self.out_attrs.setObjectName("out_attrs")
        self.horizontalLayout_2.addWidget(self.out_attrs)
        self.ConnectionLine = qtGUI.QFrame(machine)
        self.ConnectionLine.setMaximumSize(QtCore.QSize(150, 16777215))
        self.ConnectionLine.setFrameShadow(qtGUI.QFrame.Raised)
        self.ConnectionLine.setLineWidth(4)
        self.ConnectionLine.setObjectName("ConnectionLine")
        self.horizontalLayout_2.addWidget(self.ConnectionLine)
        self.in_attrs = qtGUI.QComboBox(machine)
        self.in_attrs.setStyleSheet("QComboBox:disabled {\n"
"    color: rgb(117, 117, 177);\nbackground-color: rgb(100, 100, 100);\n"
"}\n"
"QComboBox:enabled {\n"
"    color: rgb(255, 255, 255);\nbackground-color: rgb(100, 100, 100);\n"
"}")
        self.in_attrs.setObjectName("in_attrs")
        self.horizontalLayout_2.addWidget(self.in_attrs)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.value_label = qtGUI.QLabel(machine)
        self.value_label.setStyleSheet("QLabel:disabled {\n"
"    color: rgb(117, 117, 177);\n"
"}\n"
"QLabel:enabled {\n"
"    color: rgb(255, 255, 255);\n"
"}")
        self.value_label.setObjectName("value_label")
        self.verticalLayout_6.addWidget(self.value_label)
        self.values = qtGUI.QPlainTextEdit(machine)
        self.values.setStyleSheet("QPlainTextEdit:disabled {\n"
"    color: rgb(117, 117, 177);\nbackground-color: rgb(100, 100, 100);\n"
"}\n"
"QPlainTextEdit:enabled {\n"
"    color: rgb(255, 255, 255);\nbackground-color: rgb(100, 100, 100);\n"
"}")
        self.values.setFrameShape(qtGUI.QFrame.Box)
        self.values.setLineWidth(2)
        self.values.setDocumentTitle("")
        self.values.setPlainText("")
        self.values.setObjectName("values")
        self.verticalLayout_6.addWidget(self.values)
        self.horizontalLayout_3 = qtGUI.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = qtGUI.QSpacerItem(40, 20, qtGUI.QSizePolicy.Expanding, qtGUI.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.dont_do_it = qtGUI.QPushButton(machine)
        self.dont_do_it.setObjectName("dont_do_it")
        self.horizontalLayout_3.addWidget(self.dont_do_it)
        self.do_it = qtGUI.QPushButton(machine)
        self.do_it.setObjectName("do_it")
        self.horizontalLayout_3.addWidget(self.do_it)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.retranslateUi(machine)
        QtCore.QMetaObject.connectSlotsByName(machine)

    def retranslateUi(self, machine):
        machine.setWindowTitle(qtGUI.QApplication.translate("machine", "Attribute Machine", None))
        self.Title.setText(qtGUI.QApplication.translate("machine", "Attribute Machine", None))
        self.Descriptor.setText(qtGUI.QApplication.translate("machine", "Add, Set, Connect and Script Attributes en "
                                                                        "masse.\nWorks on Parent -> Child selection "
                                                                        "set where necessary.", None))
        self.python_mode.setText(qtGUI.QApplication.translate("machine", "Python Loop"))
        self.modes_group.setTitle(qtGUI.QApplication.translate("machine", "Modes", None))
        self.add_mode.setText(qtGUI.QApplication.translate("machine", "Add", None))
        self.set_mode.setText(qtGUI.QApplication.translate("machine", "Set", None))
        self.connect_mode.setText(qtGUI.QApplication.translate("machine", "Connect", None))
        self.command_mode.setText(qtGUI.QApplication.translate("machine", "Expression", None))
        self.attr_type.setTitle(qtGUI.QApplication.translate("machine", "Attribute Type", None))
        self.vector_btn.setText(qtGUI.QApplication.translate("machine", "Vector", None))
        self.int_btn.setText(qtGUI.QApplication.translate("machine", "Integer", None))
        self.string_btn.setText(qtGUI.QApplication.translate("machine", "String", None))
        self.float_btn.setText(qtGUI.QApplication.translate("machine", "Float", None))
        self.bool_btn.setText(qtGUI.QApplication.translate("machine", "Boolean", None))
        self.enum_btn.setText(qtGUI.QApplication.translate("machine", "Enum", None))
        self.keyable.setText(qtGUI.QApplication.translate("machine", "Keyable", None))
        self.hidden.setText(qtGUI.QApplication.translate("machine", "Hidden", None))
        self.min_val_label.setText(qtGUI.QApplication.translate("machine", "Min", None))
        self.min_val.setText(qtGUI.QApplication.translate("machine", "0", None))
        self.max_val_label.setText(qtGUI.QApplication.translate("machine", "Max", None))
        self.max_val.setText(qtGUI.QApplication.translate("machine", "1", None))
        self.default_val_label.setText(qtGUI.QApplication.translate("machine", "Default", None))
        self.default_val.setText(qtGUI.QApplication.translate("machine", "0", None))
        self.enum_label.setText(qtGUI.QApplication.translate("machine", "Enum List (Colon Delineated : )", None))
        self.enum_list.setText(qtGUI.QApplication.translate("machine", "Hi:Low", None))
        self.out_attr_label.setText(qtGUI.QApplication.translate("machine", "Out Attribute List", None))
        self.in_attr_label.setText(qtGUI.QApplication.translate("machine", "In Attribute List", None))
        self.value_label.setText(qtGUI.QApplication.translate("machine", "Values To Apply", None))
        self.dont_do_it.setText(qtGUI.QApplication.translate("machine", "Done", None))
        self.do_it.setText(qtGUI.QApplication.translate("machine", "Do It", None))

