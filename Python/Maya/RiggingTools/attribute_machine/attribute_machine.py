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

        self.func_running = True

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
        self.ui.keyable.setEnabled(False)
        self.ui.hidden.setEnabled(False)
        self.ui.parent_child.setEnabled(False)

    def set_sub_modes(self):
        vector_btn = self.ui.vector_btn.isChecked()
        float_btn = self.ui.float_btn.isChecked()
        int_btn = self.ui.int_btn.isChecked()
        string_btn = self.ui.string_btn.isChecked()
        bool_btn = self.ui.bool_btn.isChecked()
        enum_btn = self.ui.enum_btn.isChecked()
        if self.ui.add_mode.isChecked():
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
        selected = cmds.ls(sl=True)
        if add:
            self.disable_all()
            self.ui.vector_btn.setEnabled(True)
            self.ui.float_btn.setEnabled(True)
            self.ui.float_btn.setChecked(True)
            self.ui.string_btn.setEnabled(True)
            self.ui.int_btn.setEnabled(True)
            self.ui.enum_btn.setEnabled(True)
            self.ui.bool_btn.setEnabled(True)
            self.ui.hidden.setEnabled(True)
            self.ui.keyable.setEnabled(True)
            self.set_sub_modes()
            self.ui.value_label.setText('Attribute Name')
        elif set:
            self.disable_all()
            self.ui.values.setEnabled(True)
            self.ui.value_label.setEnabled(True)
            self.ui.in_attr_label.setEnabled(True)
            self.ui.in_attrs.setEnabled(True)
            attrs = self.collect_attributes(selected=selected)
            if attrs:
                for attr in attrs:
                    self.ui.in_attrs.addItem(attr)
            self.ui.vector_btn.setEnabled(True)
            self.ui.float_btn.setEnabled(True)
            self.ui.float_btn.setChecked(True)
            self.ui.string_btn.setEnabled(True)
            self.ui.int_btn.setEnabled(True)
            self.ui.enum_btn.setEnabled(True)
            self.ui.bool_btn.setEnabled(True)
            self.ui.value_label.setText('Value')
        elif connect:
            self.disable_all()
            self.ui.in_attrs.setEnabled(True)
            self.ui.in_attr_label.setEnabled(True)
            self.ui.out_attr_label.setEnabled(True)
            self.ui.out_attrs.setEnabled(True)
            parent = selected.pop(0)
            children = selected
            p_attrs = self.collect_attributes(selected=[parent])
            if p_attrs:
                for p_attr in p_attrs:
                    self.ui.out_attrs.addItem(p_attr)
            c_attrs = self.collect_attributes(selected=children)
            if c_attrs:
                for c_attr in c_attrs:
                    self.ui.in_attrs.addItem(c_attr)

            self.ui.value_label.setText('')
        elif command:
            self.disable_all()
            self.ui.value_label.setEnabled(True)
            self.ui.values.setEnabled(True)
            self.ui.parent_child.setEnabled(True)
            self.ui.value_label.setText('Expression')

    def pop_up(self, message=None):
        if message:
            m = QtGui.QMessageBox()
            m.setText(message)
            m.exec_()

    def collect_attributes(self, selected=None):
        collected_attributes = []
        for sel in selected:
            get_attr = cmds.listAttr(sel)
            for attr in get_attr:
                if attr not in collected_attributes:
                    collected_attributes.append(attr)
        return collected_attributes

    def add_attr(self, obj=None, value=None, attr_type=None, min=None, max=None, enum_list=None,
                 default=None):
        self.func_running = True
        keyable = self.ui.keyable.isChecked()
        hidden = self.ui.hidden.isChecked()
        if value:
            value = value.replace(' ', '_')
        if obj:
            cmds.select(obj, r=True)
            if attr_type:
                if attr_type in ['float', '']:
                    if min and max:
                        cmds.addAttr(obj, ln=value, min=float(min), max=float(max), dv=float(default), k=keyable,
                                     hidden=hidden)
                    else:
                        cmds.addAttr(obj, ln=value, k=keyable, hidden=hidden)
                elif attr_type == 'int':
                    if min and max:
                        cmds.addAttr(obj, ln=value, min=int(min), max=int(max), dv=int(default), k=keyable,
                                     hidden=hidden)
                    else:
                        cmds.addAttr(ln=value, k=keyable, hidden=hidden)
                elif attr_type == 'vectorArray':
                    cmds.addAttr(obj, ln=value, at='double3', k=keyable, hidden=hidden)
                    x = '%sX' % value
                    y = '%sY' % value
                    z = '%sZ' % value
                    cmds.addAttr(obj, ln=x, at='double', p=value, k=keyable, hidden=hidden)
                    cmds.addAttr(obj, ln=y, at='double', p=value, k=keyable, hidden=hidden)
                    cmds.addAttr(obj, ln=z, at='double', p=value, k=keyable, hidden=hidden)
                elif attr_type == 'bool':
                    cmds.addAttr(obj, ln=value, at='bool', k=keyable, hidden=hidden)
                elif attr_type == 'string':
                    cmds.addAttr(obj, ln=value, dt='string', k=keyable, hidden=hidden)
                elif attr_type == 'enum':
                    cmds.addAttr(obj, ln=value, at='enum', en=enum_list, k=keyable, hidden=hidden)

    def set_attr(self, obj=None, value=None, attr_type=None, attribute=None):
        self.func_running = True
        if obj:
            cmds.select(obj, r=True)
            if attr_type:
                if attr_type in ['float', '']:
                    try:
                        cmds.setAttr('%s.%s' % (obj, attribute), float(value))
                    except (ValueError, RuntimeError):
                        self.func_running = False
                        self.pop_up('Wrong data type')
                elif attr_type == 'int':
                    try:
                        cmds.setAttr('%s.%s' % (obj, attribute), int(value))
                    except (ValueError, RuntimeError):
                        self.func_running = False
                        self.pop_up('Wrong data type')
                elif attr_type == 'vectorArray':
                    try:
                        if attribute.endswith('X') or attribute.endswith('Y') or attribute.endswith('Z'):
                            if ',' not in value:
                                cmds.setAttr('%s.%s' % (obj, attribute), float(value))
                            else:
                                raise ValueError
                                self.func_running = False
                        else:
                            if ',' in value:
                                split = value.split(',')
                                x = float(split[0].strip(' '))
                                y = float(split[1].strip(' '))
                                z = float(split[2].strip(' '))
                                cmds.setAttr('%s.%s' % (obj, attribute), x, y, z, type='double3')
                            else:
                                self.func_running = False
                                raise ValueError
                    except (ValueError, RuntimeError):
                        self.func_running = False
                        self.pop_up('Wrong data type')
                elif attr_type == 'bool':
                    if value in ['False', 'false', 'off', 'Off', '0', 0]:
                        value = False
                    elif value in ['True', 'true', 'On', 'on', '1', 1]:
                        value = True
                    try:
                        cmds.setAttr('%s.%s' % (obj, attribute), bool(value))
                    except (ValueError, RuntimeError):
                        self.func_running = False
                        self.pop_up('Wrong data type')
                elif attr_type == 'enum':
                    try:
                        cmds.setAttr('%s.%s' % (obj, attribute), int(value))
                    except (ValueError, RuntimeError):
                        self.func_running = False
                        self.pop_up('Wrong data type')
                elif attr_type == 'string':
                    try:
                        cmds.setAttr('%s.%s' % (obj, attribute), value, type='string')
                    except (ValueError, RuntimeError):
                        self.func_running = False
                        self.pop_up('Wrong data type')

    def connect_attr(self, parent=None, children=[], out_attr=None, in_attr=None):
        if children:
            for child in children:
                try:
                    cmds.connectAttr('%s.%s' % (parent, out_attr), '%s.%s' % (child, in_attr))
                except (RuntimeError, ValueError, AttributeError):
                    self.pop_up('These attributes will not connect!')
                    break
        else:
            self.pop_up('You need to select something to connect to.')

    def run_command(self):
        value = self.ui.values.toPlainText()
        expression = value
        selection = cmds.ls(sl=True)
        if selection:
            for selected in selection:
                try:
                    cmds.expression(s=expression, o=selected, ae=True, uc='all')
                except (RuntimeError, ValueError):
                    self.pop_up('Cannot apply the expression to %s.  Cancelling operation.' % selected)
                    break


    def run_it(self):
        add_mode = self.ui.add_mode.isChecked()
        set_mode = self.ui.set_mode.isChecked()
        conn_mode = self.ui.connect_mode.isChecked()
        comm_mode = self.ui.command_mode.isChecked()
        value = self.ui.values.toPlainText()
        min_val = self.ui.min_val.text()
        max_val = self.ui.max_val.text()
        default_val = self.ui.default_val.text()
        enum_list = self.ui.enum_list.text()
        selection = cmds.ls(sl=True)
        if selection:
            if add_mode:
                vector_btn = self.ui.vector_btn.isChecked()
                float_btn = self.ui.float_btn.isChecked()
                int_btn = self.ui.int_btn.isChecked()
                bool_btn = self.ui.bool_btn.isChecked()
                str_btn = self.ui.string_btn.isChecked()
                enum_btn = self.ui.enum_btn.isChecked()
                if value:
                    if vector_btn:
                        for sel in selection:
                            self.add_attr(obj=sel, value=value, attr_type='vectorArray')
                            if not self.func_running:
                                break
                    elif float_btn:
                        for sel in selection:
                            self.add_attr(obj=sel, value=value, attr_type='float', min=min_val,
                                          max=max_val, default=default_val)
                            if not self.func_running:
                                break
                    elif int_btn:
                        for sel in selection:
                            self.add_attr(obj=sel, value=value, attr_type='int', min=min_val,
                                          max=max_val, default=default_val)
                            if not self.func_running:
                                break
                    elif bool_btn:
                        for sel in selection:
                            self.add_attr(obj=sel, value=value, attr_type='bool')
                            if not self.func_running:
                                break
                    elif str_btn:
                        for sel in selection:
                            self.add_attr(obj=sel, value=value, attr_type='string')
                            if not self.func_running:
                                break
                    elif enum_btn:
                        for sel in selection:
                            self.add_attr(obj=sel, value=value, attr_type='enum', enum_list=enum_list)
                            if not self.func_running:
                                break
                else:
                    self.pop_up('There is no Name value for the new Attribute!')
                self.ui.values.setPlainText('')
            elif set_mode:
                vector_btn = self.ui.vector_btn.isChecked()
                float_btn = self.ui.float_btn.isChecked()
                int_btn = self.ui.int_btn.isChecked()
                bool_btn = self.ui.bool_btn.isChecked()
                str_btn = self.ui.string_btn.isChecked()
                enum_btn = self.ui.enum_btn.isChecked()
                attribute = self.ui.in_attrs.currentText()
                if value:
                    if vector_btn:
                        for sel in selection:
                            self.set_attr(obj=sel, value=value, attr_type='vectorArray', attribute=attribute)
                            if not self.func_running:
                                break
                    elif float_btn:
                        for sel in selection:
                            self.set_attr(obj=sel, value=value, attr_type='float', attribute=attribute)
                            if not self.func_running:
                                break
                    elif int_btn:
                        for sel in selection:
                            self.set_attr(obj=sel, value=value, attr_type='int', attribute=attribute)
                            if not self.func_running:
                                break
                    elif bool_btn:
                        for sel in selection:
                            self.set_attr(obj=sel, value=value, attr_type='bool', attribute=attribute)
                            if not self.func_running:
                                break
                    elif str_btn:
                        for sel in selection:
                            self.set_attr(obj=sel, value=value, attr_type='string', attribute=attribute)
                            if not self.func_running:
                                break
                    elif enum_btn:
                        for sel in selection:
                            self.set_attr(obj=sel, value=value, attr_type='enum', attribute=attribute)
                            if not self.func_running:
                                break
                else:
                    self.pop_up('There is no Name value to set!')
                self.ui.values.setPlainText('')
            elif conn_mode:
                parent = selection.pop(0)
                children = selection
                out_attr = self.ui.out_attrs.currentText()
                in_attr = self.ui.in_attrs.currentText()
                self.connect_attr(parent, children, out_attr, in_attr)
                self.ui.values.setPlainText('')
            elif comm_mode:
                self.run_command()
                self.ui.values.setPlainText('')
            cmds.select(selection, r=True)
        else:
            self.pop_up('Nothing is selected!')


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

