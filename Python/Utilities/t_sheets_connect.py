import sys, os, platform, time
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
else:
    base = '/Volumes'
    env_user = 'USER'

# Build Shotgun connection string.  This will be obsolete in the main version
shotgun_conf = {
    'url':'https://asc.shotgunstudio.com',
    'name':'runThis',
    'key':'55b685383cfc7bfaad304dfd26d55a2685ee7e5efa03ca4f34408192b8ac288c'
    }

sg = sgtk.Shotgun(shotgun_conf['url'], shotgun_conf['name'], shotgun_conf['key'])

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

    def _send_to_tsheets(self, page=None, data=None):
        if page:
            if data:
                packed_data = json.dumps(data)
                request = urllib2.Request('%s%s' % (url, page), headers=headers, data=packed_data)
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
            subjob_request = urllib2.Request('%sjobcodes?%s' % (url, subjoblist), headers=headers)
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
        ts_projects = {}
        jobs_js = json.loads(urllib2.urlopen(self.jobs_request).read())
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
        sj_jobs_data = self.return_subs(project_id)
        if project_id:
            # Project ID from T-Sheets
            if __name__ == '__main__':
                for shot_asset in sj_jobs_data:
                    # This level only has Top Level categories: Assets, Design, Production Admin, Shots, VFX
                    sj_data = sj_jobs_data[shot_asset]
                    sj_name = sj_data['name']
                    sj_has_children = sj_data['has_children']
                    sj_id = sj_data['id']
                    if sj_name == 'Assets':
                        # List assets
                        if sj_has_children:
                            asset_children = self.return_subs(sj_id)
                            assets = {}
                            for asset_id, asset_data in asset_children.items():
                                # asset_id returns the ID of the asset child
                                asset_has_children = asset_data['has_children']
                                asset_name = asset_data['name']
                                asset_active = asset_data['active']
                                tasks = {}
                                if asset_has_children:
                                    # This will look for Tasks when and if they exist
                                    asset_tasks = self.return_subs(asset_id)
                                    for task_id, task_data in asset_tasks.items():
                                        task_name = task_data['name']
                                        task_active = task_data['active']
                                        tasks[task_id] = {'type': 'Asset_Task', 'name': task_name,
                                                          'active': task_active}
                                assets[asset_id] = {'type': 'Asset', 'name': asset_name, 'has_children': asset_has_children,
                                                    'active': asset_active, 'tasks': tasks}
                            subs[sj_id] = {'type': sj_name, 'data': assets}
                    elif sj_name == 'Shots':
                        # List Sequences.  Then sub and list shots
                        if sj_has_children:
                            # Return a list of sequences
                            sequence_data = self.return_subs(sj_id)
                            sequences = {}
                            for seq_id, seq_data in sequence_data.items():
                                # List the ID and Name of Sequences
                                seq_has_children = seq_data['has_children']
                                seq_name = seq_data['name']
                                seq_active = seq_data['active']
                                shots = {}
                                if seq_has_children:
                                    # This will find Shots
                                    shots_data = self.return_subs(seq_id)
                                    for shot_id, shot_data in shots_data.items():
                                        shot_has_children = shot_data['has_children']
                                        shot_name = shot_data['name']
                                        shot_active = shot_data['active']
                                        tasks = {}
                                        if shot_has_children:
                                            shot_tasks = self.return_subs(shot_id)
                                            for task_id, task_data in shot_tasks.items():
                                                task_name = task_data['name']
                                                task_active = task_data['active']
                                                tasks[task_id] = {'type': 'Shot_Task', 'name': task_name,
                                                                  'active': task_active}
                                        shots[shot_id] = {'type': 'Shot', 'name': shot_name, 'has_children': shot_has_children,
                                                          'active': shot_active, 'tasks': tasks}
                                sequences[seq_id] = {'type': 'Seq', 'name': seq_name, 'has_children': seq_has_children,
                                                     'active': seq_active, 'shots': shots}
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
        people = sg.find(entity_type='HumanUser', filters=[['sg_status_list', 'is', 'act']], fields=['email', 'name', 'sg_computer'])
        sg_users = {}
        for jerk in people:
            sg_users[jerk['email']] = {'name': jerk['name'], 'computer': jerk['sg_computer']}
        return sg_users

    def get_shotgun_projects(self):
        projects = {}
        find_projects = sg.find(entity_type='Project', filters=[['sg_status', 'is', 'Active']], fields=['id', 'name'])
        for project in find_projects:
            proj_data = project
            proj_id = proj_data['id']
            proj_name = proj_data['name']
            projects[proj_id] = proj_name
        return projects

    # Added 10-23-17
    def get_shotgun_sequence(self, project=None):
        print 'Return Shotgun Sequences for a particular project'
        if project:
            sequences = {}
            filters = [
                ['project', 'is', {'type': 'Project', 'id': project}]
            ]
            fields = [
                'code'
            ]
            find_seq = sg.find('Sequence', filters, fields)
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
        print 'Return active shots for a given project'
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
                find_shots = sg.find('Shot', filters, fields)
                for shot in find_shots:
                    shots[shot['id']] = {'shot': shot['code'], 'seq_id': sequence}
            return shots
        return False

    def get_ts_sequences(self, project_name=None):
        print 'get ts sequences'
        '''
        So, T-Sheets projects are basically just a JSON hierarchy.

        Project
            Design
            Production Admin
            Shots
                Seq #
                    Shot #
                        Task #
            Assets
                Asset #
                    Task #

        Thus...
        {'project': [ 'Design': [], 'Project Admin': [], 'Shots': ['Shot #': [Task #]], 'Asset': []'

        '''

    def compare_project_sequences(self, project=None):
        print 'Comparing Shotgun to T-Sheets Sequences...'
        if project:
            sequences = {}
            filters = [
                ['project', 'is', {'type': 'Project', 'id': project}]
            ]
            fields = ['code', 'id']
            find_sequences = sg.find('Sequence', filters=filters, fields=fields)
            for seq in find_sequences:
                sequences[seq['id']] = seq['code']
            return sequences
        return False

    # End ------------------------------------------------------------------------

    def get_shotgun_assets(self, project=None):
        print 'Return the assets associated with a particular project, or shot'
        if project:
            assets = {}
            filters = [
                ['project', 'is', {'type': 'Project', 'id': project}]
            ]
            fields = ['code', 'id']
            find_assets = sg.find('Asset', filters=filters, fields=fields)
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
                        for asset_id, asset_data in sub_data.items():
                            # Split up the sub_data
                            # asset_id = id number of the T-Sheets jobcode
                            # asset_data = Dictionary of values from the specific jobcode.
                            ts_assets[asset_id] = asset_data['name']

                    elif data_type == 'Shots':
                        # First up is sequences
                        for seq_id, seq_data in sub_data.items():
                            # Each sequence gets saved into the ts_seq dictionary
                            ts_seq[seq_id] = seq_data['name']

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
                            if ts_asset == sg_asset:
                                sg_asset_found = True
                                break
                        # Check if the asset is found
                        if not sg_asset_found:
                            # If the asset isn't found in T-Sheets, add it to the database
                            print 'FAIL!!! SHOTGUN ASSET NOT FOUND: %s' % sg_asset
                            print 'Sending to the function that will create the Asset in T-Sheets'

                if sg_project_seq:
                    # If there are sequences listed in Shotgun
                    if __name__ == '__main__':
                        for sg_seq_id, sg_seq in sg_project_seq.items():
                            # Set the sg_seq_found to False until a match is found
                            sg_seq_found = False
                            # Cycle through ts_seq to look for a match
                            for tsid, tsseq in ts_seq.items():
                                if tsseq == sg_seq:
                                    # If the sequence is found, search through for shots and set to True
                                    sg_seq_found = True
                                    sg_shots = self.get_shotgun_shots(project=sg_id, sequence=sg_seq_id)
                                    if sg_shots:
                                        for sg_shot_name in sg_shots.values():
                                            for tsshot, tsdata in ts_shots.items():
                                                # print 'test: %s, %s, %s' % (sg_seq, sg_shot_name, tsdata['shot'])
                                                if sg_seq == tsdata['seq_name'] and sg_shot_name['shot'] == tsdata['shot']:
                                                    print 'SHOTGUN SHOT %s FOUND IN T-Sheets!' % sg_shot_name
                                                    # break if the shot is found
                                                    break
                                    # break if the sequence is found
                                    break
                            if not sg_seq_found:
                                # If the sequence isn't found in T-Sheets, then add it to the database
                                # and then add any shots that may also exist in Shotgun
                                print 'Add shit to the database.'

                # ***************************************************************************************
                # END Shotgun to T-Sheets data comparison
                # ***************************************************************************************

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
                    print 'Shithead is not clocked in'
                    # For the moment, this may be how the test is achieve to trigger a different clock in response.
        return timesheet

    def add_new_ts_sequence(self, name=None, parent_id=None):
        print 'Add a new sequence from Shotgun. %s' % name
        # This may be done with the add_sub_folders() method
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
        packed_data = json.dumps(data)
        request = urllib2.Request('%sjobcodes' % url, headers=headers, data=packed_data)
        request.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(request)
        response_data = json.loads(response.read())
        check = response_data['results']['jobcodes']['1']['_status_message']
        new_id = response_data['results']['jobcodes']['1']['id']
        if check == 'Created':
            self.add_sub_folders(proj_id=new_id, sub_folder_name='Design')
            self.add_sub_folders(proj_id=new_id, sub_folder_name='Assets')
            self.add_sub_folders(proj_id=new_id, sub_folder_name='Shots')
            self.add_sub_folders(proj_id=new_id, sub_folder_name='Production Admin')
            return new_id
        return False

    def get_ts_authorization(self):
        filters = [
            ['id', 'is', 3]
        ]
        fields = [
            'code'
        ]
        auth_search = sg.find('CustomNonProjectEntity06', filters, fields)
        print auth_search

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


# ----------------------------------------------------------------------------------------------------------------------
# Test Triggers
# ----------------------------------------------------------------------------------------------------------------------
run = t_sheets_connect()

# out_data = run.get_ts_user_timesheet(email='adam@sdvfx.com')
# out_data = run.get_ts_user_timesheet(email='adamb@asc-vfx.com')
out_data = run.compare_active_projects()
# out_data = run.get_shotgun_sequence(168)
print out_data
# for sid, seq in out_data.items():
#     out_data2 = run.get_shotgun_shots(168, sid)
#     print out_data2

print os.environ['COMPUTERNAME']
