"""
Highly simplistic tools for doing quick tests and repairs.
"""
import shotgun_api3 as sgapi
import os
import sys
from PySide import QtGui, QtCore
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta
from dateutil import parser

# Time Lord Libraries
from bin.time_continuum import continuum
from bin.companions import companions
from bin import configuration
from bin import shotgun_collect
import time

config = configuration.get_configuration()

sg = sgapi.Shotgun(config['sg_url'], config['sg_name'], config['sg_key'])


def super_cleanup(user_id=None):
    """
    Sets start and end times on any straggler time sheets from the distant past.
    :param user_id:
    :return:
    """
    if user_id:

        filters = [
            ['user', 'is', {'type': 'HumanUser', 'id': user_id}],
            {
                "filter_operator": "any",
                "filters": [
                    ['sg_task_start', 'is', None],
                    ['sg_task_end', 'is', None]
                ]
            }
        ]
        fields = [
            'sg_task_start',
            'sg_task_end',
            'id',
            'user',
            'date'
        ]
        try:
            empties = sg.find('TimeLog', filters, fields, order=[{'field_name': 'id', 'direction': 'desc'}])
        except Exception as e:
            empties = None
            print('Shit hit the fan: %s' % e)
        if empties:
            for empty in empties:
                print '-' * 120
                print empty
                date = empty['date']
                start = empty['sg_task_start']
                end = empty['sg_task_end']
                if start and not end:
                    end = start + timedelta(hours=1)
                    print 'new end: %s' % end
                    data = {
                        'sg_task_end': end,
                        'description': 'Clock Tools Super Cleanup'
                    }
                    update = sg.update('TimeLog', empty['id'], data)
                    print 'Updated: %s' % update
                elif not start and not end:
                    start = '%s %s' % (date, config['regular_start'])
                    start = parser.parse(start)
                    end = '%s %s' % (date, config['regular_end'])
                    end = parser.parse(end)
                    print 'New Start: %s' % start
                    print 'New End: %s ' % end
                    data = {
                        'sg_task_start': start,
                        'sg_task_end': end,
                        'description': 'Clock Tools Super Cleanup'
                    }
                    update = sg.update('TimeLog', empty['id'], data)
                    print 'Updated: %s' % update
        else:
            print 'No Empties Found'


super_cleanup(user_id=41)

