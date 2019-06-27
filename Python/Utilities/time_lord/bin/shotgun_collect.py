"""
The Shotgun Collect will grab data about projects, assets, shots and tasks.
"""

import logging


class sg_data(object):
    def __init__(self, sg=None):
        self.logger = logging.getLogger('psychic_paper.sg_data')
        self.logger.info('Shotgun Data Collection Activated!')
        self.sg = sg

    def get_active_projects(self):
        self.logger.info('Getting active projects')
        filters = [
            ['sg_status', 'is', 'Active']
        ]
        fields = [
            'name',
            'tank_name',
            'code'
        ]
        active_projects = self.sg.find('Project', filters, fields)
        self.logger.info('Projects collected!')
        self.logger.debug('Project List: %s' % active_projects)
        return active_projects

    def get_project_assets(self, proj_id=None):
        if proj_id:
            self.logger.info('Getting project assets...')

    def get_project_shots(self, proj_id=None):
        if proj_id:
            self.logger.info('Getting project shots...')

    def get_entity_tasks(self, entity_id=None):
        if entity_id:
            self.logger.info('Getting tasks...')

