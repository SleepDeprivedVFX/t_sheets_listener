from PySide import QtCore, QtGui
from maya import cmds
import sys
import os
poop = os.environ['path']
shit = poop.split(';')
for turd in shit:
    print turd
sys.path.append('C:/Users/sleep/OneDrive/Documents/Scripts/Python/Maya/RiggingTools/attribute_machine')
from ui import attribute_machine_ui as amu

class attr_mach_ui(QtGui.QWidget):
    """
    Attribute Machine UI.
    """
    def __init__(self, parent=None):
        # Preliminary things
        QtGui.QWidget.__init__(self, parent)
        self.ui = amu.machine()
        self.ui.setupUi(self)
        self.ui.do_it.clicked.connect(self.run_it)
        self.ui.dont_do_it.clicked.connect(self.close)

    def run_it(self):
        pass

if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)
    window = attr_mach_ui()
    window.show()
    sys.exit(app.exec_())
