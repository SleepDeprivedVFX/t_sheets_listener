
__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.5.1'

import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
from dateutil import parser
from dateutil import relativedelta
import time
import inspect
import requests
import json


class comm_sys(object):
    def __init__(self, sg=None, config=None, sub=None):
        self.sg = sg
        self.config = config

        # Get Slack Authorizations
        done_auth_id = int(self.config['slack_id'])
        done_auth_filters = [
            ['id', 'is', done_auth_id]
        ]
        auth_fields = ['code', 'sg_url']
        # sg = Shotgun(shotgun_conf['url'], shotgun_conf['name'], shotgun_conf['key'])
        get_done_auth = sg.find_one(self.config['slack_entity'], done_auth_filters, auth_fields)
        self.auth_code = get_done_auth['code']
        self.slack_url = get_done_auth['sg_url']

        # ------------------------------------------------------------------------------------------------------
        # Create logging system
        # ------------------------------------------------------------------------------------------------------
        # Find out if the logger already exists.  If not, open a file.
        log_file = 'comm_sys.log'
        if sub:
            new_name = '%s_%s' % (sub, log_file)
            log_file = new_name
        log_root = os.path.join(sys.path[0], 'logs')
        if not os.path.exists(log_root):
            os.makedirs(log_root)
        log_path = os.path.join(log_root, log_file)
        debugger = config['debug_logging']
        if debugger == 'True' or debugger == 'true' or debugger == True:
            level = logging.DEBUG
        else:
            level = logging.INFO
        log_name = 'comm_sys'
        if sub:
            log_name = '%s_%s' % (sub, log_name)
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level=level)
        fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                                      backupCount=int(config['log_days']))
        fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
        fh.setFormatter(fm)
        self.logger.addHandler(fh)
        self.logger.info('Comm System Activated!')

    def get_supervisors(self, maintenance=False, coordinators=False):
        """
        This gets the Coordinators and Supervisors with which to send hipchats to.
        :return: admins (dict) {name: email}
        """
        if maintenance:
            slack_groups = [self.config['maintenance']]
        else:
            slack_groups = [self.config['admins']]

        # Add Coordinators if needed
        if coordinators:
            slack_groups.append(self.config['coords'])

        self.logger.info('Collecting Support team members from the groups...')
        admins = {}
        groups = []
        for group in slack_groups:
            groups.append(['code', 'is', group])
        filters = [
            {
                'filter_operator': 'any',
                'filters': groups
            }
        ]
        fields = [
            'users',
            'code'
        ]
        tries = 0
        try:
            group_members = self.sg.find('Group', filters, fields)
        except Exception as e:
            # FIXME: This does nothing.
            group_members = []
            tries += 1
            self.logger.error('Comm System failure to get data: %s' % e)
            if tries > 10:
                self.logger.error('Total failure, returning False!')
                return False
        self.logger.debug('GROUP %s' % group_members)
        for group in group_members:
            users = group['users']
            if users:
                for user in users:
                    person = user['name']
                    person_id = user['id']
                    data = self.get_sg_user(userid=person_id)
                    if data:
                        email = data[person_id]['email']
                        admins[person] = email
                        self.logger.debug('%s\'s email %s added' % (person, email))
        return admins

    def get_sg_user(self, userid=None):
        """
        Get a specific Shotgun User's details from any basic input.
        Only the first detected value will be searched.  If all 3 values are added, only the ID will be searched.
        :param userid: (int) Shotgun User ID number
        :param name:   (str) First and Last Name
        :param email:  (str) email@asc-vfx.com
        :return: user: (dict) Basic details
        """
        self.logger.info('Collecting user data to find email...')
        user = {}
        if userid:
            filters = [['sg_status_list', 'is', 'act'], ['id', 'is', userid]]
            fields = [
                'email',
                'projects',
            ]
            try:
                find_user = self.sg.find_one('HumanUser', filters, fields)
                self.logger.debug('find_user returns: %s' % find_user)
            except AttributeError as e:
                self.logger.error('Couldn\'t find user: %s ' % e)
                find_user = None
            except Exception as err:
                self.logger.error('It really died this time: %s' % err)

            if find_user:
                user_id = find_user['id']
                sg_email = find_user['email']
                user[user_id] = {'email': sg_email}
                self.logger.debug('User email found!  %s' % sg_email)
            if not user:
                self.logger.info('This user is not part of the project!')
                return None
        else:
            self.logger.warning('No data passed to get_sg_user()!  Nothing processed!')
        return user

    def get_slack_user(self, email=None, auth_code=None, url=None, tries=0):
        if not auth_code:
            auth_code = self.auth_code
        if not url:
            url = self.slack_url
        self.logger.info('Getting slack user ID...')
        user_id = None
        if email:
            headers = {
                'Authorization': 'Bearer %s' % auth_code,
                'Content-type': 'application/json'
            }
            try:
                slack_users = requests.get('%susers.list' % url, headers=headers)
                self.logger.debug('Checking slack request... %s' % slack_users.json())
                if slack_users.json()['ok']:
                    all_users = slack_users.json()['members']
                    user_id = None
                    for user in all_users:
                        profile = user['profile']
                        if 'email' in profile.keys():
                            user_email = profile['email']
                            if user_email == email:
                                user_id = user['id']
                                self.logger.debug('Slack user ID found! %s' % user_id)
                                break
                else:
                    self.logger.debug('Waiting 10 seconds to allow for Slack rate limits...')
                    time.sleep(10)
                    self.logger.debug('Trying again...')
                    user_id = self.get_slack_user(email=email, auth_code=auth_code, url=url)

            except KeyError as e:
                self.logger.error('Key not found! %s  Trying again...' % e)
                try:
                    t = tries + 1
                    time.sleep(30)
                    if t > 5:
                        raise Exception("Too many tries!  Skipping...")
                    user_id = self.get_slack_user(email=email, auth_code=auth_code, url=url, tries=t)
                except Exception as e:
                    self.logger.error('There is no saving this thing: %s' % e)
                    return None
            except Exception as e:
                try:
                    t = tries + 1
                    if t > 10:
                        self.logger.error("Too many tries!  Skipping...")
                    user_id = self.get_slack_user(email=email, auth_code=auth_code, url=url,
                                                  tries=t)
                except Exception as e:
                    self.logger.error('There is no saving this thing!: %s' % e)
                    return None
        return user_id

    def send_ot_message(self, slack_url=None, user=None, auth_code=None, color='green', proj=None, entity=None):
        if not auth_code:
            auth_code = self.auth_code
        if not slack_url:
            slack_url = self.slack_url

        if color == 'green':
            color = '#00aa00'
        elif color == 'red':
            color = '#aa0000'
        elif color == 'blue':
            color = '#0000aa'
        else:
            color = '#aacc00'

        self.logger.info('Robo-Coordinator is on the job...')
        try:
            get_user = self.get_slack_user(email=user['email'], auth_code=auth_code, url=slack_url)
        except requests.ConnectionError:
            time.sleep(1000)
            get_user = self.get_slack_user(email=user['email'], auth_code=auth_code, url=slack_url)

        data = {
            "type": "message",
            "channel": get_user,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": '%s has requested *approval for Overtime*!' % user['name']
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Project:*\n_%s_" % proj['name']
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*%s:*\n%s" % (entity['type'], entity['name'])
                        }
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Approve"
                            },
                            "style": "primary",
                            "value": "click_me_123"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Deny"
                            },
                            "style": "danger",
                            "value": "click_me_123"
                        }
                    ]
                }
            ],
            'as_user': True,
            'username': 'Robo-Coordinator'
        }
        print('About to send....')
        if data:
            headers = {
                'Authorization': 'Bearer %s' % auth_code,
                'Content-type': 'application/json'
            }
            data = json.dumps(data)
            try:
                person = requests.post('%schat.postMessage' % slack_url, headers=headers, data=data)
                print('Slack ')
                self.logger.debug('Message Sent: %s' % person.json())
                print('Message sent with data: %s' % person.json())
                self.logger.info('Message sent to %s' % user['name'])
            except Exception as error:
                print('Message fuckard: %s' % error)
                self.logger.error('Something went wrong sending the message!  %s' % error)

    def send_on_quit_alert(self, user=None):
        admins = self.get_supervisors(coordinators=True)
        for admin in admins:
            email = admins[admin]
            slack_id = self.get_slack_user(email=email)

            data = {
                "type": "message",
                "channel": slack_id,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": '*%s has quit the Time Lord TARDIS*!' % user['name']
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "Maybe find out why they're no longer using the time-sheet system."
                            }
                        ]
                    }
                ],
                'as_user': True,
                'username': 'Robo-Coordinator'
            }

            if data:
                headers = {
                    'Authorization': 'Bearer %s' % self.auth_code,
                    'Content-type': 'application/json'
                }
                data = json.dumps(data)
                try:
                    person = requests.post('%schat.postMessage' % self.slack_url, headers=headers, data=data)
                    self.logger.debug('Message sent: %s' % person.json())
                except Exception as error:
                    self.logger.error('Failed to send message: %s' % error)

    def send_error_alert(self, user=None, error=None):
        maintenance = self.get_supervisors(maintenance=True)
        if not user:
            user = {'name': os.environ['USERNAME'], 'id': 0, 'sg_computer': os.environ['COMPUTERNAME']}

        for maint in maintenance:
            email = maintenance[maint]
            slack_id = self.get_slack_user(email=email)

            data = {
                "type": "message",
                "channel": slack_id,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": '*%s has an ERROR*!' % user['name']
                        }
                    },
                    {
                        "type": "section",
                        "fields": [
                            {
                                "type": "mrkdwn",
                                "text": "%s" % error
                            }
                        ]
                    }
                ],
                'as_user': True,
                'username': 'Robo-Coordinator'
            }

            if data:
                headers = {
                    'Authorization': 'Bearer %s' % self.auth_code,
                    'Content-type': 'application/json'
                }
                data = json.dumps(data)
                try:
                    person = requests.post('%schat.postMessage' % self.slack_url, headers=headers, data=data)
                    self.logger.debug('Message sent: %s' % person.json())
                except Exception as error:
                    self.logger.error('Failed to send message: %s' % error)
