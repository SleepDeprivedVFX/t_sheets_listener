from PySide import QtCore, QtGui
from maya import cmds
import sys
import os
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
        self.set_mode()

    def set_mode(self):
        add = self.ui.add_mode.isChecked()
        set = self.ui.set_mode.isChecked()
        connect = self.ui.connect_mode.isChecked()
        command = self.ui.command_mode.isChecked()
        if add:
            selected = cmds.ls(sl=True)
            attrs = self.collect_attributes(selected=selected)
            index = 0
            print attrs
            for attr in attrs:
                # self.ui.in_attrs_list.addItem(QtGui.QListWidgetItem(QtGui.QRadioButton('%s' % attr)))
                # radio_btn = QtGui.QRadioButton('%s' % attr)
                # radio_btn.setObjectName(attr)
                # print radio_btn.text()
                # row = QtGui.QListWidgetItem(radio_btn)
                # self.ui.in_attrs_list.addItem(row)
                # index += 1
                row = QtGui.QTreeWidgetItem()
                row.setText(0, attr)
                add_btn = QtGui.QRadioButton()
                add_btn.setText(attr)
                add_btn.parent()

        elif set:
            pass
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

