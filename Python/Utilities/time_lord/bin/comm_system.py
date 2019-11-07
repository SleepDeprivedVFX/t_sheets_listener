
__author__ = 'Adam Benson'
__version__ = '0.1.0'

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
                    self.logger.info('Waiting 10 seconds to allow for Slack rate limits...')
                    time.sleep(10)
                    self.logger.info('Trying again...')
                    user_id = self.get_slack_user(email=email, auth_code=auth_code, url=url)

            except KeyError, e:
                self.logger.error('Key not found! %s  Trying again...' % e)
                try:
                    t = tries + 1
                    time.sleep(30)
                    if t > 5:
                        raise Exception("Too many tries!  Skipping...")
                    user_id = self.get_slack_user(email=email, auth_code=auth_code, url=url, tries=t)
                except Exception, e:
                    self.logger.error('There is no saving this thing: %s' % e)
                    return None
            except Exception, e:
                try:
                    t = tries + 1
                    if t > 10:
                        self.logger.error("Too many tries!  Skipping...")
                    user_id = self.get_slack_user(email=email, auth_code=auth_code, url=url,
                                             tries=t)
                except Exception, e:
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
            'type': 'message',
            'channel': get_user,
            'text': '%s has requested *approval for Overtime*!' % user['name'],
            'attachments': [
                {
                    'fallback': 'Overtime Request',
                    'title': 'Overtime Request',
                    'text': 'Approve Overtime?',
                    'fields': [
                        {
                            'title': 'Project',
                            'value': '_%s_' % proj['name']
                        },
                        {
                            'title': '%s' % entity['type'],
                            'value': '*%s*' % entity['name']
                        }
                    ]
                }
            ],
            'as_user': True,
            'username': 'Robo-Coordinator'
        }

        if data:
            headers = {
                'Authorization': 'Bearer %s' % auth_code,
                'Content-type': 'application/json'
            }
            data = json.dumps(data)
            try:
                person = requests.post('%schat.postMessage' % slack_url, headers=headers, data=data)
                self.logger.debug('Message Sent: %s' % person.json())
                self.logger.info('Message sent to %s' % user['name'])
            except Exception as error:
                self.logger.error('Something went wrong sending the message!  %s' % error)

