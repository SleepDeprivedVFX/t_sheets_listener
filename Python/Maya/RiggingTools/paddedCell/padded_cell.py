# Padded Cell
# Object Padding Utility .
# Create various kinds of complex padding for joints, controllers, or any other organizational thing that nees padding.

try:
    from PySide import QtCore, QtGui
    from shiboken import wrapInstance
    from pysideuic import compileUi
except:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance
    from pyside2uic import compileUi

import sys

from functools import partial
from maya import cmds
from maya import mel

if 'pyside2uic' in sys.modules:
    qtGUI = QtWidgets
elif 'pysideuic' in sys.modules:
    qtGUI = QtGui
else:
    qtGUI = None

__author__ = 'Adam Benson'
__version__ = '1.0.0'


class padded_cell(qtGUI.QWidget):
    def __init__(self, parent=None):
        super(padded_cell, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui = Ui_paddedCellForm()
        self.ui.setupUi(self)
        self.prep_ui()

    # --------------------------------------------------------------------------------------------------------------
    # Prep
    # --------------------------------------------------------------------------------------------------------------

    def prep_ui(self):
        print 'Running...'
        self.ui.reset_btn.clicked.connect(self.reset)
        self.ui.build_btn.clicked.connect(self.build)
        self.ui.cancel_btn.clicked.connect(self.cancel)
        self.ui.Build_Padding.clicked.connect(partial(self.mode, set_mode='build'))
        self.ui.AddAPad_GRP.clicked.connect(partial(self.mode, set_mode='add'))
        self.ui.PatchAPad_GRP.clicked.connect(partial(self.mode, set_mode='patch'))
        self.ui.match_child.clicked.connect(partial(self.patch_mode, set_mode='child'))
        self.ui.match_parent.clicked.connect(partial(self.patch_mode, set_mode='parent'))
        self.reset()

    def reset(self):
        print 'Reset...'
        current_selection = cmds.ls(sl=True)
        offset = self.ui.offset_name.text()
        pad = self.ui.pad_name.text()
        addapad = self.ui.addapad_name.text()
        if current_selection:
            new_offset = '%s_%s' % (current_selection[0], offset)
            new_pad = '%s_%s' % (current_selection[0], pad)
            if offset in current_selection[0]:
                new_addapad = current_selection[0].replace(offset, addapad)
            elif pad in current_selection[0]:
                new_addapad = current_selection[0].replace(pad, addapad)
            else:
                new_addapad = '%s_%s' % (current_selection[0], addapad)
            self.ui.addapad_output.setText(new_addapad)
            self.ui.new_offset_name.setText(new_offset)
            self.ui.new_pad_name.setText(new_pad)

    def build(self):
        print 'Build this...'
        build = self.ui.Build_Padding.isChecked()
        add = self.ui.AddAPad_GRP.isChecked()
        patch = self.ui.PatchAPad_GRP.isChecked()

        if build:
            self.prep_build()
        elif add:
            self.prep_add()
        elif patch:
            self.prep_patch()

    def cancel(self):
        print 'Cancelling...'
        self.close()

    def prep_build(self):
        print 'Prepping Build...'
        objs = cmds.ls(sl=True)
        if not objs:
            return False

        for obj in objs:
            cmds.select(obj, r=True)
            p = self.ui.pad_name.text()
            o = self.ui.offset_name.text()
            self.buildGroupPadding(p=p, o=o)

    def prep_add(self):
        print 'Prepping Add...'
        objs = cmds.ls(sl=True)
        if not objs:
            return False

        for obj in objs:
            cmds.select(obj, r=True)
            a = self.ui.addapad_name.text()
            p = self.ui.pad_name.text()
            o = self.ui.offset_name.text()
            self.addapad(a=a, o=o, p=p)

    def prep_patch(self):
        print 'Prepping Patch---'

    def patch_mode(self, set_mode=None):
        child = self.ui.match_child.isChecked()
        parent = self.ui.match_parent.isChecked()
        if set_mode == 'child' and child:
            self.ui.match_parent.setChecked(False)
        elif set_mode == 'parent' and parent:
            self.ui.match_child.setChecked(False)

    def mode(self, set_mode=None):
        build = self.ui.Build_Padding.isChecked()
        add = self.ui.AddAPad_GRP.isChecked()
        patch = self.ui.PatchAPad_GRP.isChecked()
        if set_mode == 'build' and build:
            print 'build mode'
            self.ui.AddAPad_GRP.setChecked(False)
            self.ui.PatchAPad_GRP.setChecked(False)
        elif set_mode == 'add' and add:
            print 'add mode'
            self.ui.Build_Padding.setChecked(False)
            self.ui.PatchAPad_GRP.setChecked(False)
        elif set_mode == 'patch' and patch:
            print 'patch mode'
            self.ui.Build_Padding.setChecked(False)
            self.ui.AddAPad_GRP.setChecked(False)
        else:
            self.ui.Build_Padding.setChecked(False)
            self.ui.AddAPad_GRP.setChecked(False)
            self.ui.PatchAPad_GRP.setChecked(False)

    def buildGroupPadding(self, p=None, o=None):
        selected = cmds.ls(sl=True)

        if len(selected) > 1:
            cmds.confirmDialog(m='Only one object should be selected for this')
            return False
        elif not selected:
            cmds.confirmDialog(m='You must select an object to group-pad')
            return False
        else:
            this = selected[0]
        if cmds.nodeType(this) == 'joint':
            pivot = cmds.xform(this, q=True, t=True, ws=True)
            print pivot
        else:
            pivot = cmds.xform(this, q=True, rp=True, ws=True)
            print pivot
        pad = '%s_%s' % (this, p)
        offset = '%s_%s' % (this, o)
        cmds.group(n=pad)
        cmds.xform(rp=pivot)
        cmds.xform(sp=pivot)
        cmds.group(n=offset)
        cmds.xform(rp=pivot)
        cmds.xform(sp=pivot)

    def addapad(self, a=None, o=None, p=None):
        selected_pad = cmds.ls(sl=True)
        if len(selected_pad) > 1:
            cmds.confirmDialog(m='You must select only a single group pad')
            return False
        elif not selected_pad:
            cmds.confirmDialog(m='You must select a group pad')
        elif cmds.nodeType(selected_pad) != 'transform':
            cmds.confirmDialog(m='That ain\'t a group')
        else:
            this = selected_pad[0]

            pivot = cmds.xform(this, q=True, rp=True)
            if p in this:
                new_name = this.replace(p, a)
            elif o in this:
                new_name = this.replace(o, a)
            else:
                new_name = '%s_%s' % (this, a)
            cmds.group(n=new_name)
            cmds.xform(rp=pivot)
            cmds.xform(sp=pivot)


class Ui_paddedCellForm(object):
    def setupUi(self, paddedCellForm):
        paddedCellForm.setObjectName("paddedCellForm")
        paddedCellForm.setWindowModality(QtCore.Qt.NonModal)
        paddedCellForm.resize(1085, 545)
        paddedCellForm.setMinimumSize(QtCore.QSize(1085, 545))
        paddedCellForm.setWindowOpacity(1.0)
        paddedCellForm.setStyleSheet("background-color: qradialgradient(spread:pad, cx:0.525, cy:0.54, radius:0.886, fx:0.525, fy:0.534, stop:0.407563 rgba(0, 0, 0, 255), stop:1 rgba(198, 86, 0, 255));\n"
"border-color: rgba(0, 0, 0, 0);\n"
"selection-background-color: rgb(255, 106, 0);\n"
"selection-color: rgb(255, 106, 0);")
        self.verticalLayout_6 = qtGUI.QVBoxLayout(paddedCellForm)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_5 = qtGUI.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.column_1 = qtGUI.QFrame(paddedCellForm)
        sizePolicy = qtGUI.QSizePolicy(qtGUI.QSizePolicy.Maximum, qtGUI.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.column_1.sizePolicy().hasHeightForWidth())
        self.column_1.setSizePolicy(sizePolicy)
        self.column_1.setMaximumSize(QtCore.QSize(400, 16777215))
        self.column_1.setStyleSheet("font: 75 12pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.column_1.setObjectName("column_1")
        self.verticalLayout_5 = qtGUI.QVBoxLayout(self.column_1)
        self.verticalLayout_5.setSizeConstraint(qtGUI.QLayout.SetMinAndMaxSize)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.title = qtGUI.QLabel(self.column_1)
        self.title.setMinimumSize(QtCore.QSize(350, 60))
        self.title.setMaximumSize(QtCore.QSize(400, 16777215))
        self.title.setStyleSheet("font: 75 24pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.title.setObjectName("title")
        self.verticalLayout_5.addWidget(self.title)
        self.subtitle = qtGUI.QLabel(self.column_1)
        self.subtitle.setMaximumSize(QtCore.QSize(400, 45))
        self.subtitle.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.subtitle.setObjectName("subtitle")
        self.verticalLayout_5.addWidget(self.subtitle)
        self.Build_Padding = qtGUI.QGroupBox(self.column_1)
        self.Build_Padding.setMinimumSize(QtCore.QSize(491, 0))
        self.Build_Padding.setStyleSheet("font: 75 12pt \"Orbitron\";\n"
"border-color: rgb(255, 129, 2);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.Build_Padding.setCheckable(True)
        self.Build_Padding.setObjectName("Build_Padding")
        self.verticalLayout = qtGUI.QVBoxLayout(self.Build_Padding)
        self.verticalLayout.setContentsMargins(-1, 20, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.build_controls = qtGUI.QGroupBox(self.Build_Padding)
        self.build_controls.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);\n"
"border: rgb(198, 86, 0);")
        self.build_controls.setObjectName("build_controls")
        self.build_padding_layout = qtGUI.QGridLayout(self.build_controls)
        self.build_padding_layout.setObjectName("build_padding_layout")
        self.pad_diagram = qtGUI.QFrame(self.build_controls)
        sizePolicy = qtGUI.QSizePolicy(qtGUI.QSizePolicy.MinimumExpanding, qtGUI.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pad_diagram.sizePolicy().hasHeightForWidth())
        self.pad_diagram.setSizePolicy(sizePolicy)
        self.pad_diagram.setMinimumSize(QtCore.QSize(230, 145))
        self.pad_diagram.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"background-image: url(:/icons/folder_diagram.png);\n"
"background-repeat: none;")
        self.pad_diagram.setFrameShape(qtGUI.QFrame.StyledPanel)
        self.pad_diagram.setFrameShadow(qtGUI.QFrame.Raised)
        self.pad_diagram.setObjectName("pad_diagram")
        self.pad_label = qtGUI.QLabel(self.pad_diagram)
        self.pad_label.setGeometry(QtCore.QRect(50, 70, 43, 25))
        self.pad_label.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);\n"
"background-image: url(:/icons/spacer.png);")
        self.pad_label.setObjectName("pad_label")
        self.offset_label = qtGUI.QLabel(self.pad_diagram)
        self.offset_label.setGeometry(QtCore.QRect(30, 30, 69, 25))
        self.offset_label.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-image: url(:/icons/spacer.png);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.offset_label.setObjectName("offset_label")
        self.offset_name = qtGUI.QLineEdit(self.pad_diagram)
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
        self.your_object = qtGUI.QLabel(self.pad_diagram)
        self.your_object.setGeometry(QtCore.QRect(70, 110, 130, 25))
        self.your_object.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);\n"
"background-image: url(:/icons/spacer.png);")
        self.your_object.setObjectName("your_object")
        self.pad_name = qtGUI.QLineEdit(self.pad_diagram)
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
        spacerItem = qtGUI.QSpacerItem(20, 15, qtGUI.QSizePolicy.Minimum, qtGUI.QSizePolicy.Expanding)
        self.build_padding_layout.addItem(spacerItem, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.build_controls)
        self.build_output = qtGUI.QVBoxLayout()
        self.build_output.setObjectName("build_output")
        self.new_offset_layout = qtGUI.QHBoxLayout()
        self.new_offset_layout.setObjectName("new_offset_layout")
        self.new_offset_label = qtGUI.QLabel(self.Build_Padding)
        self.new_offset_label.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.new_offset_label.setObjectName("new_offset_label")
        self.new_offset_layout.addWidget(self.new_offset_label)
        self.new_offset_name = qtGUI.QLabel(self.Build_Padding)
        self.new_offset_name.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);\n"
"font-weight: bold;")
        self.new_offset_name.setObjectName("new_offset_name")
        self.new_offset_layout.addWidget(self.new_offset_name)
        spacerItem1 = qtGUI.QSpacerItem(40, 20, qtGUI.QSizePolicy.Expanding, qtGUI.QSizePolicy.Minimum)
        self.new_offset_layout.addItem(spacerItem1)
        self.build_output.addLayout(self.new_offset_layout)
        self.new_name_layout = qtGUI.QHBoxLayout()
        self.new_name_layout.setObjectName("new_name_layout")
        spacerItem2 = qtGUI.QSpacerItem(40, 20, qtGUI.QSizePolicy.Preferred, qtGUI.QSizePolicy.Minimum)
        self.new_name_layout.addItem(spacerItem2)
        self.new_pad_label = qtGUI.QLabel(self.Build_Padding)
        self.new_pad_label.setMaximumSize(QtCore.QSize(150, 16777215))
        self.new_pad_label.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.new_pad_label.setObjectName("new_pad_label")
        self.new_name_layout.addWidget(self.new_pad_label)
        self.new_pad_name = qtGUI.QLabel(self.Build_Padding)
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
        self.column_2 = qtGUI.QFrame(paddedCellForm)
        self.column_2.setStyleSheet("font: 75 12pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.column_2.setObjectName("column_2")
        self.verticalLayout_4 = qtGUI.QVBoxLayout(self.column_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.AddAPad_GRP = qtGUI.QGroupBox(self.column_2)
        self.AddAPad_GRP.setStyleSheet("font: 75 12pt \"Orbitron\";\n"
"border-color: rgb(255, 129, 2);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.AddAPad_GRP.setCheckable(True)
        self.AddAPad_GRP.setChecked(False)
        self.AddAPad_GRP.setObjectName("AddAPad_GRP")
        self.widget = qtGUI.QWidget(self.AddAPad_GRP)
        self.widget.setGeometry(QtCore.QRect(10, 50, 497, 131))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = qtGUI.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.addapad_ = qtGUI.QLabel(self.widget)
        self.addapad_.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.addapad_.setWordWrap(True)
        self.addapad_.setObjectName("addapad_")
        self.verticalLayout_2.addWidget(self.addapad_)
        self.horizontalLayout = qtGUI.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.suffix_name = qtGUI.QLabel(self.widget)
        self.suffix_name.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.suffix_name.setObjectName("suffix_name")
        self.horizontalLayout.addWidget(self.suffix_name)
        self.addapad_name = qtGUI.QLineEdit(self.widget)
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
        self.horizontalLayout_2 = qtGUI.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = qtGUI.QSpacerItem(40, 20, qtGUI.QSizePolicy.Expanding, qtGUI.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.addapad_out_label = qtGUI.QLabel(self.widget)
        self.addapad_out_label.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.addapad_out_label.setObjectName("addapad_out_label")
        self.horizontalLayout_2.addWidget(self.addapad_out_label)
        self.addapad_output = qtGUI.QLabel(self.widget)
        self.addapad_output.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);\n"
"font-weight: bold;")
        self.addapad_output.setObjectName("addapad_output")
        self.horizontalLayout_2.addWidget(self.addapad_output)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addWidget(self.AddAPad_GRP)
        self.PatchAPad_GRP = qtGUI.QGroupBox(self.column_2)
        self.PatchAPad_GRP.setStyleSheet("font: 75 12pt \"Orbitron\";\n"
"border-color: rgb(255, 129, 2);\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.PatchAPad_GRP.setCheckable(True)
        self.PatchAPad_GRP.setChecked(False)
        self.PatchAPad_GRP.setObjectName("PatchAPad_GRP")
        self.widget1 = qtGUI.QWidget(self.PatchAPad_GRP)
        self.widget1.setGeometry(QtCore.QRect(10, 50, 508, 129))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_3 = qtGUI.QVBoxLayout(self.widget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.instructions = qtGUI.QLabel(self.widget1)
        self.instructions.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.instructions.setObjectName("instructions")
        self.verticalLayout_3.addWidget(self.instructions)
        self.match_child = qtGUI.QCheckBox(self.widget1)
        self.match_child.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.match_child.setObjectName("match_child")
        self.verticalLayout_3.addWidget(self.match_child)
        self.match_parent = qtGUI.QCheckBox(self.widget1)
        self.match_parent.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.match_parent.setObjectName("match_parent")
        self.verticalLayout_3.addWidget(self.match_parent)
        self.freeze_trans = qtGUI.QCheckBox(self.widget1)
        self.freeze_trans.setStyleSheet("font: 75 10pt \"Orbitron\";\n"
"background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 129, 2);")
        self.freeze_trans.setObjectName("freeze_trans")
        self.verticalLayout_3.addWidget(self.freeze_trans)
        self.verticalLayout_4.addWidget(self.PatchAPad_GRP)
        self.horizontalLayout_5.addWidget(self.column_2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = qtGUI.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cancel_btn = qtGUI.QPushButton(paddedCellForm)
        self.cancel_btn.setStyleSheet("background-color: rgb(255, 106, 0);\n"
"font: 75 8pt \"Orbitron\";\n"
"color: rgb(0, 0, 0);\n"
"padding: 5px;")
        self.cancel_btn.setObjectName("cancel_btn")
        self.horizontalLayout_4.addWidget(self.cancel_btn)
        self.reset_btn = qtGUI.QPushButton(paddedCellForm)
        self.reset_btn.setStyleSheet("background-color: rgb(255, 106, 0);\n"
"font: 75 8pt \"Orbitron\";\n"
"color: rgb(0, 0, 0);\n"
"padding: 5px;")
        self.reset_btn.setObjectName("reset_btn")
        self.horizontalLayout_4.addWidget(self.reset_btn)
        self.build_btn = qtGUI.QPushButton(paddedCellForm)
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
        paddedCellForm.setWindowTitle(qtGUI.QApplication.translate("paddedCellForm", "Padded Cell", None))
        self.title.setText(qtGUI.QApplication.translate("paddedCellForm", "Padded Cell", None))
        self.subtitle.setText(qtGUI.QApplication.translate("paddedCellForm", "Fight hierarchy padding insanity", None))
        self.Build_Padding.setTitle(qtGUI.QApplication.translate("paddedCellForm", "Build Standard Group Pads", None))
        self.pad_label.setText(qtGUI.QApplication.translate("paddedCellForm", "Pad", None))
        self.offset_label.setText(qtGUI.QApplication.translate("paddedCellForm", "Offset", None))
        self.offset_name.setText(qtGUI.QApplication.translate("paddedCellForm", "OFF", None))
        self.your_object.setText(qtGUI.QApplication.translate("paddedCellForm", "Your Object", None))
        self.pad_name.setText(qtGUI.QApplication.translate("paddedCellForm", "PAD", None))
        self.new_offset_label.setText(qtGUI.QApplication.translate("paddedCellForm", "New Offset:", None))
        self.new_offset_name.setText(qtGUI.QApplication.translate("paddedCellForm", "your_object_OFF", None))
        self.new_pad_label.setText(qtGUI.QApplication.translate("paddedCellForm", "New Pad:", None))
        self.new_pad_name.setText(qtGUI.QApplication.translate("paddedCellForm", "your_object_PAD", None))
        self.AddAPad_GRP.setTitle(qtGUI.QApplication.translate("paddedCellForm", "Add-a-Pad", None))
        self.addapad_.setText(qtGUI.QApplication.translate("paddedCellForm", "Insert a pad above your currently selected object.", None))
        self.suffix_name.setText(qtGUI.QApplication.translate("paddedCellForm", "Suffix/Tag Name:", None))
        self.addapad_name.setText(qtGUI.QApplication.translate("paddedCellForm", "ANIM", None))
        self.addapad_out_label.setText(qtGUI.QApplication.translate("paddedCellForm", "New Pad:", None))
        self.addapad_output.setText(qtGUI.QApplication.translate("paddedCellForm", "your_object_ANIM", None))
        self.PatchAPad_GRP.setTitle(qtGUI.QApplication.translate("paddedCellForm", "Patch-a-Pad", None))
        self.instructions.setText(qtGUI.QApplication.translate("paddedCellForm", "Fix existing pad pivots and freeze translations", None))
        self.match_child.setText(qtGUI.QApplication.translate("paddedCellForm", "Match Pivot to Child", None))
        self.match_parent.setText(qtGUI.QApplication.translate("paddedCellForm", "Match Pivot to Parent", None))
        self.freeze_trans.setText(qtGUI.QApplication.translate("paddedCellForm", "Freeze Transforms", None))
        self.cancel_btn.setText(qtGUI.QApplication.translate("paddedCellForm", "Cancel\n"
"Close", None))
        self.reset_btn.setText(qtGUI.QApplication.translate("paddedCellForm", "Reset\n"
"Selection", None))
        self.build_btn.setText(qtGUI.QApplication.translate("paddedCellForm", "Build\n"
"Padding", None))

# import bgs_rc

run = padded_cell()
run.show()
