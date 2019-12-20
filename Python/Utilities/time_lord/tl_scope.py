"""
The Scope is a simple viewer for seeing who is clocked in, what they're working on, and how long they've been doing it.
It is an admin only tool.
"""

import shotgun_api3 as sgapi
import os
import sys
from PySide import QtGui, QtCore
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta
from dateutil import parser
import time
import math

# Time Lord Libraries
from bin.time_continuum import continuum
from bin.companions import companions
import bin.configuration
import bin.shotgun_collect
from bin.comm_system import comm_sys

from ui import time_lord_scope as tls

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.4.1'

config = bin.configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'scope.log'
log_root = os.path.join(sys.path[0], 'logs')
if not os.path.exists(log_root):
    os.makedirs(log_root)
log_path = os.path.join(log_root, log_file)
debug = config['debug_logging']
if debug == 'True' or debug == 'true' or debug == True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('scope')
logger.setLevel(level=level)
fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                              backupCount=int(config['log_days']))
fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
fh.setFormatter(fm)
logger.addHandler(fh)

logger.info('Scope Utility has started.')

# --------------------------------------------------------------------------------------------------
# Setup Shotgun Connection
# --------------------------------------------------------------------------------------------------
sg = sgapi.Shotgun(config['sg_url'], config['sg_name'], config['sg_key'])
logger.debug('Shotgun is connected.')

# --------------------------------------------------------------------------------------------------
# Connect Time Lord Components
# --------------------------------------------------------------------------------------------------
# setup continuum
tl_time = continuum(sg, config=config, sub='scope')

# Setup and get users
users = companions(sg, config=config, sub='scope')
user = users.get_user_from_computer()

# setup shotgun data connection
sg_data = bin.shotgun_collect.sg_data(sg, config=config, sub='scope')

# Setup the communications system
comm = comm_sys(sg, config=config, sub='scope')


class scope_signals(QtCore.QObject):
    user_running_time = QtCore.Signal(dict)
    view_list = QtCore.Signal(dict)
    add_user = QtCore.Signal(dict)
    remove_user = QtCore.Signal(dict)


class scope_engine(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

        self.scope_signals = scope_signals()

        # Build Scope
        self.scope = {}

        # UI Table List
        self.scope_viewer = {}

        self.scope_signals.view_list.connect(self.set_scope_viewer)

    def run(self, *args, **kwargs):
        second = int(datetime.now().second)
        minute = datetime.now().minute
        active_timesheets = tl_time.get_active_timesheets()
        self.compare_scope_to_timesheets(active_timesheets)
        self.compare_scope_to_viewer()
        while True:
            if second != int(datetime.now().second):
                second = int(datetime.now().second)
                if minute != datetime.now().minute:
                    minute = datetime.now().minute
                    active_timesheets = tl_time.get_active_timesheets()

                    # The compare_scope_to_timesheets() function sets the self.scope.  Which in turn gives us the
                    # master list of Artists to be displayed in the Scope Viewer.
                    self.compare_scope_to_timesheets(active_timesheets)
                    # print self.scope

                    # Update the Lists:
                    self.compare_scope_to_viewer()

    def set_scope_viewer(self, viewer=None):
        if viewer:
            self.scope_viewer = viewer

    def add_user(self, uid=None):
        pass

    def remove_user(self, uid=None):
        pass

    def compare_scope_to_viewer(self):
        if self.scope:
            for uid, data in self.scope.items():
                if uid not in self.scope_viewer.keys():
                    # The UID from the timesheets is not found in the return list from the UI
                    # NOTE: Might need a MUTEX here?
                    # So, Send the track to the UI to add a new Row.
                    self.scope_signals.add_user.emit({uid: data})

            for vuid, vdata in self.scope_viewer.items():
                if vuid not in self.scope.keys():
                    # Remove it from the list.
                    self.scope_signals.remove_user.emit({vuid: vdata})
                else:
                    v_task_id = vdata['task_id']
                    task_id = self.scope[vuid]['task_id']
                    print v_task_id
                    print task_id
                    if v_task_id != task_id:
                        print('Update Task')


    def compare_scope_to_timesheets(self, timesheets=None):
        # Check the timesheets against the scope list
        if timesheets:
            for timesheet in timesheets:
                user = timesheet['user']
                username = user['name']
                userid = user['id']
                project = timesheet['project']
                proj_name = project['name']
                proj_id = project['id']
                task = timesheet['entity']
                task_name = task['name']
                task_id = task['id']
                start_time = timesheet['sg_task_start']

                if userid not in self.scope.keys():
                    self.scope[userid] = {
                        'name': username,
                        'project': proj_name,
                        'proj_id': proj_id,
                        'entity': None,
                        'task': task_name,
                        'task_id': task_id,
                        'start_time': start_time
                    }
                elif userid in self.scope.keys() and self.scope[userid]['task_id'] != task_id:
                    print('WRONG TASK!')
                    print('userid: %s' % userid)
                    print('scope task: %s' % self.scope[userid]['task_id'])
                    print('task_id: %s' % task_id)

        # Check Scope List against Timesheets
        for uid, data in self.scope.items():
            # test = next(item for item in timesheets if item['user']['id'] == uid)
            still_clocked_in = filter(lambda item: item['user']['id'] == uid, timesheets)
            if not still_clocked_in:
                # remove from the scope
                del self.scope[uid]


class scope(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.scope_engine = scope_engine()

        # Set Viewer record
        self.scope_viewer = {}

        self.ui = tls.Ui_WhosWorking()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/tl_icon.ico'))

        self.ui.slave_list.setStyleSheet("QHeaderView::section{\n"
                                          "    \n"
                                          "    background-color: rgb(97, 97, 97);\n"
                                          "}\n"
                                          "QTableView::item{\n"
                                          "    border: 0px;\n"
                                          "    padding: 5px;\n"
                                          "}")

        # Setup column widths
        header = self.ui.slave_list.horizontalHeader()
        header.setResizeMode(4, QtGui.QHeaderView.Stretch)

        self.scope_engine.scope_signals.add_user.connect(self.add_user)
        self.scope_engine.scope_signals.remove_user.connect(self.remove_user)

        self.ui.slave_list.clear()
        self.scope_engine.start()

    def send_viewer_list(self, view_list=None):
        if view_list:
            self.scope_engine.scope_signals.view_list.emit(view_list)

    def add_user(self, data=None):
        """
        Add a user to the Table
        :param data: (dict) { ID: {
                                name
                                project
                                proj_id
                                entity
                                task
                                task_id
                                start_time
                                table_id
                                }
                            }
        :return:
        """
        uid = data.keys()[0]
        u_data = data[uid]
        name = u_data['name']
        project = u_data['project']
        proj_id = u_data['proj_id']
        entity = u_data['entity']
        task = u_data['task']
        task_id = u_data['task_id']
        start_time = u_data['start_time']

        row_count = self.ui.slave_list.rowCount()
        if row_count > 1:
            row = row_count - 1
        else:
            row = 0
        self.ui.slave_list.insertRow(row)

        name_label = QtGui.QLabel()
        name_label.setText(name)
        name_label.setToolTip('%s' % uid)
        self.ui.slave_list.setCellWidget(row, 0, name_label)
        proj_label = QtGui.QLabel()
        proj_label.setText(project)
        proj_label.setToolTip('Project ID: %s' % proj_id)
        self.ui.slave_list.setCellWidget(row, 1, proj_label)
        task_label = QtGui.QLabel()
        task_label.setText(task)
        task_tool = 'Entity: %s\n' \
                    'Task ID: %s' % (entity, task_id)
        task_label.setToolTip(task_tool)
        self.ui.slave_list.setCellWidget(row, 2, task_label)
        start_time_label = QtGui.QLabel()
        start_time_label.setText(str(start_time))
        self.ui.slave_list.setCellWidget(row, 3, start_time_label)

        self.scope_viewer[uid] = data[uid]

        # Return the Scope Viewer Data
        self.scope_engine.scope_signals.view_list.emit(self.scope_viewer)

    def remove_user(self, data=None):
        """
        Add a user to the Table
        :param data: (dict) { ID: {
                                name
                                project
                                proj_id
                                entity
                                task
                                task_id
                                start_time
                                table_id
                                }
                            }
        :return:
        """
        uid = data.keys()[0]
        u_data = data[uid]
        name = u_data['name']
        project = u_data['project']
        proj_id = u_data['proj_id']
        entity = u_data['entity']
        task = u_data['task']
        task_id = u_data['task_id']
        start_time = u_data['start_time']

        # Search through the table and find the UID?
        row_count = self.ui.slave_list.rowCount()
        for i in range(0, row_count-1):
            this_uid = int(self.ui.slave_list.cellWidget(i, 0).toolTip())
            if uid == this_uid:
                self.ui.slave_list.removeRow(i)
                break

        del(self.scope_viewer[uid])

        self.scope_engine.scope_signals.view_list.emit(self.scope_viewer)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    o = scope()
    o.show()
    sys.exit(app.exec_())



