import shotgun_api3 as sgapi
import os
import sys
from PySide import QtGui, QtCore
import logging
from datetime import datetime

# Time Lord Libraries
from bin.time_continuum import continuum
from bin.companions import companions
from bin import configuration
from bin import shotgun_collect


config = configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'psychic_paper.log'
log_path = os.path.join(config['log_path'], log_file)
if config['debug_logging'] == 'True' or 'true' or True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('psychic_paper')
logger.setLevel(level=level)
fh = logging.FileHandler(filename=log_path)
fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
fh.setFormatter(fm)
logger.addHandler(fh)

logger.info('The Time Lord has started!')

# --------------------------------------------------------------------------------------------------
# Setup Shotgun Connection
# --------------------------------------------------------------------------------------------------
sg = sgapi.Shotgun(config['sg_url'], config['sg_name'], config['sg_key'])
logger.debug('Shotgun is connected.')

# --------------------------------------------------------------------------------------------------
# Connect Time Lord Components
# --------------------------------------------------------------------------------------------------
# setup continuum
tl_time = continuum(sg)

# Setup and get users
users = companions(sg)
user = users.get_user_from_computer()

# setup shotgun data connection
sg_data = shotgun_collect.sg_data(sg)

task_list = sg_data.get_entity_tasks(entity_id=2938)
print task_list

# Get the previous time sheet.
previous_time = tl_time.get_last_timesheet(user=user)
if previous_time:
    previous_end_time = previous_time['sg_task_end']
    previous_start_time = previous_time['sg_task_start']
    if not previous_end_time:
        if tl_time.aint_today(previous_start_time):
            new_datetime = tl_time.assume_end_time(previous_start_time, config['regular_end'])
            tl_time.clock_out_time_sheet(timesheet=previous_time, clock_out=new_datetime)
        else:
            tl_time.clock_out_time_sheet(timesheet=previous_time, clock_out=datetime.now())

    # Create new time sheet
    # This needs context. How to get that context is going to be interesting.
    # 1. From inside a Shotgun DCC. No problem, BUT the UI may need some differences.
    # 2. Somehow using the template/path/filename to get the context (Whew, easy and hard at the same time)
    # 3. From the UI.
    # In the end, I really just need the task ID/entity.  Entity, user, time.
    # If I get the project ID from either the folder name (search for similar project name) or some other
    # place, then I can use sg_data.get_sg_configuration()
    # As this is primarily for the stand alone UI, then the context will have to come from the UI.
    # The drag-n-drop will get context from the path
    # And the DCC version will get context from Shotgun.
    context = {'Task': {'id': 21831, 'content': 'model.main'}, 'Entity': {'id': 5926, 'code': 'timeLord_UI'},
               'Project': {'id': 442, 'name': 'neo'}}
    tl_time.create_new_timesheet(user=user, context=context)


# previous_day = tl_time.get_previous_work_day(date=datetime.now(), regular_days=config['regular_days'])
# not_today = tl_time.aint_today(previous_day)
# if not_today:
#     is_weekday = tl_time.date_is_weekday(previous_day)
#     if is_weekday[0]:
#         previous_week = tl_time.time_from_last_week(previous_day)
#         print previous_day
