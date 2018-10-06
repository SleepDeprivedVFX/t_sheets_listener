# ATTRIBUTE MACHINE
# This version was configured to work specifically at ASC.  Minor adjustments would
# need to be made to run elsewhere.

__author__ = 'Adam Benson'
__version__ = '1.0.0'

from maya import cmds
import sys
try:
    from PySide import QtCore, QtGui
except:
    from PySide2 import QtCore, QtGui, QtWidgets


if 'PySide' in sys.modules:
    qtGUI = QtGui
elif 'PySide2' in sys.modules:
    qtGUI = QtWidgets
else:
    qtGUI = None
    print 'FUCK!!!'

sys.path.append(r'C:\Users\sleep\OneDrive\Documents\Scripts\Python\Maya\RiggingTools\switch_witch')
from ui import switch_witch_ui as sw
reload(sw)


class sw_ui(qtGUI.QWidget):
    """
    Attribute Machine UI.
    """
    def __init__(self, parent=None):
        # Preliminary things
        qtGUI.QWidget.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui = sw.Ui_switchwitch()
        self.ui.setupUi(self)
        self.ui.select_controller.clicked.connect(self.select_control)
        self.ui.build.clicked.connect(self.run_build)
        self.ui.done.clicked.connect(self.cancel)

    def collect_attributes(self, selected=None):
        collected_attributes = []
        for sel in selected:
            get_attr = cmds.listAttr(sel)
            for attr in get_attr:
                if attr not in collected_attributes:
                    collected_attributes.append(attr)
        return collected_attributes

    def cancel(self):
        self.close()

    def select_control(self):
        prime_selection = cmds.ls(sl=True)
        if prime_selection:
            select = prime_selection[0]
            self.ui.driver_object_name.setText(select)
            self.ui.switch_attributes.clear()
            get_attrs = self.collect_attributes([select])
            for attr in get_attrs:
                self.ui.switch_attributes.addItem(attr)
            cmds.select(cl=True)

    def run_build(self):
        # Main operation - Note: current joint tags are: BND, IK, FK
        # TODO: I need to add the more robost features, like building the bones too.
        '''
        Before we do anything, we need to import the data from the UI, then...
        Start with the same IK_tag check.  Depending on what bone is selected, that becomes the master bone
        Before each duplicate is created, the name is checked for, assuring that the bone doesn't
        already exist in the scene.
        Assuming it doesn't, it will need to read down the hierarchy, checking for transform nodes in between
        If it finds joints further down the chain, it should create those as well, although the transforms bring
        up their own potential issues.  My gut instinct is to NOT create them, but then another part of me says
        duplicate the tree verbatim, so that it has all the same construction.  I just don't want it accidentally
        duplicating effectors, constraints or IK handles.  Locators might be necessary, as well as straight transforms

        :return:
        '''

        IK_tag = self.ui.tag_1.text()
        FK_tag = self.ui.tag_2.text()
        bind_tag = self.ui.tag_3.text()
        controller = self.ui.driver_object_name.text()
        attribute_Name = self.ui.switch_attributes.currentText()
        cmds.select(hi=True)
        joint_chain = cmds.ls(sl=True)
        reverse = cmds.createNode('plusMinusAverage')
        cmds.setAttr('%s.operation' % reverse, 2)
        cmds.setAttr('%s.input1D[0]' % reverse, 1)
        cmds.connectAttr('%s.%s' % (controller, attribute_Name), '%s.input1D[1]' % reverse)
        for link in joint_chain:
            if cmds.nodeType(link) == 'joint':
                if IK_tag in link:
                    ik = link
                    fk = link.replace(IK_tag, FK_tag)
                    bnd = link.replace(IK_tag, bind_tag)
                elif FK_tag in link:
                    ik = link.replace(FK_tag, IK_tag)
                    fk = link
                    bnd = link.replace(FK_tag, bind_tag)
                elif bind_tag in link:
                    ik = link.replace(bind_tag, IK_tag)
                    fk = link.replace(bind_tag, FK_tag)
                    bnd = link
                else:
                    print 'Dude, your shit is fucked up.  You must have grabbed the wrong fucking bone!'
                point = cmds.pointConstraint(fk, bnd, mo=True, w=1)
                cmds.pointConstraint(ik, bnd, mo=True, w=0)
                orient = cmds.orientConstraint(fk, bnd, mo=True, w=1)
                cmds.orientConstraint(ik, bnd, mo=True, w=0)
                print point
                print orient
                cmds.connectAttr('%s.output1D' % reverse, '%s.%sW0' % (point[0], fk))
                cmds.connectAttr('%s.%s' % (controller, attribute_Name), '%s.%sW1' % (point[0], ik))
                cmds.connectAttr('%s.output1D' % reverse, '%s.%sW0' % (orient[0], fk))
                cmds.connectAttr('%s.%s' % (controller, attribute_Name), '%s.%sW1' % (orient[0], ik))
            else:
                break


# try:
#     app = qtGUI.QApplication(sys.argv)
#     sys.exit(app.exec_())
# except:
#     app = qtGUI.QApplication.instance()
if __name__ == '__main__':
    try:
        app = qtGUI.QApplication(sys.argv)
        window = sw_ui()
        window.show()
        sys.exit(app.exec_())
    except:
        app = qtGUI.QApplication.instance()
        window = sw_ui()
        window.show()
