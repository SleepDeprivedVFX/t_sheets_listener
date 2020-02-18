import shotgun_api3 as sgapi

from bin import configuration
from bin import shotgun_collect
from bin import time_continuum
from bin import companions

config = configuration.get_configuration()


# --------------------------------------------------------------------------------------------------
# Setup Shotgun Connection
# --------------------------------------------------------------------------------------------------
sg = sgapi.Shotgun(config['sg_url'], config['sg_name'], config['sg_key'])

sg_data = shotgun_collect.sg_data(sg, config=config, sub='test')

users = companions.companions(sg, config=config, sub='test')
user = users.get_user_from_computer()

tl_time = time_continuum.continuum(sg, config=config, sub='test')

def get_all_project_dropdowns(self):
    projects = sg_data.get_active_projects(user=user)

    assets = sg_data.get_active_assets(user=user, active_projects=projects)
    shots = sg_data.get_active_shots(user=user, active_projects=projects)
    entities = assets + shots
    tasks = sg_data.get_active_tasks(entities=entities)

    data = {}

    for project in projects:
        project_name = project['name']
        project_id = project['id']
        if project_name not in data.keys():
            data[project_name] = {
                '__specs__': {
                    'id': project_id
                }
            }

        for entity in entities:
            entity_name = entity['code']
            entity_id = entity['id']
            if entity['project']['id'] == project_id:
                if entity_name not in data[project_name].keys():
                    data[project_name][entity_name] = {
                        '__specs__': {
                            'id': entity_id
                        }
                    }

                    for task in tasks:
                        # print(task)
                        task_name = task['content']
                        task_id = task['id']
                        task_step = task['step']
                        if task_step:
                            step_name = task_step['name']
                        else:
                            step_name = None
                        task_project_id = task['project']['id']
                        task_entity_id = task['entity']['id']
                        # print('task_entity_id: %s | entity_id: %s' % (task_entity_id, entity_id))
                        if task_project_id == project_id and task_entity_id == entity_id:
                            if task_name not in data[project_name][entity_name].keys():
                                data[project_name][entity_name][task_name] = {
                                    '__specs__': {
                                        'id': task_id
                                    }
                                }
    print('DATA:', data)
    return data

