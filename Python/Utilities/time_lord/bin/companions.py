"""
The companions are the human users who run along with our Time Lord.
"""

__author__ = 'Adam Benson'
__version__ = '0.1.0'

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
                'id'
            ]
            find_user = self.sg.find_one('HumanUser', filters, fields)
            return find_user
        return False

