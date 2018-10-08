# ATTRIBUTE MACHINE
# This version was configured to work specifically at ASC.  Minor adjustments would
# need to be made to run elsewhere.

__author__ = 'Adam Benson'
__version__ = '1.0.0'

from maya import cmds
import sys
import difflib
try:
    from PySide import QtCore, QtGui
except ImportError:
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

    def create_new_joints(self, link=None, duplicate=[], parent=None):
        start_selection = cmds.ls(sl=True)
        if link:
            rotation_order = cmds.xform(link, roo=True, q=True)
            rotation = cmds.xform(link, ro=True, q=True)
            translation = cmds.xform(link, t=True, q=True, ws=True)
            pivots = [translation[0], translation[1], translation[2]]
            joint_orient = cmds.getAttr('%s.jointOrient' % link)
            if duplicate:
                detect_existing = []
                dup_1 = duplicate[0]
                dup_2 = duplicate[1]

                # First joint chain
                if cmds.objExists(dup_1):
                    print 'This thing already exists! Skipping %s' % dup_1
                    detect_existing.append(dup_1)
                else:
                    cmds.select(cl=True)
                    cmds.joint(n=dup_1, o=joint_orient[0], p=pivots, roo=rotation_order)
                    if parent:
                        dup_1_diff = difflib.ndiff(link, dup_1)
                        dup_1_tag = ''
                        link_tag = ''
                        for a, b in enumerate(dup_1_diff):
                            if b[0] == '+':
                                dup_1_tag += b[-1]
                            elif b[0] == '-':
                                link_tag += b[-1]

                        dup_1_parent = parent.replace(link_tag, dup_1_tag)
                        cmds.parent(dup_1, dup_1_parent)
                    cmds.setAttr('%s.rotate' % dup_1, rotation[0], rotation[1], rotation[2])
                    cmds.setAttr('%s.jointOrient' % dup_1, joint_orient[0][0], joint_orient[0][1], joint_orient[0][2])

                # Second joint chain
                if cmds.objExists(dup_2):
                    print 'This thing already exists! Skipping %s' % dup_2
                    detect_existing.append(dup_2)
                else:
                    cmds.select(cl=True)
                    cmds.joint(n=dup_2, o=joint_orient[0], p=pivots, roo=rotation_order)
                    if parent:
                        dup_2_diff = difflib.ndiff(link, dup_2)
                        dup_2_tag = ''
                        link_tag = ''
                        for a, b in enumerate(dup_2_diff):
                            if b[0] == '+':
                                dup_2_tag += b[-1]
                            elif b[0] == '-':
                                link_tag += b[-1]
                        dup_2_parent = parent.replace(link_tag, dup_2_tag)
                        cmds.parent(dup_2, dup_2_parent)
                    cmds.setAttr('%s.rotate' % dup_2, rotation[0], rotation[1], rotation[2])
                    cmds.setAttr('%s.jointOrient' % dup_2, joint_orient[0][0], joint_orient[0][1], joint_orient[0][2])
        cmds.select(start_selection, r=True)

    def run_build(self):
        # Main operation - Note: current joint tags are: BND, IK, FK
        # TODO: I still need to add some idiot proofing, and error handling
        # TODO: There is an error with parenting when I start with the BND joints.

        IK_tag = self.ui.tag_1.text()
        FK_tag = self.ui.tag_2.text()
        bind_tag = self.ui.tag_3.text()
        controller = self.ui.driver_object_name.text()
        attribute_Name = self.ui.switch_attributes.currentText()
        if controller == 'No Selection':
            controller = None
        if not  controller:
            controller_alert = qtGUI.QMessageBox()
            controller_alert.setText('You must set a controller and attribute!')
            controller_alert.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            controller_alert.exec_()
            return False
        if not attribute_Name:
            attr_alert = qtGUI.QMessageBox()
            attr_alert.setText('You must pick an attribute to drive the FKIK Switch.')
            attr_alert.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            attr_alert.exec_()
            return False
        create_new = self.ui.create_new.isChecked()
        cmds.select(hi=True)
        joint_chain = cmds.ls(sl=True)
        reverse = cmds.createNode('plusMinusAverage')
        cmds.setAttr('%s.operation' % reverse, 2)
        cmds.setAttr('%s.input1D[0]' % reverse, 1)
        cmds.connectAttr('%s.%s' % (controller, attribute_Name), '%s.input1D[1]' % reverse)
        parent = None
        for link in joint_chain:
            if cmds.nodeType(link) == 'joint':
                if IK_tag in link:
                    ik = link
                    fk = link.replace(IK_tag, FK_tag)
                    bnd = link.replace(IK_tag, bind_tag)
                    if create_new:
                        self.create_new_joints(link=ik, duplicate=[fk, bnd], parent=parent)
                        parent = link
                elif FK_tag in link:
                    ik = link.replace(FK_tag, IK_tag)
                    fk = link
                    bnd = link.replace(FK_tag, bind_tag)
                    if create_new:
                        self.create_new_joints(link=fk, duplicate=[ik, bnd], parent=parent)
                        parent = link
                elif bind_tag in link:
                    ik = link.replace(bind_tag, IK_tag)
                    fk = link.replace(bind_tag, FK_tag)
                    bnd = link
                    if create_new:
                        self.create_new_joints(link=bnd, duplicate=[ik, fk], parent=parent)
                        parent = link
                else:
                    # print 'Dude, your shit is fucked up.  You must have grabbed the wrong fucking bone!'
                    quick_alert = qtGUI.QMessageBox()
                    quick_alert.setText('This selection doesn\'t seem to be a valid FKIK Joint Chain')
                    quick_alert.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                    quick_alert.exec_()

                if cmds.objExists(fk) and cmds.objExists(ik) and cmds.objExists(bnd):
                    point = cmds.pointConstraint(fk, bnd, mo=True, w=1)
                    cmds.pointConstraint(ik, bnd, mo=True, w=0)
                    orient = cmds.orientConstraint(fk, bnd, mo=True, w=1)
                    cmds.orientConstraint(ik, bnd, mo=True, w=0)
                    # print point
                    # print orient
                    cmds.connectAttr('%s.output1D' % reverse, '%s.%sW0' % (point[0], fk))
                    cmds.connectAttr('%s.%s' % (controller, attribute_Name), '%s.%sW1' % (point[0], ik))
                    cmds.connectAttr('%s.output1D' % reverse, '%s.%sW0' % (orient[0], fk))
                    cmds.connectAttr('%s.%s' % (controller, attribute_Name), '%s.%sW1' % (orient[0], ik))
                else:
                    missing_parts = qtGUI.QMessageBox()
                    missing_parts.setText('The necessary FK, IK and Bind joints cannot be found. Joints can be created'
                                          'using the "Create New" option.')
                    missing_parts.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                    missing_parts.exec_()
                    break
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
