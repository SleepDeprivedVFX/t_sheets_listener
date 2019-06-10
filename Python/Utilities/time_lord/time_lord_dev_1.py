import shotgun_api3 as sgapi
import os
import sys
import datetime
import time
import requests
from PySide import QtGui, QtCore
import ConfigParser

sys_path = sys.path
config_file = 'dalek.cfg'
try:
    print 'Finding configuration file...'
    config_path = [f for f in sys_path if os.path.isfile(f + '/' + config_file)][0] + '/' + config_file
    config_path = config_path.replace('\\', '/')
    print 'Configuration found!'
except IndexError, e:
    raise e

configuration = ConfigParser.ConfigParser()
print 'Reading the configuration file...'
configuration.read(config_path)

cfg_sg_url = configuration.get('Shotgun', 'sg_url')
cfg_sg_key = configuration.get('Shotgun', 'sg_key')
cfg_sg_name = configuration.get('Shotgun', 'sg_name')

sg = sgapi.Shotgun(cfg_sg_url, cfg_sg_name, cfg_sg_key)

# Get the first day of the week
week_start = datetime.datetime.today() - datetime.timedelta(days=datetime.datetime.today().isoweekday() % 7)
week_start = week_start.replace(tzinfo=None)

right_now = datetime.datetime.now()

# List by a specific user
filters = [
    ['user', 'is', {'type': 'HumanUser', 'id': 41}],
    ['sg_task_end', 'is', None]
]
fields = [
    'user',
    'date',
    'sg_task_start',
    'sg_task_end'
]
test = sg.find('TimeLog', filters, fields)
i = 1
for t in test:
    if t['sg_task_start']:
        # Check the current start time against the first of the week.

        # Important IF:
        #   If someone forgets to clock out last weekend, then the system will either have to auto-clock them out at
        #   7PM (configurable) or it will have to do a soft filter and a hard filter.
        #   Hard filter:
        #       Filters out anything greater than date X, let's say one month.
        #   Soft filter:
        #       Filters out anything greater than the first of the week.
        #   This way, it's easy to do by the week calculations (and trigger events) for the big numbers, and absolute
        #   cut off dates for old time sheets has a limit.
        start_time = t['sg_task_start']
        start_time = start_time.replace(tzinfo=None)
        print start_time
        print week_start
        if start_time > week_start:
            # At this point checks for multiple time sheets can come into play.

            print i, t['user']
            print '  ', t['date']
            print '  ', t['sg_task_start']
            print '  ', t['sg_task_end']
            i += 1



