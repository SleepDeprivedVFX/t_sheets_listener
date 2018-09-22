from PySide import QtCore, QtGui
from maya import cmds
import sys
import os
sys.path.append(r'C:\Users\sleep\OneDrive\Documents\Scripts\Python\Maya\RiggingTools\attribute_machine')
from ui import attribute_machine_ui as amu
reload(amu)

class attr_mach_ui(QtGui.QWidget):
    """
    Attribute Machine UI.
    """
    def __init__(self, parent=None):
        # Preliminary things
        QtGui.QWidget.__init__(self, parent)
        self.ui = amu.Ui_machine()
        self.ui.setupUi(self)
        self.ui.do_it.clicked.connect(self.run_it)
        self.ui.dont_do_it.clicked.connect(self.close)
        self.ui.add_mode.clicked.connect(self.set_mode)
        self.ui.set_mode.clicked.connect(self.set_mode)
        self.ui.connect_mode.clicked.connect(self.set_mode)
        self.ui.command_mode.clicked.connect(self.set_mode)
        self.ui.vector_btn.clicked.connect(self.set_sub_modes)
        self.ui.float_btn.clicked.connect(self.set_sub_modes)
        self.ui.int_btn.clicked.connect(self.set_sub_modes)
        self.ui.bool_btn.clicked.connect(self.set_sub_modes)
        self.ui.enum_btn.clicked.connect(self.set_sub_modes)
        self.ui.string_btn.clicked.connect(self.set_sub_modes)
        self.disable_all()
        self.set_mode()

    def disable_all(self):
        self.ui.in_attrs.clear()
        self.ui.out_attrs.clear()
        self.ui.out_attrs.setEnabled(False)
        self.ui.in_attrs.setEnabled(False)
        self.ui.default_val.setEnabled(False)
        self.ui.min_val.setEnabled(False)
        self.ui.max_val.setEnabled(False)
        self.ui.bool_btn.setEnabled(False)
        self.ui.int_btn.setEnabled(False)
        self.ui.float_btn.setEnabled(False)
        self.ui.enum_btn.setEnabled(False)
        self.ui.enum_list.setEnabled(False)
        self.ui.string_btn.setEnabled(False)
        self.ui.vector_btn.setEnabled(False)
        self.ui.default_val.setEnabled(False)
        self.ui.min_val_label.setEnabled(False)
        self.ui.max_val_label.setEnabled(False)
        self.ui.default_val_label.setEnabled(False)
        self.ui.values.setEnabled(False)
        self.ui.value_label.setEnabled(False)
        self.ui.in_attr_label.setEnabled(False)
        self.ui.out_attr_label.setEnabled(False)


    def set_sub_modes(self):
        vector_btn = self.ui.vector_btn.isChecked()
        float_btn = self.ui.float_btn.isChecked()
        int_btn = self.ui.int_btn.isChecked()
        string_btn = self.ui.string_btn.isChecked()
        bool_btn = self.ui.bool_btn.isChecked()
        enum_btn = self.ui.enum_btn.isChecked()
        if float_btn:
            self.ui.enum_list.setEnabled(False)
            self.ui.enum_label.setEnabled(False)
            self.ui.min_val.setEnabled(True)
            self.ui.max_val.setEnabled(True)
            self.ui.default_val.setEnabled(True)
            self.ui.min_val_label.setEnabled(True)
            self.ui.max_val_label.setEnabled(True)
            self.ui.default_val_label.setEnabled(True)
            self.ui.value_label.setEnabled(True)
            self.ui.values.setEnabled(True)
        elif int_btn:
            self.ui.enum_list.setEnabled(False)
            self.ui.enum_label.setEnabled(False)
            self.ui.min_val.setEnabled(True)
            self.ui.max_val.setEnabled(True)
            self.ui.default_val.setEnabled(True)
            self.ui.min_val_label.setEnabled(True)
            self.ui.max_val_label.setEnabled(True)
            self.ui.default_val_label.setEnabled(True)
            self.ui.value_label.setEnabled(True)
            self.ui.values.setEnabled(True)
        elif enum_btn:
            self.ui.enum_list.setEnabled(True)
            self.ui.enum_label.setEnabled(True)
            self.ui.min_val.setEnabled(False)
            self.ui.max_val.setEnabled(False)
            self.ui.default_val.setEnabled(False)
            self.ui.min_val_label.setEnabled(False)
            self.ui.max_val_label.setEnabled(False)
            self.ui.default_val_label.setEnabled(False)
            self.ui.value_label.setEnabled(True)
            self.ui.values.setEnabled(True)
        else:
            self.ui.enum_list.setEnabled(False)
            self.ui.enum_label.setEnabled(False)
            self.ui.min_val.setEnabled(False)
            self.ui.max_val.setEnabled(False)
            self.ui.default_val.setEnabled(False)
            self.ui.min_val_label.setEnabled(False)
            self.ui.max_val_label.setEnabled(False)
            self.ui.default_val_label.setEnabled(False)
            self.ui.value_label.setEnabled(True)
            self.ui.values.setEnabled(True)


    def set_mode(self):
        add = self.ui.add_mode.isChecked()
        
        set = self.ui.set_mode.isChecked()
        connect = self.ui.connect_mode.isChecked()
        command = self.ui.command_mode.isChecked()
        if add:
            self.disable_all()
            selected = cmds.ls(sl=True)
            value = self.ui.values.toPlainText()
            self.ui.vector_btn.setEnabled(True)
            self.ui.float_btn.setEnabled(True)
            self.ui.float_btn.setChecked(True)
            self.ui.string_btn.setEnabled(True)
            self.ui.int_btn.setEnabled(True)
            self.ui.enum_btn.setEnabled(True)
            self.ui.bool_btn.setEnabled(True)
            self.set_sub_modes()

            if value:
                # Oh, shit!  Right!  The Add Attributes shit needs all sorts of variables set for it.
                # For instance.  Why kind of attribute?  Boolean? String? Enum?
                # Plus it will need a way to input all of those.
                pass

        elif set:
            self.disable_all()
            self.ui.values.setEnabled(True)
            self.ui.value_label.setEnabled(True)
            self.ui.in_attr_label.setEnabled(True)
            self.ui.in_attrs.setEnabled(True)
            selected = cmds.ls(sl=True)
            attrs = self.collect_attributes(selected=selected)
            value = self.ui.values.toPlainText()
            self.ui.vector_btn.setEnabled(True)
            self.ui.float_btn.setEnabled(True)
            self.ui.float_btn.setChecked(True)
            self.ui.string_btn.setEnabled(True)
            self.ui.int_btn.setEnabled(True)
            self.ui.enum_btn.setEnabled(True)
            self.ui.bool_btn.setEnabled(True)
            self.set_sub_modes()

        elif connect:
            pass
        elif command:
            pass

    def run_it(self):
        pass

    def collect_attributes(self, selected=None):
        collected_attributes = []
        for sel in selected:
            get_attr = cmds.listAttr(sel)
            for attr in get_attr:
                if attr not in collected_attributes:
                    collected_attributes.append(attr)
        return collected_attributes

if __name__ == '__main__':
    try:
        app = QtGui.QApplication(sys.argv)
        window = attr_mach_ui()
        window.show()
        sys.exit(app.exec_())
    except:
        app = QtGui.QApplication.instance()
        window = attr_mach_ui()
        window.show()

