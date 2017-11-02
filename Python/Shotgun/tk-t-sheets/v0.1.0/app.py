# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.


from sgtk.platform import Application
import sgtk
import threading
import json
import urllib, urllib2
import sys, os, platform, time
import logging as logger
import subprocess
import re
from datetime import datetime, timedelta

# ----------------------------------------------------------------------------------------------------------------------
# Global Variables
# ----------------------------------------------------------------------------------------------------------------------

# Define system variables
osSystem = platform.system()

if osSystem == 'Windows':
    base = '//hal'
    env_user = 'USERNAME'
else:
    base = '/Volumes'
    env_user = 'USER'

url = 'https://rest.tsheets.com/api/v1/'

class t_sheets_connect(Application):
    """
    The app entry point. This class is responsible for intializing and tearing down
    the application, handle menu registration etc.
    """

    def init_app(self):
        """
        Called as the application is being initialized
        """
        
        # first, we use the special import_module command to access the app module
        # that resides inside the python folder in the app. This is where the actual UI
        # and business logic of the app is kept. By using the import_module command,
        # toolkit's code reload mechanism will work properly.
        app_payload = self.import_module("t_sheets")

        auth_id = 3
        auth_filters = [
            ['id', 'is', auth_id]
        ]
        auth_fields = ['code']

        engine = self.engine
        self.sg = engine.sgtk

        auth_data = self.sg.shotgun.find_one('CustomNonProjectEntity06', auth_filters, auth_fields)
        authorization = auth_data['code']

        self.headers = {
            'Authorization': 'Bearer %s' % authorization
        }

        # now register a *command*, which is normally a menu entry of some kind on a Shotgun
        # menu (but it depends on the engine). The engine will manage this command and 
        # whenever the user requests the command, it will call out to the callback.

        # first, set up our callback, calling out to a method inside the app module contained
        # in the python folder of the app
        menu_callback = lambda : app_payload.tsheets_dialog.show_dialog(self)

        # now register the command with the engine
        self.engine.register_command("T-Sheets Connection...", menu_callback)

        # Put this into a Thread so that it doesn't slow down other processes.
        check_projects = threading.Thread(name='CheckTSheetsProjects', target=self.compare_active_projects)
        check_projects.start()

    def _send_to_tsheets(self, page=None, data=None):
        if page:
            if data:
                packed_data = json.dumps(data)
                request = urllib2.Request('%s%s' % (url, page), headers=self.headers, data=packed_data)
                request.add_header('Content-Type', 'application/json')
                response = urllib2.urlopen(request)
                response_data = json.loads(response.read())
                return response_data
            else:
                return False
        else:
            return False

    def _return_from_tsheets(self, page=None, data=None):
        if page:
            if data:
                data_list = urllib.urlencode(data)
                request = urllib2.Request('%s%s?%s' % (url, page, data_list), headers=self.headers)
                response = urllib2.urlopen(request)
                response_data = json.loads(response.read())
                return response_data
            else:
                return False
        else:
            return False

    def return_subs(self, job_id=None):
        subjobsparams = {
            'per_page': '50',
            'parent_ids': job_id,
            'active': 'yes'
        }
        subjob_js = self._return_from_tsheets(page='jobcodes', data=subjobsparams)
        for sj_type, sj_result in subjob_js.items():
            if sj_type == 'results':
                sj_jobs_data = sj_result['jobcodes']
                return sj_jobs_data
        return False

    def get_ts_active_users(self):
        ts_users = {}
        user_params = {'per_page': '50', 'active': 'yes'}
        user_js = self._return_from_tsheets(page='users', data=user_params)
        if user_js:
            for l_type, result_data in user_js.items():
                if l_type == 'results':
                    user_data = result_data['users']
                    for user in user_data:
                        data = user_data[user]
                        first_name = data['first_name']
                        last_name = data['last_name']
                        email = data['email']
                        last_active = data['last_active']
                        active = data['active']
                        username = data['username']
                        user_id = data['id']
                        name = first_name, last_name
                        ts_users[email] = {'name': name, 'last_active': last_active, 'active': active,
                                           'username': username, 'email': email, 'id': user_id}
            return ts_users
        else:
            return False

    def get_ts_current_user_status(self, email=None):
        data = {}
        username = email
        # Send the Username from a script that already loads the shotgun data.  This returns the T-Sheets status of a
        # single user.
        all_users = self.get_ts_active_users()
        if username in all_users.keys():
            data = all_users[username]
        return data

    def get_ts_active_projects(self):
        jobs_params = {'active': 'yes'}
        jobs_js = self._return_from_tsheets(page='jobcodes', data=jobs_params)
        ts_projects = {}
        for j_type, result_data in jobs_js.items():
            if j_type == 'results':
                jobs_data = result_data['jobcodes']
                for project in jobs_data:
                    data = jobs_data[project]
                    has_children = data['has_children']
                    if has_children:
                        project_name = data['name']
                        project_id = data['id']
                        ts_projects[project_id] = project_name
        return ts_projects

    def get_ts_subs(self, project_id=None):
        sj_jobs_data = self.return_subs(project_id)
        for shot_asset in sj_jobs_data:
            sj_data = sj_jobs_data[shot_asset]
            sj_name = sj_data['name']
            if sj_name == 'VFX' or sj_name == 'Design' or sj_name == 'Shots':
                sj_has_children = sj_data['has_children']
                if sj_has_children:
                    sub2_id = sj_data['id']
                    sub2_data = self.return_subs(sub2_id)
                    for sub_asset in sub2_data:
                        sub_data = sub2_data[sub_asset]
                        sub_name = sub_data['name']
                        sub_id = sub_data['id']
                        sub_has_children = sub_data['has_children']
                        print '\t', sub_name
                        if sub_has_children:
                            print '+' * 150
                            sub3_data = self.return_subs(sub_id)
                            for sub3_asset in sub3_data:
                                sub3_d = sub3_data[sub3_asset]
                                sub3_name = sub3_d['name']
                                print '\t\t', sub3_name
                            print '~' * 150
        print '*' * 150

    def get_shotgun_people(self):
        """
        Collect all active Shotgun Users
        :return: (dict) sg_users[email] = {'name': name, 'computer': sg_computer}
        """
        people = self.sg.shotgun.find(entity_type='HumanUser', filters=[['sg_status_list', 'is', 'act']], fields=['email', 'name', 'sg_computer'])
        sg_users = {}
        for jerk in people:
            sg_users[jerk['email']] = {'name': jerk['name'], 'computer': jerk['sg_computer']}
        return sg_users

    def get_shotgun_projects(self):
        projects = {}
        find_projects = self.sg.shotgun.find(entity_type='Project', filters=[['sg_status', 'is', 'Active']], fields=['id', 'name'])
        for project in find_projects:
            proj_data = project
            proj_id = proj_data['id']
            proj_name = proj_data['name']
            projects[proj_id] = proj_name
        return projects

    def get_shotgun_shots(self, project=None):
        print 'Return active shots for a given project'

    def get_shotgun_assets(self, project=None, shot=None):
        print 'Return the assets associated with a particular project, or shot'

    def get_shotgun_tasks(asset=None, project=None, shot=None):
        print 'Return the Shotgun tasks'

    def compare_active_users(self):
        ts_users = self.get_ts_active_users()
        sg_users = self.get_shotgun_people()
        for sg_user in sg_users.keys():
            if sg_user in ts_users.keys():
                print 'USER FOUND: %s' % sg_users[sg_user]['name']
                print 'COMPUTER: %s' % sg_users[sg_user]['computer']

    def compare_active_projects(self):
        ts_projects = self.get_ts_active_projects()
        sg_projects = self.get_shotgun_projects()
        for ID, name in sg_projects.items():
            if name not in ts_projects.values():
                print 'PROJECT NOT FOUND! %s' % name
                self.add_new_ts_project(name=name)

    def get_ts_user_timesheet(self, email=None):
        timesheet = {}
        _start_date = datetime.date((datetime.today() - timedelta(days=2)))
        current_user = self.get_ts_current_user_status(email=email)
        username = current_user['username']
        name = (current_user['name'][0] + ' ' +  current_user['name'][1])
        first_name = current_user['name'][0]
        last_name = current_user['name'][1]
        ts_email = current_user['email']
        user_id = current_user['id']
        tsheet_param = {'start_date': _start_date, 'user_ids': user_id, 'on_the_clock': 'yes'}
        tsheets_json = self._return_from_tsheets(page='timesheets', data=tsheet_param)
        for type, data in tsheets_json.items():
            if type == 'results':
                ts_data = data.values()
                try:
                    for card, info in ts_data[0].items():
                        if info['on_the_clock']:
                            timesheet[card] = {'name': name, 'username': username, 'user_id': user_id, 'timecard': info}
                except AttributeError:
                    print 'Shithead is not clocked in'
                    # For the moment, this may be how the test is achieve to trigger a different clock in response.
        return timesheet

    def add_sub_folders(self, proj_id=None, sub_folder_name=None):
        print 'Add Sub Folders'
        data = {
            "data":
                [
                    {
                        "name": "%s" % sub_folder_name,
                        "billable": "yes",
                        "assigned_to_all": "yes",
                        "parent_id": "%s" % proj_id
                    }
                ]
        }
        response_data = self._send_to_tsheets(page='jobcodes', data=data)
        return response_data

    def collect_sg_sequences(self, project=None):
        print 'Collect Shotgun Sequences'
        if project:
            print 'hello'


    def collect_sg_shots(self, project=None, sequence=None):
        print 'Collect Shotgun Shots'

    def collect_sg_assets(self, project=None):
        print 'Collect Shotgun Assets'

    def add_new_ts_project(self, name=None):
        print 'Add a new job from Shotgun. %s' % name
        data = {
            "data":
                [
                    {
                        "name": "%s" % name,
                        "billable": "yes",
                        "assigned_to_all": "yes"
                    }
                ]
        }
        response_data = self._send_to_tsheets(page='jobcodes', data=data)
        new_id = response_data['results']['jobcodes']['1']['id']
        check = response_data['results']['jobcodes']['1']['_status_message']
        if check == 'Created':
            # Here we need to run build_sub_projects.  Some will be defaults, like Design or Production Admin
            design = self.add_sub_folders(proj_id=new_id, sub_folder_name='Design')
            prod_admin = self.add_sub_folders(proj_id=new_id, sub_folder_name='Production Admin')
            return True
        else:
            return False
