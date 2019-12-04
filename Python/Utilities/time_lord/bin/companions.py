"""
The companions are the human users who run along with our Time Lord.
"""

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.3.2'

import platform
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys

if platform.system() == 'Windows':
    env_user = 'USERNAME'
    computername = 'COMPUTERNAME'
else:
    env_user = 'USER'
    computername = 'HOSTNAME'


class companions(object):
    def __init__(self, sg=None, config=None, sub=None):
        self.sg = sg
        self.config = config

        # ------------------------------------------------------------------------------------------------------
        # Create logging system
        # ------------------------------------------------------------------------------------------------------
        log_file = 'companion_report.log'
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
        log_name = 'companions'
        if sub:
            log_name = '%s_%s' % (sub, log_name)
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level=level)
        fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                                      backupCount=int(config['log_days']))
        fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
        fh.setFormatter(fm)
        self.logger.addHandler(fh)
        self.logger.info('Companions are onboard!')

    def get_user_from_computer(self):
        user = os.environ[env_user]
        # FIXME: This is a temp workaround for my laptop.
        if user == 'sleep':
            user = 'adamb'
        print(user)
        if user:
            filters = [
                ['login', 'is', user]
            ]
            fields = [
                'name',
                'email',
                'permission_rule_set',
                'sg_computer',
                'projects',
                'groups',
                'id',
                'sg_hourly',
            ]
            find_user = self.sg.find_one('HumanUser', filters, fields)
            return find_user
        return False

    def get_user_by_id(self, uid=None):
        if uid:
            filters = [
                ['id', 'is', uid]
            ]
            fields = [
                'name',
                'email',
                'permission_rule_set',
                'sg_computer',
                'projects',
                'groups',
                'sg_hourly'
            ]
            user = self.sg.find_one('HumanUser', filters, fields)
            if user:
                return user
        return False

    def get_admins(self):
        admin_group = self.config['admins']
        admins = []

        filters = [
            ['code', 'is', admin_group]
        ]
        fields = [
            'users',
            'code'
        ]
        group_members = self.sg.find_one('Group', filters, fields)
        if group_members:
            users = group_members['users']
            if users:
                for user in users:
                    try:
                        person_id = user['id']
                        new_user = self.get_user_by_id(uid=person_id)
                        if new_user:
                            admins.append(new_user)
                    except Exception as e:
                        self.logger.error('Group Collection failed: %s' % e)
        return admins

    def get_all_users(self):
        """
        Collect all the active users in Shotgun
        :return: (list) or (dict)
        """
        get_users = None
        filters = [
            ['sg_status_list', 'is', 'act'],
            ['permission_rule_set', 'is_not', {'type': 'PermissionRuleSet', 'id': 52}],
            ['id', 'is_not', 24]
        ]
        fields = [
            'name',
            'email',
            'permission_rule_set',
            'sg_computer',
            'projects',
            'groups',
            'sg_hourly'
        ]
        get_users = self.sg.find('HumanUser', filters, fields)

        return get_users



