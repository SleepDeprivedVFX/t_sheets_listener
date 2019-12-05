"""
The Shotgun Collect will grab data about projects, assets, shots and tasks.
"""

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.3.3'

import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
import inspect
from datetime import datetime
import time


class sg_data(object):
    def __init__(self, sg=None, config=None, sub=None):

        # ------------------------------------------------------------------------------------------------------
        # Create logging system
        # ------------------------------------------------------------------------------------------------------
        log_file = 'shotgun_report.log'
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
        log_name = 'sg_collection'
        if sub:
            log_name = '%s_%s' % (sub, log_name)
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level=level)
        fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                                      backupCount=int(config['log_days']))
        fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
        fh.setFormatter(fm)
        self.logger.addHandler(fh)
        self.logger.info('Shotgun Collection Activated!')
        self.sg = sg
        self.logger.debug('Shotgun sg sub-loaded.')

    def get_active_projects(self):
        self.logger.info('Getting active projects')
        try:
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
        except Exception as e:
            self.logger.error('Failed to get projects.  Trying again...')
            time.sleep(2)
            active_projects = self.get_active_projects()
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
            try:
                assets = self.sg.find('Asset', filters, fields)
            except Exception as e:
                self.logger.warning('The Asset collection failed. Trying again...')
                time.sleep(2)
                assets = self.get_project_assets(proj_id=proj_id)
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
            try:
                shots = self.sg.find('Shot', filters, fields)
            except Exception as e:
                self.logger.warning('The Shot Collectoin has failed.  Trying again. %s' % e)
                time.sleep(2)
                shots = self.get_project_shots(proj_id=proj_id)
            self.logger.info('Shots collected')
            self.logger.debug('Shots List: %s' % shots)
            return shots

    def get_entity_tasks(self, entity_id=None, entity_name=None, proj_id=None, t=0):
        if entity_id:
            print('Getting entity tasks...')
            self.logger.info('Getting tasks for entity ID %s...' % entity_id)
            entity_type = self.get_entity_type(proj_id=proj_id, entity_name=entity_name)
            filters = [
                ['entity', 'is', {'type': entity_type, 'id': entity_id}],
                ['project', 'is', {'type': 'Project', 'id': proj_id}]
            ]
            fields = [
                'content',
                'step',
                'entity'
            ]
            try:
                tasks = self.sg.find('Task', filters, fields)
            except Exception as e:
                self.logger.debug('Shotgun failure of some sort: %s' % e)
                self.logger.debug('Trying again...')
                time.sleep(2)
                t += 1
                if t > 10:
                    return None
                tasks = self.get_entity_tasks(entity_id=entity_id, entity_name=entity_name, proj_id=proj_id, t=t)

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
                self.logger.debug('Project Details found: %s' % project)
                return project
            except (AttributeError, TypeError), e:
                self.logger.error('Could not get the project: %s' % e)
                try:
                    time.sleep(1)
                    self.logger.debug('Trying again...')
                    tryagain = self.sg.find('Project', filters, fields)
                    print('secondary: %s' % tryagain)
                    if tryagain:
                        project = tryagain[0]
                        self.logger.debug('Project Details Found: %s' % project)
                        return project
                    self.logger.debug('Still couldn\'t find shit! %s' % tryagain)
                except (AttributeError, TypeError, KeyError, Exception), e:
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
            try:
                link = self.sg.find_one(ent_type, filters, fields)
            except (AttributeError, Exception), e:
                self.logger.error('Bad connection... Try again... %s' % e)
                time.sleep(2)
                print('Lame ass connection.  Trying again...')
                link = self.get_entity_links(ent_type=ent_type, name=name, ent_id=ent_id, proj_id=proj_id)
            return link
        return None

    def get_context_from_UI(self):
        pass

    def get_context_from_path(self, path=None):
        pass

    def get_sg_configuration(self, proj_id):
        """
        Get the Pipeline configuration from the Project ID.  This gets the windows_path to where the pipeline
        config files
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

    def get_entity_type(self, proj_id=None, entity_name=None):
        entity_type = None
        if proj_id and entity_name:
            assets = self.get_project_assets(proj_id=proj_id)
            shots = self.get_project_shots(proj_id=proj_id)
            entities = assets + shots
            for entity in entities:
                if entity['code'] == entity_name:
                    entity_type = entity['type']
                    break
        return entity_type

    def get_task_id(self, entity_id=None, task_name=None, entity_name=None, proj_id=None):
        task_id = None
        if entity_id and task_name:
            tasks = self.get_entity_tasks(entity_id=entity_id, entity_name=entity_name, proj_id=proj_id)
            if tasks:
                for task in tasks:
                    if task['content'] == task_name:
                        task_id = task['id']
                        break
        return task_id

    def get_lunch_task(self, lunch_proj_id=None, task_name=None):
        if lunch_proj_id and task_name:
            filters = [
                ['project', 'is', {'type': 'Project', 'id': lunch_proj_id}],
                ['content', 'is', task_name]
            ]
            fields = [
                'id'
            ]
            try:
                find_task = self.sg.find_one('Task', filters, fields)
            except AttributeError, e:
                self.logger.debug('get_lunch_task failed!  %s' % e)
                time.sleep(2)
                find_task = self.get_lunch_task(lunch_proj_id=lunch_proj_id, task_name=task_name)
            if find_task:
                return find_task
        return False

    def get_entity_from_task(self, task_id=None):
        if task_id:
            filters = [
                ['id', 'is', task_id]
            ]
            fields = [
                'entity'
            ]
            try:
                task = self.sg.find_one('Task', filters, fields)
            except Exception as e:
                self.logger.error('Get Entity from Tasks failed: %s' % e)
                time.sleep(2)
                task = self.get_entity_from_task(task_id=task_id)
            return task
        return None

