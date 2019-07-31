"""
The companions are the human users who run along with our Time Lord.
"""

import os
import sys
import platform
import logging

if platform.system() == 'Windows':
    env_user = 'USERNAME'
    computername = 'COMPUTERNAME'
else:
    env_user = 'USER'
    computername = 'HOSTNAME'


class companions(object):
    def __init__(self, sg=None):
        self.sg = sg
        self.logger = logging.getLogger('tardis_report.companions')
        self.logger.info('Companions are onboard!')

    def get_user_from_computer(self):
        user = os.environ[env_user]
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
                'groups'
            ]
            find_user = self.sg.find_one('HumanUser', filters, fields)
            return find_user
        return False

