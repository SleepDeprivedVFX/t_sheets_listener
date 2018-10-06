# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\sleep\OneDrive\Documents\Scripts\Python\Maya\RiggingTools\switch_witch\ui\switch_witch_ui.ui'
#
# Created: Sat Oct 06 00:47:36 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

try:
    from PySide import QtCore, QtGui
except:
    from PySide2 import QtCore, QtGui, QtWidgets

import sys
if 'PySide' in sys.modules:
    qtGUI = QtGui
elif 'PySide2' in sys.modules:
    qtGUI = QtWidgets
else:
    qtGUI = None
    print 'FUCK!!!'

class Ui_switchwitch(object):
    def setupUi(self, switchwitch):
        switchwitch.setObjectName("switchwitch")
        switchwitch.resize(316, 355)
        switchwitch.setStyleSheet("background-color: rgb(100, 100, 100);\n"
"color: rgb(230, 230, 230);")
        self.verticalLayout_6 = qtGUI.QVBoxLayout(switchwitch)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.title_card = qtGUI.QLabel(switchwitch)
        self.title_card.setStyleSheet("font: 75 18pt \"MS Shell Dlg 2\";")
        self.title_card.setObjectName("title_card")
        self.verticalLayout_6.addWidget(self.title_card)
        self.verticalLayout_5 = qtGUI.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.driver_object_name = qtGUI.QLabel(switchwitch)
        self.driver_object_name.setObjectName("driver_object_name")
        self.verticalLayout_5.addWidget(self.driver_object_name)
        self.select_controller = qtGUI.QPushButton(switchwitch)
        self.select_controller.setObjectName("select_controller")
        self.verticalLayout_5.addWidget(self.select_controller)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = qtGUI.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.switch_attr_labels = qtGUI.QLabel(switchwitch)
        self.switch_attr_labels.setObjectName("switch_attr_labels")
        self.verticalLayout_4.addWidget(self.switch_attr_labels)
        self.switch_attributes = qtGUI.QComboBox(switchwitch)
        self.switch_attributes.setObjectName("switch_attributes")
        self.verticalLayout_4.addWidget(self.switch_attributes)
        self.verticalLayout_6.addLayout(self.verticalLayout_4)
        self.horizontalLayout = qtGUI.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = qtGUI.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tag_1_select = qtGUI.QRadioButton(switchwitch)
        self.tag_1_select.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tag_1_select.setCheckable(True)
        self.tag_1_select.setObjectName("tag_1_select")
        self.verticalLayout_3.addWidget(self.tag_1_select)
        self.tag_1 = qtGUI.QLineEdit(switchwitch)
        self.tag_1.setObjectName("tag_1")
        self.verticalLayout_3.addWidget(self.tag_1)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = qtGUI.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tag_2_select = qtGUI.QRadioButton(switchwitch)
        self.tag_2_select.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tag_2_select.setObjectName("tag_2_select")
        self.verticalLayout_2.addWidget(self.tag_2_select)
        self.tag_2 = qtGUI.QLineEdit(switchwitch)
        self.tag_2.setObjectName("tag_2")
        self.verticalLayout_2.addWidget(self.tag_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = qtGUI.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tag_3_select = qtGUI.QRadioButton(switchwitch)
        self.tag_3_select.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.tag_3_select.setObjectName("tag_3_select")
        self.verticalLayout.addWidget(self.tag_3_select)
        self.tag_3 = qtGUI.QLineEdit(switchwitch)
        self.tag_3.setObjectName("tag_3")
        self.verticalLayout.addWidget(self.tag_3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = qtGUI.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.create_new = qtGUI.QRadioButton(switchwitch)
        self.create_new.setObjectName("create_new")
        self.horizontalLayout_2.addWidget(self.create_new)
        self.use_existing = qtGUI.QRadioButton(switchwitch)
        self.use_existing.setChecked(True)
        self.use_existing.setObjectName("use_existing")
        self.horizontalLayout_2.addWidget(self.use_existing)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = qtGUI.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = qtGUI.QSpacerItem(40, 20, qtGUI.QSizePolicy.Expanding, qtGUI.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.done = qtGUI.QPushButton(switchwitch)
        self.done.setObjectName("done")
        self.horizontalLayout_3.addWidget(self.done)
        self.build = qtGUI.QPushButton(switchwitch)
        self.build.setObjectName("build")
        self.horizontalLayout_3.addWidget(self.build)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.retranslateUi(switchwitch)
        QtCore.QMetaObject.connectSlotsByName(switchwitch)

    def retranslateUi(self, switchwitch):
        switchwitch.setWindowTitle(qtGUI.QApplication.translate("switchwitch", "Switch Witch", None))
        self.title_card.setText(qtGUI.QApplication.translate("switchwitch", "Switch Witch", None))
        self.driver_object_name.setToolTip(qtGUI.QApplication.translate("switchwitch", "Select the object that has the FK-IK Switch Slider", None))
        self.driver_object_name.setText(qtGUI.QApplication.translate("switchwitch", "No Selection", None))
        self.select_controller.setToolTip(qtGUI.QApplication.translate("switchwitch", "Select the object that has the FK-IK Switch Slider", None))
        self.select_controller.setText(qtGUI.QApplication.translate("switchwitch", "Select Controller", None))
        self.switch_attr_labels.setToolTip(qtGUI.QApplication.translate("switchwitch", "Select the Slider Attribute that will control the FK-IK Switch", None))
        self.switch_attr_labels.setText(qtGUI.QApplication.translate("switchwitch", "Control Attribute", None))
        self.switch_attributes.setToolTip(qtGUI.QApplication.translate("switchwitch", "Select the Slider Attribute that will control the FK-IK Switch", None))
        self.tag_1_select.setToolTip(qtGUI.QApplication.translate("switchwitch", "Select Tag as Master", None))
        self.tag_1_select.setText(qtGUI.QApplication.translate("switchwitch", "Tag 1", None))
        self.tag_1.setToolTip(qtGUI.QApplication.translate("switchwitch", "Set Tag value. Ex: arm_joint_[tag]", None))
        self.tag_1.setText(qtGUI.QApplication.translate("switchwitch", "IK", None))
        self.tag_2_select.setToolTip(qtGUI.QApplication.translate("switchwitch", "Select Tag as Master", None))
        self.tag_2_select.setText(qtGUI.QApplication.translate("switchwitch", "Tag 2", None))
        self.tag_2.setToolTip(qtGUI.QApplication.translate("switchwitch", "Set Tag value. Ex: arm_joint_[tag]", None))
        self.tag_2.setText(qtGUI.QApplication.translate("switchwitch", "FK", None))
        self.tag_3_select.setToolTip(qtGUI.QApplication.translate("switchwitch", "Select Tag as Master", None))
        self.tag_3_select.setText(qtGUI.QApplication.translate("switchwitch", "Tag 3", None))
        self.tag_3.setToolTip(qtGUI.QApplication.translate("switchwitch", "Set Tag value. Ex: arm_joint_[tag]", None))
        self.tag_3.setText(qtGUI.QApplication.translate("switchwitch", "BND", None))
        self.create_new.setToolTip(qtGUI.QApplication.translate("switchwitch", "Create a new matching joint chain", None))
        self.create_new.setText(qtGUI.QApplication.translate("switchwitch", "Create New Joints", None))
        self.use_existing.setToolTip(qtGUI.QApplication.translate("switchwitch", "Use existing joints", None))
        self.use_existing.setText(qtGUI.QApplication.translate("switchwitch", "Use Existing", None))
        self.done.setText(qtGUI.QApplication.translate("switchwitch", "Done", None))
        self.build.setText(qtGUI.QApplication.translate("switchwitch", "Build Switches", None))

