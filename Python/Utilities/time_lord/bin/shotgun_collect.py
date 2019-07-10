"""
The Shotgun Collect will grab data about projects, assets, shots and tasks.
"""

import logging


class sg_data(object):
    def __init__(self, sg=None):
        self.logger = logging.getLogger('psychic_paper.sg_data')
        self.sg = sg
        self.logger.debug('Shotgun sub-loaded.')
        self.logger.info('Shotgun Data Collection Activated!')

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
        active_projects = self.sg.find('Project', filters, fields, order=[{'field_name': 'name',
                                                                           'direction': 'asc'}])
        self.logger.info('Projects collected!')
        self.logger.debug('Project List: %s' % active_projects)
        return active_projects

    def get_project_assets(self, proj_id=None):
        if proj_id:
            self.logger.info('Getting project assets...')
            filters = [
                ['project', 'is', {'type': 'Project', 'id': proj_id}]
            ]
            fields = [
                'code'
            ]
            assets = self.sg.find('Asset', filters, fields)
            self.logger.info('Assets collected.')
            self.logger.debug('Assets List: %s' % assets)
            return assets

    def get_project_shots(self, proj_id=None):
        if proj_id:
            self.logger.info('Getting project shots...')
            filters = [
                ['project', 'is', {'type': 'Project', 'id': proj_id}]
            ]
            fields = [
                'code'
            ]
            shots = self.sg.find('Shot', filters, fields)
            self.logger.info('Shots collected')
            self.logger.debug('Shots List: %s' % shots)
            return shots

    def get_entity_tasks(self, entity_id=None):
        print 'entity_id: %s' % entity_id
        if entity_id:
            self.logger.info('Getting tasks for entity ID %s...' % entity_id)
            filters = [
                {
                    'filter_operator': 'any',
                    'filters': [
                        ['entity', 'is', {'type': 'Asset', 'id': entity_id}],
                        ['entity', 'is', {'type': 'Shot', 'id': entity_id}]
                    ]
                }
            ]
            fields = [
                'content',
                'step'
            ]
            tasks = self.sg.find('Task', filters, fields)
            self.logger.info('Tasks collected')
            self.logger.debug('Tasks List: %s' % tasks)
            return tasks
        return None

    def get_project_details_by_name(self, proj_name=None):
        '''
        Get details of a project when you only have its name.
        :param proj_name: (str) The name of a valid Project
        :return: (dict) a dictionary of values pertinent to the project
        '''
        if proj_name:
            self.logger.debug('Checking for project name %s' % proj_name)
            filters = [
                ['name', 'is', proj_name]
            ]
            fields = [
                'id',
                'tank_name',
                'sg_description',
                'code'
            ]
            try:
                self.logger.debug('Searching...')
                project = self.sg.find_one('Project', filters, fields)
                print 'immediate: %s' % project
                self.logger.debug('Project Details found: %s' % project)
                return project
            except (AttributeError, TypeError), e:
                self.logger.error('Could not get the project: %s' % e)
                try:
                    self.logger.debug('Trying again...')
                    tryagain = self.sg.find('Project', filters, fields)
                    print 'secondary: %s' % tryagain
                    if tryagain:
                        project = tryagain[0]
                        self.logger.debug('Project Details Found: %s' % project)
                        return project
                    self.logger.debug('Still couldn\'t find shit! %s' % tryagain)
                except (AttributeError, TypeError), e:
                    self.logger.error('Well, Fuck.  %s' % e)
        self.logger.debug('No Project found!')
        return None

    def get_entity_links(self, ent_type=None, name=None, ent_id=None, proj_id=None):
        if ent_type and name and ent_id:
            filters = [
                ['id', 'is', ent_id],
                ['project', 'is', {'type': 'Project', 'id': proj_id}]
            ]
            fields = [
                'entity'
            ]
            link = self.sg.find_one(ent_type, filters, fields)
            return link
        return None

    def get_context_from_UI(self):
        pass

    def get_context_from_path(self, path=None):
        pass

    def get_sg_configuration(self, proj_id):
        """
        Get the Pipeline configuration from the Project ID.  This gets the windows_path to where the pipeline config files
        exist on the server
        :param proj_id:
        :return: config_path
        """
        self.logger.debug(('%' * 35) + 'get_configuration' + ('%' * 35))
        try:
            if proj_id:
                filters = [
                    ['project', 'is', {'type': 'Project', 'id': proj_id}],
                    ['code', 'is', 'Primary']
                ]
                fields = [
                    'windows_path'
                ]
                get_config = self.sg.find_one('PipelineConfiguration', filters, fields)
                if get_config:
                    config_path = get_config['windows_path']
                    config_path = config_path.replace('\\', '/')

                    self.logger.debug(('.' * 35) + 'END get_configuration' + ('.' * 35))
                    return config_path
            return
        except Exception, e:
            self.logger.error('Some shit when down! %s' % e)
            return False

    def get_entity_id(self, proj_id=None, entity_name=None):
        entity_id = None
        if proj_id and entity_name:
            assets = self.get_project_assets(proj_id=proj_id)
            shots = self.get_project_shots(proj_id=proj_id)
            entities = assets + shots
            for entity in entities:
                if entity['code'] == entity_name:
                    entity_id = entity['id']
                    break
        return entity_id

    def get_task_id(self, entity_id=None, task_name=None):
        task_id = None
        if entity_id and task_name:
            tasks = self.get_entity_tasks(entity_id=entity_id)
            if tasks:
                for task in tasks:
                    if task['content'] == task_name:
                        task_id = task['id']
                        break
        return task_id
