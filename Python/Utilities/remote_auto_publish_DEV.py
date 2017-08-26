from libs.shotgun_api3 import Shotgun
import time
import os, sys, platform, re
import json as js
import logging as logger
import threading as t
from tkinter import filedialog as tk
import psd_tools as psd
import shutil
import rap_ui.remote_auto_publish_UI as ui
from PySide import QtCore, QtGui

'''
This tools requires the following libraries be installed:
psd-tools       --  python -m pip install psd-tools
Pillow          --  python -m pip install Pillow
shotgun_api3    --  python -m pip install git+git://github.com/shotgunsoftware/python-api.git
                In this case, the library is already included in the package.
'''
__author__ = 'Adam Benson'
__version__ = '1.0.1'

# Shotgun Configuration
shotgun_conf = {
    'url': 'https://asc.shotgunstudio.com',
    'name': 'remoteAutoPublisher',
    'key': '83b249a40f7a769bb6ff0f7d6a35ba158f18c52aa8f0ec3e8d7ed2fdeed454b5'
}

# Detect OS
osSystem = platform.system()
if osSystem == 'Windows':
    os_root = '//hal'
else:
    os_root = '/Volumes'

# Shotgun Roots - May eventually come from shotgun db, but for now... hard-code
sg_root = os_root + '/jobs/'

# Create Log file
logDate = str(time.strftime('%m%d%y'))
logfile = "%s/tools/scripts/logs/remoteAutoPublish_%s.log" % (os_root, logDate)
logger.basicConfig(level=logger.INFO, filename=logfile, filemode='w+')
logger.info('Starting the Remote Auto Publisher...')

# Set the database file
db = '//hal/tools/scripts/python/utilities/remote_auto_publish/db/remote_auto_publish_DB.json'

# Setup file type recognizers
publish_types = [
    '.psd',
    '.nk',
    '.mb',
    '.ma',
    '.ztl',
    '.mud',
    '.hip',
]


class RemoteAutoPublisher(QtGui.QWidget):
    """
    Remote Auto Publisher Utility
    This tool is designed to watch folders for changes and publish new objects put within a proper folder structure.
    It is designed to work with Shotgun Studio and a Dropbox folder.
    At regular intervals the tool will do the following actions:
        1. Connect to Shotgun and check for Active Projects and their associated assets.
        2. If a new project or project-asset is found in Shotgun, a correlating folder structure will be built in
            the Dropbox, and a JSON database entry may be added.
        3. At regular intervals, the tools will search the Dropbox folder structure and compare the contents to
            entries in the JSON database.
        4. If a new object is found, it is simultaneously added to the JSON database, and published to the appropriate
            asset in Shotgun.
        5. Lastly, the new object will be copied to the appropriate Real Shotgun Project, and a message will be
            posted letting pertinent people know that a new Auto-Publish has been made.
    """
    timer = QtCore.QTimer()
    count = 0

    def __init__(self, parent=None):
        super(RemoteAutoPublisher, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui = ui.Ui_RemoteAutoPublish()
        self._generator = None
        self._timerId = None
        self.set_timer = [0, 0, 1, 0]
        # Set the Dropbox folder
        self.dropbox = ''
        self.ui.setupUi(self)
        self.clock_setup()
        self.publish_queue = []
        logger.info('UI setup complete')

    # ---------------------------------------------------------------------------------------------------------------
    # Main Loop Generator
    # ---------------------------------------------------------------------------------------------------------------
    def loop_generator(self):
        """
        Main loop and time related event trigger.
        Put anything needed to be triggered at an interval into any of the positions below.

        :return: None
        """
        s = 0
        m = 0
        h = 0
        d = 0
        # Counters c is short for Counter: cs = CounterSeconds = 5
        cs = int(self.set_timer[3])
        cm = int(self.set_timer[2])
        ch = int(self.set_timer[1])
        cd = int(self.set_timer[0])

        lastTime = [0, 0, 0, 0]
        while self._generator:
            # Time interval settings and counting
            if s < 59:
                s += 1
            else:
                if m < 59:
                    s = 0
                    m += 1
                    # Close the log file and reinitialize another one.
                elif m == 59 and h < 24:
                    h += 1
                    m = 0
                    s = 0
                elif m == 59 and h == 24:
                    d += 1
                    h = 0
                    m = 0
                    s = 0

            ts = s - cs
            tm = m - cm
            th = h - ch
            td = d - cd
            t_time = [abs(td), abs(th), abs(tm), abs(ts)]
            if t_time == lastTime:
                # reset lastTime
                lastTime = [d, h, m, s]
                # Begin timed event triggers
                cshot = t.Thread(name='check_sg', target=self.check_Shotgun)
                cshot.start()

            # Set timer displays for the current loop
            self.ui.seconds_timer.display(s)
            self.ui.minutes_timer.display(m)
            self.ui.hours_timer.display(h)
            self.ui.days_timer.display(d)
            yield

    # ---------------------------------------------------------------------------------------------------------------
    # Clock Setup
    # ---------------------------------------------------------------------------------------------------------------
    def clock_setup(self):
        self.ui.start_btn.clicked.connect(self.start)
        self.ui.stop_btn.clicked.connect(self.stop)
        self.ui.set_minutes.setValue(1)
        self.ui.browse.clicked.connect(self.get_watch_folder)
        self.display_database()
        self.ui.set_seconds.setMaximum(59)
        self.ui.set_minutes.setMaximum(59)
        self.ui.set_hours.setMaximum(23)
        self.ui.set_hours.setMinimum(0)
        self.ui.set_seconds.setMinimum(0)
        self.ui.set_minutes.setMinimum(0)
        self.ui.set_days.setMinimum(0)

    # ---------------------------------------------------------------------------------------------------------------
    # Display the Database
    # ---------------------------------------------------------------------------------------------------------------
    def display_database(self):
        # Open the database and process
        f = open(db, 'r')
        data = js.load(f)
        self.ui.database.setHeaderHidden(True)
        projects = data.keys()
        projects = sorted(list(projects))
        for project in projects:
            this_proj = QtGui.QTreeWidgetItem([project])
            self.ui.database.addTopLevelItem(this_proj)
            assets = data[project]['Assets']
            for asset in assets:
                this_asset = QtGui.QTreeWidgetItem([asset])
                this_proj.addChild(this_asset)
                files = data[project]['Assets'][asset]
                for fname in files:
                    this_file = QtGui.QTreeWidgetItem([fname])
                    this_asset.addChild(this_file)

    # ---------------------------------------------------------------------------------------------------------------
    # Open a browser window to select the Watch Folder
    # ---------------------------------------------------------------------------------------------------------------
    def get_watch_folder(self):
        new_folder = tk.askdirectory()
        self.ui.watch_folder.setText(new_folder)

    # ---------------------------------------------------------------------------------------------------------------
    # Start Timer
    # ---------------------------------------------------------------------------------------------------------------
    def start(self):
        self.stop()
        days = self.ui.days_timer.value()
        hours = self.ui.hours_timer.value()
        minutes = self.ui.set_minutes.value()
        seconds = self.ui.set_seconds.value()
        self.dropbox = self.ui.watch_folder.text() + '/'
        logger.info('Watch_folder set to %s' % self.dropbox)
        self.ui.set_days.setEnabled(False)
        self.ui.set_hours.setEnabled(False)
        self.ui.set_minutes.setEnabled(False)
        self.ui.set_seconds.setEnabled(False)
        self.set_timer = [days, hours, minutes, seconds]
        logger.info('Timer set to %s' % self.set_timer)
        self._generator = self.loop_generator()
        self._timerId = self.startTimer(1000)
        logger.info('Loop Started!  Beginning Auto Publisher...')

    # ---------------------------------------------------------------------------------------------------------------
    # Stop Timer
    # ---------------------------------------------------------------------------------------------------------------
    def stop(self):
        if self._timerId is not None:
            self.killTimer(self._timerId)
            logger.info('Loop Stopped!  Auto Publisher Paused!')
            self.ui.set_days.setEnabled(True)
            self.ui.set_hours.setEnabled(True)
            self.ui.set_minutes.setEnabled(True)
            self.ui.set_seconds.setEnabled(True)
        self._generator = None
        self._timerId = None

    # ---------------------------------------------------------------------------------------------------------------
    # Timer Generator Event
    # ---------------------------------------------------------------------------------------------------------------
    def timerEvent(self, event):
        if self._generator is None:
            return
        try:
            next(self._generator)
        except StopIteration:
            self.stop()

    # ---------------------------------------------------------------------------------------------------------------
    # Check Shotgun - SUB: Check Database, Check Folders, Check Assets
    # ---------------------------------------------------------------------------------------------------------------
    def check_Shotgun(self):
        """
        Check shotgun for active projects and assets
        :return:
        """
        try:
            sg = Shotgun(shotgun_conf['url'], shotgun_conf['name'], shotgun_conf['key'])
        except Exception, e:
            logger.info('What the fuck? %s' % e)
            sg = None
        filters = [
            ['sg_status', 'is', 'active']
        ]
        fields = [
            'id',
            'tank_name'
        ]
        projects_list = sg.find('Project', filters, fields)

        # Make sure the database and the folder structure both have the currently active projects.
        for project_info in projects_list:
            name = project_info['tank_name']
            sg_id = project_info['id']
            project = self.check_project(name=name, id_num=sg_id)
            if project:
                asset_filters = [
                    ['project', 'is', {'type': 'Project', 'id': sg_id}]
                ]
                asset_fields = [
                    'code'
                ]
                asset_list = sg.find('Asset', asset_filters, asset_fields)
                for asset in asset_list:
                    asset_name = asset['code']
                    asset_id = asset['id']
                    self.check_asset(project=name, name=asset_name, ass_id=asset_id)

        # Update the display - This is currently not working
        # self.update_display()
        # Watch for new files and compare the files with the database
        self.watch()

    # ---------------------------------------------------------------------------------------------------------------
    # Update the display  - Currently not functional
    # ---------------------------------------------------------------------------------------------------------------
    def update_display(self):
        # THIS IS CURRENTLY NOT WORKING
        iterator = QtGui.QTreeWidgetItemIterator(self.ui.database)
        while iterator.value():
            item = iterator.value()

            iterator.next()
            print item.text(0)

    # ---------------------------------------------------------------------------------------------------------------
    # Actively watch the folder for new files
    # ---------------------------------------------------------------------------------------------------------------
    def watch(self):
        f = open(db, 'r')
        data = js.load(f)
        projects = os.listdir(self.dropbox)
        for project in projects:
            if project in data:
                path = self.dropbox + project
                assets = os.listdir(path)
                for asset in assets:
                    if asset in data[project]['Assets']:
                        asset_path = path + '/' + asset
                        file_path = asset_path + '/'
                        files = [fname for fname in os.listdir(asset_path) if os.path.isfile(file_path + fname)]
                        if files:
                            for fname in files:
                                publish_this = False
                                if fname in data[project]['Assets'][asset]:
                                    in_db = True
                                else:
                                    in_db = False
                                if not in_db:
                                    # This may have to have a queue added to it at some point.
                                    # While Yield Next mixed with thread.is_alive() or something.
                                    logger.info('New File Found! %s' % fname)
                                    logger.info('%s not found in database!' % fname)
                                    publish_file = file_path + fname
                                    if os.path.isfile(publish_file):
                                        for p_type in publish_types:
                                            if fname.endswith(p_type):
                                                publish_this = True
                                                break
                                            else:
                                                publish_this = False
                                        if publish_this:
                                            # This is where I need to add this data to a queue, and then have the queue
                                            # publish the data.
                                            # Essentially: While there is something in the queue, publish the items.
                                            try:
                                                run_publish = t.Thread(name='Publish', target=self.publish_file,
                                                                       kwargs={'filename': fname,
                                                                               'path': file_path,
                                                                               'project': project,
                                                                               'asset': asset})
                                                run_publish.start()
                                            except Exception, e:
                                                logger.error('THE PUBLISH THREAD FAILED! %s' % e)
                                        else:
                                            # Same thing with the versions, need a queue here.
                                            # This might be easier than I expected.
                                            try:
                                                run_version = t.Thread(target=self.version_file,
                                                                       kwargs={'filename': fname,
                                                                               'path': file_path,
                                                                               'project': project,
                                                                               'asset': asset})
                                                run_version.start()
                                            except Exception, e:
                                                logger.error('THE VERSION THREAD FAILED! %s' % e)
        f.close()

    # ---------------------------------------------------------------------------------------------------------------
    # Publish the file
    # ---------------------------------------------------------------------------------------------------------------
    def publish_file(self, **kwargs):
        logger.info('File publish requested!')
        filename = kwargs['filename']
        project = kwargs['project']
        asset = kwargs['asset']
        path = kwargs['path']
        logger.info('Filename: %s' % filename)
        logger.info('Project: %s' % project)
        logger.info('Asset: %s' % asset)

        # Get the task info
        task = self.get_task(filename=filename, project=project, asset=asset)
        proj_id = task['proj_id']
        asset_id = task['asset_id']
        task_id = task['task_id']
        asset_type = task['asset_type']

        fixed_asset = asset.replace(' ', '-')
        fixed_filename = filename.replace(' ', '-')

        sg = Shotgun(shotgun_conf['url'], shotgun_conf['name'], shotgun_conf['key'])

        original_path = path + '/' + filename
        name_only = str(filename).rsplit('.', 1)[0]
        ext = str(filename).rsplit('.', 1)[1]

        # Find the Server Asset path
        alleged_asset_path = sg_root + '%s/assets/%s/%s/tasks' % (project, asset_type, fixed_asset)
        if os.path.exists(alleged_asset_path):
            task_path = alleged_asset_path + '/design.main'
            if not os.path.exists(task_path):
                os.mkdir(task_path)
                logger.info('Folder created... %s' % task_path)
                logger.info('PASSED make directory %s' % task_path)
        else:
            # THE FOLLOWING WAS MEANT TO CREATE FOLDERS ON HAL - IT FAILED.
            check_asset_type_path = sg_root + '%s/assets/%s' % (project, asset_type)
            check_asset_path = check_asset_type_path + '/%s' % fixed_asset
            if not os.path.exists(check_asset_type_path):
                os.mkdir(check_asset_type_path)
                logger.info('Folder created: %s' % check_asset_type_path)
            if not os.path.exists(check_asset_path):
                os.mkdir(check_asset_path)
                logger.info('Folder created: %s' % check_asset_path)
            os.mkdir(alleged_asset_path)
            logger.info('Folder created... %s' % alleged_asset_path)
            task_path = alleged_asset_path + '/design.main'
            os.mkdir(task_path)
            logger.info('Folder Created... %s' % task_path)

        # Find the Publish Path
        # The IDs are the constants currently in the shotgun database.
        # This could be dangerous later on.
        if ext.lower() == 'psd':
            folder = 'photoshop'
            published_file_type = {'type': 'PublishedFileType', 'id': 39}
            thumbnail_path = path + '/%s_thumb.jpg' % name_only
            task_path = task_path + '/' + folder
            try:
                file_to_pub = psd.PSDImage.load(original_path)
                thumbnail = file_to_pub.as_PIL()
                thumbnail.save(thumbnail_path)
                logger.info('Thumbnail created for %s' % name_only)
            except IOError, e:
                logger.info('UNABLE TO WRITE THUMBNAIL! %s', e)
        elif ext.lower() == 'ma' or ext.lower() == 'mb':
            folder = 'maya'
            published_file_type = {'type': 'PublishedFileType', 'id': 37}
            task_path = task_path + '/' + folder
        elif ext.lower() == 'ztl':
            folder = 'zbrush'
            published_file_type = {'type': 'PublishedFileType', 'id': 49}
            task_path = task_path + '/' + folder
        elif ext.lower() == 'hip':
            folder = 'houdini'
            published_file_type = {'type': 'PublishedFileType', 'id': 40}
            task_path = task_path + '/' + folder
        elif ext.lower() == 'scn':
            folder = 'softimage'
            published_file_type = {'type': 'PublishedFileType', 'id': 4}
            task_path = task_path + '/' + folder
        elif ext.lower() == 'edml':
            folder = 'softimage'
            published_file_type = {'type': 'PublishedFileType', 'id': 5}
            task_path = task_path + '/' + folder
        elif ext.lower() == 'nk':
            folder = 'comps'
            published_file_type = {'type': 'PublishedFileType', 'id': 1}
            task_path = task_path + '/' + folder
        elif ext.lower() == 'abc':
            folder = 'caches/Alembic'
            published_file_type = {'type': 'PublishedFileType', 'id': 38}
            task_path = task_path + '/' + folder
        elif ext.lower() == 'obj':
            folder = 'geo'
            published_file_type = {'type': 'PublishedFileType', 'id': 45}
            task_path = task_path + '/' + folder
        else:
            folder = 'elements'
            published_file_type = {'type': 'PublishedFileType', 'id': 47}
            task_path = task_path + '/' + folder
            thumbnail_path = path + '/%s_thumb.jpg' % name_only
            file_to_pub = ''
            thumbnail = ''
        if not os.path.exists(task_path):
            os.mkdir(task_path)
            logger.info('Folder created: %s' % task_path)
        alleged_publish_path = sg_root + '%s/assets/%s/%s/publish/%s/design.main/' % (project, asset_type, asset, folder)
        logger.info('alleged_publish_path: %s' % alleged_publish_path)
        if os.path.exists(alleged_publish_path):
            publish_path = alleged_publish_path
        else:
            check_publish_path = sg_root + '%s/assets/%s/%s/publish' % (project, asset_type, asset)
            check_publish_type_path = check_publish_path + '/' + folder
            if not os.path.exists(check_publish_path):
                os.mkdir(check_publish_path)
                logger.info('Folder created: %s' % check_publish_path)
            if not os.path.exists(check_publish_type_path):
                os.mkdir(check_publish_type_path)
                logger.info('Folder created: %s' % check_publish_type_path)
            os.mkdir(alleged_publish_path)
            publish_path = alleged_publish_path
            logger.info('Folder created on SERVER: HAL - %s' % publish_path)

        # Find existing versions
        pattern = re.compile(r'(_v\d*|_V\d*|\sv\d{1,5}|\sV\d{1,5})')
        task_files = os.listdir(task_path)
        publish_files = os.listdir(publish_path)
        version = 1
        check_name = ''
        search_for_version = []
        sorted(task_files)
        sorted(publish_files)
        if task_files:
            # this may be where the problem lies... last_file = 'snapshots' in some folders.  Lame...
            if task_files[-1] != 'snapshots':
                last_file = task_files[-1]
            else:
                # For or While loop to figure out the highest numbered file.
                for t_file in task_files:
                    if os.path.isfile(task_path + '/' + t_file):
                        search_for_version.append(t_file)
                last_file = search_for_version[-1]

            find_version = pattern.search(last_file)
            if find_version:
                version = int(re.sub(r'\D', '', find_version.group()))
                version += 1
                check_name = '%s_design.main_v%03d.%s' % (asset, version, ext)
                save_task_path = task_path + '/' + check_name
                check = False
                while check:
                    if os.path.exists(save_task_path):
                        version += 1
                        check_name = '%s_design.main_v%03d.%s' % (asset, version, ext)
                        save_task_path = task_path + '/' + check_name
                    else:
                        check = True
                shutil.copy2(original_path, save_task_path)
                logger.info('Publish file copied to HAL and renamed to fit Shotgun Template - %s' % save_task_path)
            else:
                version = 1
                check_name = '%s_design.main_v001.%s' % (asset, ext)
                save_task_path = task_path + '/' + check_name
                shutil.copy2(original_path, save_task_path)
                logger.info('Publish file copied to HAL and renamed to fit Shotgun Template - %s' % save_task_path)
        else:
            check_name = '%s_design.main_v001.%s' % (asset, ext)
            shutil.copy2(original_path, (task_path + '/' + check_name))
            logger.info('Publish file copied to HAL and renamed to fit Shotgun Template - %s' % (task_path + '/' + check_name))

        if publish_files:
            last_file = publish_files[-1]
            find_version = pattern.search(last_file)
            if find_version:
                version = int(re.sub(r'\D', '', find_version.group()))
                version += 1
                publish_name = '%s_design.main_v%03d.%s' % (asset, version, ext)
                save_publish_path = publish_path + publish_name
                check = False
                while check:
                    if os.path.exists(save_publish_path):
                        version += 1
                        publish_name = '%s_design.main_v%03d.%s' % (asset, version, ext)
                        save_publish_path = publish_path + publish_name
                    else:
                        check = True
                shutil.copy2(original_path, save_publish_path)
                logger.info('Publish file copied to HAL and renamed to fit Shotgun Template - %s' % save_publish_path)
            else:
                version = 1
                publish_name = '%s_design.main_v001.%s' % (asset, ext)
                save_publish_path = publish_path + publish_name
                shutil.copy2(original_path, save_publish_path)
                logger.info('Publish file copied to HAL and renamed to fit Shotgun Template - %s' % save_publish_path)
        else:
            publish_name = '%s_design.main_v001.%s' % (asset, ext)
            shutil.copy2(original_path, (publish_path + publish_name))
            logger.info('Publish file copied to HAL and renamed to fit Shotgun Template - %s' % (publish_path + publish_name))

        publisher_path = '%s/assets/%s/%s/publish/%s/design.main/%s' % (project, asset_type, asset, folder, publish_name)
        pub_path = sg_root + publisher_path
        publish_data = {
            'project': {'type': 'Project', 'id': proj_id},
            'entity': {'type': 'Asset', 'id': asset_id},
            'task': {'type': 'Task', 'id': task_id},
            'name': 'design.main',
            'description': 'File was found in a watch folder and was auto-published.',
            'code': publish_name,
            'path_cache': publisher_path,
            'version_number': version,
            'published_file_type': published_file_type
        }
        new_publish = sg.create('PublishedFile', publish_data)
        publish_id = int(new_publish['id'])
        publish_update = {
            'path': {'local_path': pub_path.replace('/', '\\')}
        }
        sg.update('PublishedFile', publish_id, publish_update)
        logger.info('%s has been published successfully!' % publish_name)
        if thumbnail_path:
            sg.upload_thumbnail('PublishedFile', publish_id, thumbnail_path)
            logger.info('Thumbnail uploaded from %s' % thumbnail_path)

        # Open the database
        f = open(db, 'r')
        read_db = js.load(f)
        read_db[project]['Assets'][asset].append(filename)
        s = open(db, 'w')
        save_jsn = js.dumps(read_db, sort_keys=True, indent=2, separators=(',', ': '))
        s.write(save_jsn)
        f.close()
        s.close()
        logger.info('JSON Database updated with new publish for %s' % publish_name)

    # ---------------------------------------------------------------------------------------------------------------
    # Create a Version
    # ---------------------------------------------------------------------------------------------------------------
    def version_file(self, **kwargs):
        """
        Publishes a version to Shotgun from a file dropped into the project asset folder
        :param kwargs: filename, project, asset, path
        :return: None
        """
        logger.info('Creating Version....')
        filename = kwargs['filename']
        project = kwargs['project']
        asset = kwargs['asset']
        path = kwargs['path']
        file_path = path + filename
        logger.info('Filename: %s' % filename)
        logger.info('Project: %s' % project)
        logger.info('Asset: %s' % asset)
        fixed_asset = asset.replace(' ', '-')
        fixed_filename = filename.replace(' ', '-')

        task = self.get_task(filename=filename, project=project, asset=asset)
        proj_id = task['proj_id']
        asset_id = task['asset_id']
        task_id = task['task_id']

        description = 'New version found in the remote folder.\nOriginal Filename: %s' % filename
        version_data = {
            'project': {'type': 'Project', 'id': proj_id },
            'description': description,
            'sg_status_list': 'rev',
            'code': filename,
            'entity': {'type': 'Asset', 'id': asset_id},
            'sg_task': {'type': 'Task', 'id': task_id}
        }

        # Open the database
        f = open(db, 'r')
        read_db = js.load(f)
        sg = Shotgun(shotgun_conf['url'], shotgun_conf['name'], shotgun_conf['key'])
        new_version = sg.create('Version', version_data)
        sg.upload_thumbnail('Version', new_version['id'], file_path)
        if '.mov' in filename or '.mp4' in filename or '.avi' in filename:
            sg.upload('Version', new_version['id'], file_path)

        # Add the file to the database
        read_db[project]['Assets'][asset].append(filename)
        s = open(db, 'w')
        save_jsn = js.dumps(read_db, sort_keys=True, indent=2, separators=(',', ': '))
        s.write(save_jsn)
        f.close()
        s.close()

    # ---------------------------------------------------------------------------------------------------------------
    # get a task
    # ---------------------------------------------------------------------------------------------------------------
    def get_task(self, filename=None, project=None, asset=None):
        """
        Return the ID numbers for a Project, Asset and Task
        :param filename: (str) name of the file being passed
        :param project:  (str) Project name
        :param asset:    (str) Asset Name
        :return: (dict) {'proj_id': 100, 'asset_id': 500, 'task_id': 10800}
        """
        logger.info('Retrieving Task Information....')
        fixed_asset = asset.replace(' ', '-')
        fixed_filename = filename.replace(' ', '-')
        sg = Shotgun(shotgun_conf['url'], shotgun_conf['name'], shotgun_conf['key'])

        # Open the database and get the project ID
        f = open(db, 'r')
        read_db = js.load(f)
        proj_id = read_db[project]['ID']
        asset_list = read_db[project]['Assets']

        # find the Asset ID
        asset_filter = [
            ['code', 'is', asset],
            ['project', 'is', {'type': 'Project', 'id': proj_id}]
        ]
        asset_fields = [
            'id',
            'sg_asset_type'
        ]
        find_asset = sg.find_one('Asset', asset_filter, asset_fields)
        asset_id = find_asset['id']
        asset_type = find_asset['sg_asset_type']

        # Check for a design.main task
        check_filters = [
            ['entity', 'is', {'type': 'Asset', 'id': asset_id}]
        ]
        check_fields = [
            'content', 'id', 'step'
        ]
        check_task = sg.find('Task', check_filters, check_fields)
        task_found = False
        for key in range(0, len(check_task)):
            if 'design.main' == check_task[key]['content']:
                task_found = True
                task_id = check_task[key]['id']
                break
        if not task_found:
            # Create new task
            step_filters = [
                ['code', 'is', 'design']
            ]
            step_fields = [
                'id'
            ]
            get_step = sg.find_one('Step', step_filters, step_fields)
            step_id = get_step['id']
            task_data = {
                'project': {'type': 'Project', 'id': proj_id},
                'content': 'design.main',
                'entity': {'type': 'Asset', 'id': asset_id},
                'step': {'type': 'Step', 'id': step_id}
            }
            new_task = sg.create('Task', task_data)
            task_id = new_task['id']
        if not task_id:
            return False
        task = {'proj_id': proj_id, 'asset_id': asset_id, 'task_id': task_id, 'asset_type': asset_type}
        logger.info('Task information returned: %s' % task)
        return task

    # ---------------------------------------------------------------------------------------------------------------
    # Check Project existence in JSON database
    # ---------------------------------------------------------------------------------------------------------------
    def check_project(self, name=None, id_num=None):
        if name:
            # Check for a projects existence in the Database
            f = open(db, 'r')
            f_list = js.load(f)
            f_projects = f_list.keys()
            if name in f_projects:
                in_db = True
            else:
                in_db = False
                logger.info('%s NOT found in database!' % name)
            folder = self.dropbox + '/' + name
            if os.path.exists(folder):
                in_folder = True
            else:
                in_folder = False
                logger.info('%s folder NOT in the Dropbox!' % name)
            if not in_db:
                in_db = self.add_project_to_database(name=name, id_num=id_num)
            if not in_folder:
                in_folder = self.add_project_to_folder(name=name)
            if in_folder and in_db:
                return True
            else:
                return False

    # ---------------------------------------------------------------------------------------------------------------
    # Add a missing project to the JSON Database
    # ---------------------------------------------------------------------------------------------------------------
    def add_project_to_database(self, name=None, id_num=None):
        f = open(db, 'r')
        jsn = js.load(f)
        # BUT with an Asset AND a series of files it would read:
        # {u'asura': {u'Remnant': ['file1_dsn_v01.psd', 'file2_concept_v02.jpg'], u'Sanctuary_Set': []}, u'nicole': {}}
        keys = jsn.keys()
        if name not in keys:
            jsn[name] = {'ID': id_num, 'Assets': {}}
        s = open(db, 'w')
        save_jsn = js.dumps(jsn, sort_keys=True, indent=2, separators=(',', ': '))
        s.write(save_jsn)
        logger.info('Added %s to the database' % name)
        return True

    # ---------------------------------------------------------------------------------------------------------------
    # Add a missing project to the folder structure
    # ---------------------------------------------------------------------------------------------------------------
    def add_project_to_folder(self, name=None):
        make_folder = self.dropbox + name
        os.mkdir(make_folder)
        if os.path.exists(make_folder):
            logger.info('%s folder created in %s' % (name, self.dropbox))
            return True
        else:
            logger.info('%s could not be created in %s' % (name, self.dropbox))
            return False

    # ---------------------------------------------------------------------------------------------------------------
    # Check asset's existence in DB and Folder structure
    # ---------------------------------------------------------------------------------------------------------------
    def check_asset(self, project=None, name=None, ass_id=None):
        f = open(db, 'r')
        jsn = js.load(f)
        ass_in_db = False
        for prj, ass in jsn.items():
            if name in ass['Assets']:
                ass_in_db = True
                break
        if not ass_in_db:
            logger.info('Asset %s not found in %s in the database' % (name, project))
            add_ass = self.add_asset_to_db(project=project, name=name, ass_id=ass_id)
        else:
            add_ass = False
        if add_ass:
            return True
        else:
            return False

    # ---------------------------------------------------------------------------------------------------------------
    # Add Asset to Database and Folder
    # ---------------------------------------------------------------------------------------------------------------
    def add_asset_to_db(self, project=None, name=None, ass_id=None):
        folder = self.dropbox + project + '/' + name
        if not os.path.exists(folder):
            os.mkdir(folder)
            logger.info('%s folder created' % folder)
        f = open(db, 'r')
        jsn = js.load(f)
        jsn[project]['Assets'][name] = []
        s = open(db, 'w')
        save_jsn = js.dumps(jsn, sort_keys=True, indent=2, separators=(',', ': '))
        s.write(save_jsn)
        logger.info('%s added to %s in the database' % (name, project))
        return True

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    run = RemoteAutoPublisher()
    run.show()
    sys.exit(app.exec_())
