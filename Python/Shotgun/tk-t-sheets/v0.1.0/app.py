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
        menu_callback = lambda: app_payload.tsheets_dialog.show_dialog(self)

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
        # this returns all children of a parent job id.  It does not return sub-children.
        if job_id:
            subjobsparams = {
                'parent_ids': job_id,
                'active': 'yes'
            }
            subjoblist = urllib.urlencode(subjobsparams)
            subjob_request = urllib2.Request('%sjobcodes?%s' % (url, subjoblist), headers=self.headers)
            subjob_js = json.loads(urllib2.urlopen(subjob_request).read())
            for sj_type, sj_result in subjob_js.items():
                if sj_type == 'results':
                    sj_jobs_data = sj_result['jobcodes']
                    return sj_jobs_data
            return False
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
        subs = {}
        if project_id:
            sj_jobs_data = self.return_subs(project_id)
            # Project ID from T-Sheets
            for shot_asset in sj_jobs_data:
                # This level only has Top Level categories: Assets, Design, Production Admin, Shots, VFX
                sj_data = sj_jobs_data[shot_asset]
                sj_name = sj_data['name']
                sj_has_children = sj_data['has_children']
                sj_id = sj_data['id']
                if sj_name == 'Assets':
                    assets = {}
                    # List assets
                    if sj_has_children:
                        asset_children = self.return_subs(sj_id)
                        for asset_id, asset_data in asset_children.items():
                            # asset_id returns the ID of the asset child
                            asset_has_children = asset_data['has_children']
                            asset_name = asset_data['name']
                            asset_active = asset_data['active']
                            asset_parent_id = asset_data['parent_id']
                            tasks = {}
                            if asset_has_children:
                                # This will look for Tasks when and if they exist
                                asset_tasks = self.return_subs(asset_id)
                                for task_id, task_data in asset_tasks.items():
                                    task_name = task_data['name']
                                    task_active = task_data['active']
                                    tasks[task_id] = {'type': 'Asset_Task', 'name': task_name,
                                                      'active': task_active}
                            assets[asset_id] = {'type': 'Asset', 'name': asset_name,
                                                'has_children': asset_has_children,
                                                'active': asset_active, 'tasks': tasks,
                                                'parent_id': asset_parent_id}
                        subs[sj_id] = {'type': sj_name, 'data': assets}
                    else:
                        subs[sj_id] = {'type': sj_name, 'data': assets}
                elif sj_name == 'Shots':
                    sequences = {}
                    # List Sequences.  Then sub and list shots
                    if sj_has_children:
                        # Return a list of sequences
                        sequence_data = self.return_subs(sj_id)
                        for seq_id, seq_data in sequence_data.items():
                            # List the ID and Name of Sequences
                            seq_has_children = seq_data['has_children']
                            seq_name = seq_data['name']
                            seq_active = seq_data['active']
                            seq_parent_id = seq_data['parent_id']
                            shots = {}
                            if seq_has_children:
                                # This will find Shots
                                shots_data = self.return_subs(seq_id)
                                for shot_id, shot_data in shots_data.items():
                                    shot_has_children = shot_data['has_children']
                                    shot_name = shot_data['name']
                                    shot_active = shot_data['active']
                                    shot_parent_id = shot_data['parent_id']
                                    tasks = {}
                                    if shot_has_children:
                                        shot_tasks = self.return_subs(shot_id)
                                        for task_id, task_data in shot_tasks.items():
                                            task_name = task_data['name']
                                            task_active = task_data['active']
                                            tasks[task_id] = {'type': 'Shot_Task', 'name': task_name,
                                                              'active': task_active}
                                    shots[shot_id] = {'type': 'Shot', 'name': shot_name,
                                                      'has_children': shot_has_children,
                                                      'active': shot_active, 'tasks': tasks,
                                                      'parent_id': shot_parent_id}
                            sequences[seq_id] = {'type': 'Seq', 'name': seq_name, 'has_children': seq_has_children,
                                                 'active': seq_active, 'shots': shots, 'parent_id': seq_parent_id}
                        subs[sj_id] = {'type': sj_name, 'data': sequences}
                    else:
                        subs[sj_id] = {'type': sj_name, 'data': sequences}
                elif sj_name == 'Design' or sj_name == 'VFX':
                    # I think we'll pass this up
                    pass
            return subs
        return False

    def get_shotgun_people(self):
        """
        Collect all active Shotgun Users
        :return: (dict) sg_users[email] = {'name': name, 'computer': sg_computer}
        """
        people = self.sg.shotgun.find(entity_type='HumanUser', filters=[['sg_status_list', 'is', 'act']],
                                      fields=['email', 'name', 'sg_computer'])
        sg_users = {}
        for jerk in people:
            sg_users[jerk['email']] = {'name': jerk['name'], 'computer': jerk['sg_computer']}
        return sg_users

    def get_shotgun_projects(self):
        projects = {}
        find_projects = self.sg.shotgun.find(entity_type='Project', filters=[['sg_status', 'is', 'Active']],
                                             fields=['id', 'name'])
        for project in find_projects:
            proj_data = project
            proj_id = proj_data['id']
            proj_name = proj_data['name']
            projects[proj_id] = proj_name
        return projects

    def get_shotgun_sequence(self, project=None):
        # print 'Return Shotgun Sequences for a particular project'
        if project:
            sequences = {}
            filters = [
                ['project', 'is', {'type': 'Project', 'id': project}]
            ]
            fields = [
                'code'
            ]
            find_seq = self.sg.shotgun.find('Sequence', filters, fields)
            for seq in find_seq:
                sequences[seq['id']] = seq['code']
            return sequences
        return False

    def get_shotgun_shots(self, project=None, sequence=None):
        """

        :param project: (int) project ID number
        :param sequence: (int) sequence ID number
        :return: shots: (dict) { shot_id: {'shot': shotname, 'seq_id': sequence ID}
        """
        # print 'Return active shots for a given project'
        if project and sequence:
            shots = {}
            if sequence:
                filters = [
                    ['project', 'is', {'type': 'Project', 'id': project}],
                    ['sg_sequence', 'is', {'type': 'Sequence', 'id': sequence}]
                ]
                fields = [
                    'code'
                ]
                find_shots = self.sg.shotgun.find('Shot', filters, fields)
                for shot in find_shots:
                    shots[shot['id']] = {'shot': shot['code'], 'seq_id': sequence}
            return shots
        return False

    def compare_project_sequences(self, project=None):
        # print 'Comparing Shotgun to T-Sheets Sequences...'
        if project:
            sequences = {}
            filters = [
                ['project', 'is', {'type': 'Project', 'id': project}]
            ]
            fields = ['code', 'id']
            find_sequences = self.sg.shotgun.find('Sequence', filters=filters, fields=fields)
            for seq in find_sequences:
                sequences[seq['id']] = seq['code']
            return sequences
        return False

    def get_shotgun_assets(self, project=None):
        # print 'Return the assets associated with a particular project, or shot'
        if project:
            assets = {}
            filters = [
                ['project', 'is', {'type': 'Project', 'id': project}]
            ]
            fields = ['code', 'id']
            find_assets = self.sg.shotgun.find('Asset', filters=filters, fields=fields)
            for asset in find_assets:
                assets[asset['id']] = asset['code']
            return assets
        return False

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
        # Loop Shotgun Projects
        for sg_id, name in sg_projects.items():
            # Loop ts projects to match to current sg project
            for ts_id, ts_name in ts_projects.items():
                ts_project_id = None
                if name == ts_name:
                    # Project found!  Collect ID number
                    ts_project_id = ts_id
                    break

            if not ts_project_id:
                # If no project is matched, the ID should still be empty.  Create new project in T-Sheets
                add_project = self.add_new_ts_project(name=name)
                ts_project_id = add_project

            # Check sg assets against ts assets
            sg_project_assets = self.get_shotgun_assets(project=sg_id)
            sg_project_seq = self.get_shotgun_sequence(project=sg_id)
            # After get_shotgun_sequence() call each shot from within the sequence loop.

            # ts_project_jobcodes contains the ID for both the 'Assets' and 'Shots' folders in the keys
            ts_project_jobcodes = self.get_ts_subs(project_id=ts_project_id)

            # ==========================================================================
            # Package TS Jobcodes into dictionaries for processing
            # ==========================================================================
            if ts_project_jobcodes:
                # Confirm that ts_project_jobcodes
                # Prep storage dictionaries
                ts_assets = {}
                ts_seq = {}
                ts_shots = {}
                for base_id, data in ts_project_jobcodes.items():
                    # Split up ts_project_jobcodes
                    # The base ID is the ID number of the jobcode return the data
                    # data is a dictionary of information about the jobcode.

                    # data_type = 'Asset', 'Shots', 'Production Admin'
                    # sub_data = is a dictionary of Assets, Shots or Sequences from T-Sheets
                    data_type = data['type']
                    sub_data = data['data']

                    if data_type == 'Assets':
                        assets_folder_id = base_id
                        for asset_id, asset_data in sub_data.items():
                            # Split up the sub_data
                            # asset_id = id number of the T-Sheets jobcode
                            # asset_data = Dictionary of values from the specific jobcode.
                            ts_assets[asset_id] = {'asset': asset_data['name'], 'parent_id': asset_data['parent_id']}

                    elif data_type == 'Shots':
                        shots_folder_id = base_id
                        # First up is sequences
                        for seq_id, seq_data in sub_data.items():
                            # Each sequence gets saved into the ts_seq dictionary
                            ts_seq[seq_id] = {'seq': seq_data['name'], 'parent_id': seq_data['parent_id']}

                            # Cycle through sequence data to collect and package shots associated with each sequence
                            for shot_id, shot_data in seq_data['shots'].items():
                                # seq_data['shots'] is a dictionary that contains shots for a given sequence
                                # package that data into the ts_shots dictionary
                                ts_shots[shot_id] = {'seq_id': seq_id, 'seq_name': seq_data['name'],
                                                     'shot': shot_data['name']}

                # ***************************************************************************************
                # Compare SG data to TS data and perform additions if items are missing.
                # ***************************************************************************************
                if sg_project_assets:
                    # if there are Assets listed in Shotgun
                    for sg_asset_id, sg_asset in sg_project_assets.items():
                        # set the sg_asset_found to False until a match is found.
                        sg_asset_found = False
                        for ts_asset in ts_assets.values():
                            # Cycling through the assets in the ts_asset dictionary. If a match is found, set to True
                            if ts_asset['asset'] == sg_asset:
                                sg_asset_found = True
                                break
                        # Check if the asset is found
                        if not sg_asset_found:
                            # print 'sg_asset_found = FALSE'
                            # If the asset isn't found in T-Sheets, add it to the database
                            self.add_sub_folders(parent_id=assets_folder_id, sub_folder_name=sg_asset)

                if sg_project_seq:
                    # If there are sequences listed in Shotgun
                    for sg_seq_id, sg_seq in sg_project_seq.items():
                        # Set the sg_seq_found to False until a match is found
                        sg_seq_found = False
                        # Cycle through ts_seq to look for a match
                        for tsid, tsseq in ts_seq.items():
                            if tsseq['seq'] == sg_seq:
                                # If the sequence is found, search through for shots and set to True
                                sg_seq_found = True
                                sg_shots = self.get_shotgun_shots(project=sg_id, sequence=sg_seq_id)
                                if sg_shots:
                                    for sg_shot_name in sg_shots.values():
                                        sg_shot_found = False
                                        for tsshot, tsdata in ts_shots.items():
                                            # print 'test: %s, %s, %s' % (sg_seq, sg_shot_name, tsdata['shot'])
                                            if sg_seq == tsseq['seq'] and sg_shot_name['shot'] == tsdata['shot']:
                                                # Set True and break if the shot is found
                                                # print 'Shot Found: %s' % sg_shot_name['shot']
                                                sg_shot_found = True
                                                break

                                        # The reason this won't work is taht tsdata['seq_name'] is already looped out.
                                        if sg_seq == tsseq['seq'] and not sg_shot_found:
                                            # Add the shot to the T-Sheets DB
                                            # print 'Sequence found, but shot not found!'
                                            # print 'sg_seq: %s | tsseq["seq"]: %s | sg_shot_name["shot"]: %s' % (sg_seq, tsseq['seq'], sg_shot_name['shot'])
                                            # print '=' * 150
                                            self.add_sub_folders(parent_id=tsid,
                                                                 sub_folder_name=sg_shot_name['shot'])

                                # break if the sequence is found
                                break
                        if not sg_seq_found:
                            # If the sequence isn't found in T-Sheets, then add it to the database
                            # and then add any shots that may also exist in Shotgun
                            # print 'sg_seq_found = FALSE | %s' % sg_seq
                            new_seq_id = self.add_sub_folders(parent_id=shots_folder_id,
                                                              sub_folder_name=sg_seq)
                            sg_shots = self.get_shotgun_shots(project=sg_id, sequence=sg_seq_id)
                            new_id = new_seq_id['results']['jobcodes']['1']['id']
                            # print 'NEW SEQUENCE ID: %s' % new_id
                            if new_id:
                                if sg_shots:
                                    for sg_shot_name in sg_shots.values():
                                        # print 'Adding shot for new sequence %s' % sg_seq
                                        self.add_sub_folders(parent_id=new_id, sub_folder_name=sg_shot_name['shot'])

                                        # ***************************************************************************************
                                        # END Shotgun to T-Sheets data comparison
                                        # ***************************************************************************************

    def get_ts_user_timesheet(self, email=None):
        timesheet = {}
        _start_date = datetime.date((datetime.today() - timedelta(days=2)))
        current_user = self.get_ts_current_user_status(email=email)
        username = current_user['username']
        name = (current_user['name'][0] + ' ' + current_user['name'][1])
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

    def add_sub_folders(self, parent_id=None, sub_folder_name=None):
        # print 'Add Sub Folders: %s' % sub_folder_name
        # print 'parent_id: %s' % parent_id
        # print '-' * 150
        data = {
            "data":
                [
                    {
                        "name": "%s" % sub_folder_name,
                        "billable": "yes",
                        "assigned_to_all": "yes",
                        "parent_id": "%s" % parent_id
                    }
                ]
        }
        response_data = self._send_to_tsheets(page='jobcodes', data=data)
        return response_data

    def add_new_ts_project(self, name=None):
        # print 'Add a new job from Shotgun. %s' % name
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
            self.add_sub_folders(parent_id=new_id, sub_folder_name='Design')
            self.add_sub_folders(parent_id=new_id, sub_folder_name='Assets')
            self.add_sub_folders(parent_id=new_id, sub_folder_name='Shots')
            self.add_sub_folders(parent_id=new_id, sub_folder_name='Production Admin')
            return new_id
        return False
