import sys, os, platform, time, getpass
import logging as logger
import subprocess
import re
from datetime import datetime, timedelta

import shotgun_api3 as sgtk

import json
import urllib, urllib2

# ----------------------------------------------------------------------------------------------------------------------
# Global Variables
# ----------------------------------------------------------------------------------------------------------------------

# Define system variables
osSystem = platform.system()

if osSystem == 'Windows':
    base = '//hal'
    env_user = 'USERNAME'
    computername = 'COMPUTERNAME'
else:
    base = '/Volumes'
    env_user = 'USER'
    computername = 'HOSTNAME'

# Build Shotgun connection string.  This will be obsolete in the main version
shotgun_conf = {
    'url':'https://asc.shotgunstudio.com',
    'name':'runThis',
    'key':'55b685383cfc7bfaad304dfd26d55a2685ee7e5efa03ca4f34408192b8ac288c'
    }


# T-Sheets Authorization.  This needs to be acquired from Shotgun.
authorization = 'S.4__b0c48a6b9e2e5bc810e2c402496f5549df7fb16a'

url = 'https://rest.tsheets.com/api/v1/'

headers = {
    'Authorization': 'Bearer %s' % authorization
}

user_params = {'per_page': '50', 'active': 'yes'}
jobs_params = {'active': 'yes'}


class t_sheets_connect:
    """
    Connect T-Sheets databases to Shotgun to compare projects, shots, designs and assets, and people
    """
    def __init__(self):
        self.jobs_list = urllib.urlencode(jobs_params)
        self.jobs_request = urllib2.Request('%sjobcodes?%s' % (url, self.jobs_list), headers=headers)

        self.sg = sgtk.Shotgun(shotgun_conf['url'], shotgun_conf['name'], shotgun_conf['key'])

        self.timezone = '-7:00'

    # ------------------------------------------------------------------------------------------------------------------
    # T-Sheets Web Connection IO
    # ------------------------------------------------------------------------------------------------------------------
    def _send_to_tsheets(self, page=None, data=None):
        if page:
            if data:
                try:
                    packed_data = json.dumps(data)
                    request = urllib2.Request('%s%s' % (url, page), headers=headers, data=packed_data)
                    request.add_header('Content-Type', 'application/json')
                    response = urllib2.urlopen(request)
                    response_data = json.loads(response.read())
                    return response_data
                except Exception, e:
                    print 'Web connection failed!  Error: %s' % e
            else:
                return False
        else:
            return False

    def _return_from_tsheets(self, page=None, data=None):
        if page:
            if data:
                try:
                    data_list = urllib.urlencode(data)
                    request = urllib2.Request('%s%s?%s' % (url, page, data_list), headers=headers)
                    response = urllib2.urlopen(request)
                    response_data = json.loads(response.read())
                    return response_data
                except Exception, e:
                    print 'Web Connection Failed!  Error: %s' % e
            else:
                return False
        else:
            return False

    def _edit_tsheets(self, page=None, data=None):
        if page:
            if data:
                try:
                    packed_data = json.dumps(data)
                    request = urllib2.Request('%s%s' % (url, page), headers=headers, data=packed_data)
                    request.add_header('Content-Type', 'application/json')
                    request.get_method = lambda: 'PUT'
                    response = urllib2.urlopen(request)
                    response_data = json.loads(response.read())
                    return response_data
                except Exception, e:
                    print 'Web Connection Failed! Error: %s' % e
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
            subjob_request = urllib2.Request('%sjobcodes?%s' % (url, subjoblist), headers=headers)
            subjob_js = json.loads(urllib2.urlopen(subjob_request).read())
            for sj_type, sj_result in subjob_js.items():
                if sj_type == 'results':
                    sj_jobs_data = sj_result['jobcodes']
                    return sj_jobs_data
            return False
        return False

    # ------------------------------------------------------------------------------------------------------------------
    # T-Sheets Jobcode Workers
    # ------------------------------------------------------------------------------------------------------------------
    def get_ts_active_projects(self):
        ts_projects = {}
        jobs_js = self._return_from_tsheets(page='jobcodes', data=jobs_params)
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
                                    shots[shot_id] = {'type': 'Shot', 'name': shot_name, 'has_children': shot_has_children,
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
        packed_data = json.dumps(data)
        request = urllib2.Request('%sjobcodes' % url, headers=headers, data=packed_data)
        request.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(request)
        response_data = json.loads(response.read())
        check = response_data['results']['jobcodes']['1']['_status_message']
        new_id = response_data['results']['jobcodes']['1']['id']
        if check == 'Created':
            self.add_sub_folders(parent_id=new_id, sub_folder_name='Design')
            self.add_sub_folders(parent_id=new_id, sub_folder_name='Assets')
            self.add_sub_folders(parent_id=new_id, sub_folder_name='Shots')
            self.add_sub_folders(parent_id=new_id, sub_folder_name='Production Admin')
            return new_id
        return False

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

    def get_ts_jobcode(self, jobcode=None):
        # print 'Get Jobcode %s' % jobcode
        jobcode_data = {}
        if jobcode:
            data = {'ids': jobcode}
            get_jobcode = self._return_from_tsheets(page='jobcodes', data=data)
            for keys in get_jobcode:
                if keys == 'results':
                    job_data = get_jobcode[keys]['jobcodes']
                    for job_id, job_info in job_data.items():
                        jobid = job_id
                        job_tasks = job_info['filtered_customfielditems'].keys()[0]
                        job_name = job_info['name']
                        has_children = job_info['has_children']
                        parent_id = job_info['parent_id']
                        jobcode_data[jobid] = {'tasks': job_tasks, 'name': job_name, 'has_children': has_children,
                                               'parent_id': parent_id}
        return jobcode_data

    # ------------------------------------------------------------------------------------------------------------------
    # Shotgun Projects, Assets, Sequences & Shots Workers
    # ------------------------------------------------------------------------------------------------------------------
    def get_shotgun_projects(self):
        projects = {}
        find_projects = self.sg.find(entity_type='Project', filters=[['sg_status', 'is', 'Active']], fields=['id', 'name'])
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
            find_seq = self.sg.find('Sequence', filters, fields)
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
                find_shots = self.sg.find('Shot', filters, fields)
                for shot in find_shots:
                    shots[shot['id']] = {'shot': shot['code'], 'seq_id': sequence}
            return shots
        return False

    def get_shotgun_assets(self, project=None):
        # print 'Return the assets associated with a particular project, or shot'
        if project:
            assets = {}
            filters = [
                ['project', 'is', {'type': 'Project', 'id': project}]
            ]
            fields = ['code', 'id']
            find_assets = self.sg.find('Asset', filters=filters, fields=fields)
            for asset in find_assets:
                assets[asset['id']] = asset['code']
            return assets
        return False

    def get_shotgun_tasks(asset=None, project=None, shot=None):
        print 'Return the Shotgun tasks'

    # ------------------------------------------------------------------------------------------------------------------
    # Shotgun to T-Sheets Project, Asset, Shots and Jobcodes Workers
    # ------------------------------------------------------------------------------------------------------------------
    def compare_project_sequences(self, project=None):
        # print 'Comparing Shotgun to T-Sheets Sequences...'
        if project:
            sequences = {}
            filters = [
                ['project', 'is', {'type': 'Project', 'id': project}]
            ]
            fields = ['code', 'id']
            find_sequences = self.sg.find('Sequence', filters=filters, fields=fields)
            for seq in find_sequences:
                sequences[seq['id']] = seq['code']
            return sequences
        return False

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

    # ------------------------------------------------------------------------------------------------------------------
    # Shotgun and T-Sheets User Information
    # ------------------------------------------------------------------------------------------------------------------
    def get_shotgun_people(self):
        """
        Collect all active Shotgun Users
        :return: (dict) sg_users[email] = {'name': name, 'computer': sg_computer}
        """
        people = self.sg.find(entity_type='HumanUser', filters=[['sg_status_list', 'is', 'act']], fields=['email', 'name', 'sg_computer'])
        sg_users = {}
        for jerk in people:
            sg_users[jerk['email']] = {'name': jerk['name'], 'computer': jerk['sg_computer']}
        return sg_users

    def get_sg_user(self, userid=None, name=None, email=None, sg_login=None, sg_computer=None):
        """
        Get a specific Shotgun User's details from any basic input.
        Only the first detected value will be searched.  If all 3 values are added, only the ID will be searched.
        :param userid: (int) Shotgun User ID number
        :param name:   (str) First and Last Name
        :param email:  (str) email@asc-vfx.com
        :return: user: (dict) Basic details
        """

        user = {}
        if userid or name or email or sg_login or sg_computer:
            filters = [
                ['sg_status_list', 'is', 'act']
            ]
            if userid:
                filters.append(['id', 'is', userid])
            elif name:
                filters.append(['name', 'is', name])
            elif email:
                filters.append(['email', 'is', email])
            elif sg_login:
                filters.append(['login', 'is', sg_login])
            elif sg_computer:
                filters.append(['sg_computer', 'is', sg_computer])
            fields = [
                'email',
                'name',
                'sg_computer',
                'login',
                'permission_rule_set',
                'projects',
                'groups'
            ]
            find_user = self.sg.find_one('HumanUser', filters, fields)
            if find_user:
                user_id = find_user['id']
                sg_email = find_user['email']
                computer = find_user['sg_computer']
                sg_name = find_user['name']
                # Dictionary {'type': 'PermissionRuleSet', 'id': 8 'name': 'Artist'}
                permissions = find_user['permission_rule_set']
                # List of Dictionaries [{'type': 'Group', 'id': 7, 'name':'VFX'}]
                groups = find_user['groups']
                login = find_user['login']
                # List of Dictionaries [{'type': 'Project', 'id': 168, 'name': 'masterTemplate'}]
                projects = find_user['projects']

                user[user_id] = {'name': sg_name, 'email': sg_email, 'computer': computer, 'permissions': permissions,
                                 'groups': groups, 'login': login, 'project': projects}
        return user

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

    def compare_active_users(self):
        ts_users = self.get_ts_active_users()
        sg_users = self.get_shotgun_people()
        for sg_user in sg_users.keys():
            if sg_user in ts_users.keys():
                print 'USER FOUND: %s' % sg_users[sg_user]['name']
                print 'COMPUTER: %s' % sg_users[sg_user]['computer']

    def get_sg_people_from_department(self, grp_id=None):
        """
        This will return a list of people associated with a given group.
        :param          dept:           (str) Department code
        :return:        people:         (dict) List of people associated with a department
        """
        people = {}
        if grp_id:
            filters = [
                ['id', 'is', grp_id]
            ]
            fields = [
                'users'
            ]
            find_people = self.sg.find_one('Department', filters, fields)
            if find_people:
                data = find_people['users']
                for user in data:
                    people[user['id']] = user['name']
        return people

    def confirm_user(self):
        current_user = os.environ[env_user]
        current_comp = os.environ[computername]
        confirmed_user = False
        get_current_user = self.get_sg_user(sg_login=current_user)
        get_current_computer = self.get_sg_user(sg_computer=current_comp)
        if get_current_computer == get_current_user:
            user_data = get_current_user.values()[0]
            user_email = user_data['email']
            user_name = user_data['name']
            get_ts_user = self.get_ts_current_user_status(email=user_email)
            if get_ts_user:
                ts_user = '%s %s' % (get_ts_user['name'][0], get_ts_user['name'][1])
                if user_name == ts_user:
                    confirmed_user = get_ts_user
        return confirmed_user

    # ------------------------------------------------------------------------------------------------------------------
    # T-Sheets Timesheet Workers
    # ------------------------------------------------------------------------------------------------------------------
    def get_iso_timestamp(self):
        iso_date = datetime.date(datetime.now()).isoformat()
        iso_time = '%02d:%02d:%02d' % (datetime.now().hour, datetime.now().minute, datetime.now().second)
        iso_tz = self.timezone
        clock_out = iso_date + 'T' + iso_time + iso_tz
        return clock_out

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
        tsheet_list = urllib.urlencode(tsheet_param)
        tsheets_request = urllib2.Request('%stimesheets?%s' % (url, tsheet_list), headers=headers)
        tsheets_json = json.loads(urllib2.urlopen(tsheets_request).read())
        for type, data in tsheets_json.items():
            if type == 'results':
                ts_data = data.values()
                try:
                    for card, info in ts_data[0].items():
                        if info['on_the_clock']:
                            timesheet[card] = {'name': name, 'username': username, 'user_id': user_id, 'timecard': info}
                except AttributeError:
                    # User Not clocked in
                    pass
        return timesheet

    def check_sg_timesheet_status(self):
        confirmed_user = self.confirm_user()
        if confirmed_user:
            user_timesheet = self.get_ts_user_timesheet(email=confirmed_user['username'])
            context = self.get_sg_current_context()
            if user_timesheet:
                new_ts = False
                # timesheet_id is for changing the timesheet if it turns out that it ain't the same.
                timesheet_id = user_timesheet.keys()[0]
                timesheet_data = user_timesheet.values()[0]
                jobcode = timesheet_data['timecard']['jobcode_id']
                # Get jobcode_id from T-Sheets. This includes the job name which can be compared to shotgun
                jobcode_data = self.get_ts_jobcode(jobcode=jobcode)
                ctx_name = context[context.keys()[0]]['name']
                ctx_task = context[context.keys()[0]]['task']
                ts_name = jobcode_data[jobcode_data.keys()[0]]['name']
                ts_task = jobcode_data[jobcode_data.keys()[0]]['tasks']
                ts_job_task = timesheet_data['timecard']['customfields'][ts_task]
                tran_task = self.get_sg_translator(sg_task=ctx_task)['task']
                if ctx_name == ts_name:
                    if tran_task != ts_job_task:
                        new_ts = True
                else:
                    new_ts = True

                if new_ts:
                    # This will actually need to go into the User Interface before calling
                    self.change_ts_timesheet(timesheet_id=timesheet_id, ctx=context, jobcode_id=jobcode)
            else:
                # This will actually need to go into the User Interface before calling
                self.clock_in_ts_timesheet(ctx=context)

    def change_ts_timesheet(self, timesheet_id=None, ctx=None, jobcode_id=None):
        new_ts = {}
        confirmed_user = self.confirm_user()
        if confirmed_user:
            if timesheet_id and ctx:
                user_email = confirmed_user['username']
                current_timesheet = self.get_ts_user_timesheet(email=user_email)
                end_time = current_timesheet[current_timesheet.keys()[0]]['timecard']['end']
                if not end_time:
                    clock_out_timesheet = self.clock_out_ts_timesheet(timesheet_id=timesheet_id, jobcode_id=jobcode_id)
                    if clock_out_timesheet:
                        clock_in_timesheet = self.clock_in_ts_timesheet(ctx=ctx)
                        if clock_in_timesheet:
                            if clock_in_timesheet['results']['timesheets']['1']['_status_message'] == 'Created':
                                new_ts = True
        return new_ts

    def clock_in_ts_timesheet(self, ctx=None):
        """
        Clock_in_ts_timesheet is going to be a little tricky.
        It will have to split out the context, and then find the jobcode_id based on the project, shot/asset & job task.
        The user_id, start time and other things will have to be collected as well.
        :param ctx:
        :return:
        """
        new_ts = {}
        confirmed_user = self.confirm_user()
        if confirmed_user:
            if ctx:
                print ctx
                user_id = confirmed_user['id']
                start = self.get_iso_timestamp()
                project_id = ctx.keys()[0]
                ctx_data = ctx[project_id]
                project = ctx_data['project']
                project_jobcode = None
                task = ctx_data['task']
                shot_or_asset = ctx_data['name']
                context = ctx_data['context']
                if context == 'Asset':
                    ts_folder = 'Assets'
                elif context == 'Shot':
                    ts_folder = 'Shots'
                ts_projects = self.get_ts_active_projects()
                for pid, proj in ts_projects.items():
                    if proj == project:
                        project_jobcode = pid
                        break

                print user_id
                print start
        return new_ts

    def clock_out_ts_timesheet(self, timesheet_id=None, jobcode_id=None):
        print 'START'
        confirm_user = self.confirm_user()
        print 'Confirmed User 3', confirm_user
        user_email = confirm_user['username']
        print 'Confirmed_user Email', user_email
        clocked_out = False
        # current_timesheet = self.get_ts_user_timesheet(email=user_email)
        if confirm_user:
            clock_out = self.get_iso_timestamp()
            print 'clock_out', clock_out
            data = {
                "data":
                    [
                        {
                            "id": int(timesheet_id),
                            "end": "%s" % clock_out,
                            "jobcode_id": int(jobcode_id)
                        }
                    ]
            }
            print 'Send to _edit_tsheets'
            success = self._edit_tsheets(page='timesheets', data=data)
            print 'RETURN from _edit_tsheets', success
            if success:
                if success['results']['timesheets']['1']['_status_message'] == 'Updated':
                    clocked_out = True

        return clocked_out

    # ------------------------------------------------------------------------------------------------------------------
    # Shotgun to T-Sheets Job Task Workers
    # ------------------------------------------------------------------------------------------------------------------
    def get_ts_job_tasks(self):
        pass

    def get_sg_current_context(self):
        context = {}
        # Temporary context info until I can get Shotgun connected.  This is just junk for testing purposes.
        # This will return the taks name, shot/asset name, which may take some fanegeling on T-Sheets part.
        context[140] = {
            'task': 'model.main',
            'context': 'Asset',
            'name': 'Remnant',
            'project': 'Asura'
        }
        return context

    def get_sg_translator(self, sg_task=None):
        """
        The T-Sheets Translator requires a special Shotgun page to be created.
        The fields in the database are as follows:
        Database Name:  code:                (str) A casual name of the database.
        sgtask:         sg_sgtask:          (str-unique) The shotgun task. Specifically, '.main' namespaces are removed.
        tstask:         sg_tstask:          (str) The T-Sheets name for a task
        ts_short_code:  sg_ts_short_code:   (str) The ironically long name for a 3 letter code.
        task_depts:     sg_task_grp:        (multi-entity) Returns the groups that are associated with tasks
        people_override:sg_people_override: (multi-entity) Returns individuals assigned to specific tasks

         :param:        sg_task:            (str) Shotgun task name from context
        :return:        translation:        (dict) {
                                                    task: sg_tstask
                                                    short: sg_ts_short_code
                                                    dept: sg_task_depts
                                                    people: sg_people_override
                                                    }
        """
        translation = {}
        if sg_task:
            if '.main' in sg_task:
                task_name = sg_task.replace('.main', '')
            else:
                task_name = sg_task

            task_name = task_name.lower()

            filters = [
                ['sg_sgtask', 'is', task_name]
            ]
            fields = [
                'sg_sgtask',
                'sg_tstask',
                'sg_ts_short_code',
                'sg_task_grp',
                'sg_people_override'
            ]
            translation_data = self.sg.find_one('CustomNonProjectEntity07', filters, fields=fields)

            if translation_data:
                task = translation_data['sg_tstask']
                short = translation_data['sg_ts_short_code']
                group = translation_data['sg_task_grp']
                people = translation_data['sg_people_override']
                translation = {'task': task, 'short': short, 'group': group, 'people': people}
        return translation

# ----------------------------------------------------------------------------------------------------------------------
# Test Triggers
# ----------------------------------------------------------------------------------------------------------------------
run = t_sheets_connect()

# out_data = run.get_ts_user_timesheet(email='adam@sdvfx.com')
# out_data = run.get_ts_user_timesheet(email='adamb@asc-vfx.com')
# out_data = run.compare_active_projects()
# out_data = run.get_shotgun_sequence(168)
# out_data = run.get_sg_translator('model.main')
# out_data = run.get_sg_user(sg_login='Adam')
out_data = run.check_sg_timesheet_status()
print out_data
# for sid, seq in out_data.items():
#     out_data2 = run.get_shotgun_shots(168, sid)
#     print out_data2

# print os.environ['COMPUTERNAME']
# print os.environ['USERNAME']
print getpass.getuser()
