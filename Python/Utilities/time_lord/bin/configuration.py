"""
This will basically just streamline the configuration and cleanup the main code a bit
"""

import ConfigParser
import sys
import os


def get_configuration():
    sys_path = sys.path
    config_file = 'tardis_config.cfg'
    try:
        print 'Finding configuration file...'
        config_path = [f for f in sys_path if os.path.isfile(f + '/' + config_file)][0] + '/' + config_file
        config_path = config_path.replace('\\', '/')
        print 'Configuration found!'
    except IndexError, e:
        raise e

    # Create the configuration connection
    configuration = ConfigParser.ConfigParser()
    print 'Reading the configuration file...'
    configuration.read(config_path)

    config = {}
    # Parse out the configuration to local variables
    # Shotgun
    config['sg_url'] = configuration.get('Shotgun', 'sg_url')
    config['sg_key'] = configuration.get('Shotgun', 'sg_key')
    config['sg_name'] = configuration.get('Shotgun', 'sg_name')

    # Time Lord
    config['regular_days'] = configuration.get('Time Lord', 'regular_days').split(',')
    config['weekend_days'] = configuration.get('Time Lord', 'weekend_days').split(',')
    config['regular_start'] = configuration.get('Time Lord', 'regular_start')
    config['regular_end'] = configuration.get('Time Lord', 'regular_end')
    config['approx_lunch_start'] = configuration.get('Time Lord', 'approx_lunch_start')
    config['approx_lunch_end'] = configuration.get('Time Lord', 'approx_lunch_end')
    config['ot_type'] = configuration.get('Time Lord', 'ot_type')
    config['ot_hours'] = configuration.get('Time Lord', 'ot_hours')
    config['dt_hours'] = configuration.get('Time Lord', 'dt_hours')

    # Logging
    config['debug_logging'] = configuration.get('Logging', 'debugging')

    return config

