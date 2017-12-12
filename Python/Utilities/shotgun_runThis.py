# ---------------------------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------------------------
import sys, os, platform, time
import logging as logger
import subprocess
import re
from datetime import datetime

# from shotgun_action import ShotgunAction
from pprint import pprint


# ----------------------------------------------
# Generic Shotgun Exception Class
# ----------------------------------------------
# AB NOTE: Add shit here when shit goes wrong
class ShotgunException(Exception):
    print Exception
    pass

osSystem = platform.system()

inTesting = True

# ---------------------------------------------------------------------------------------------
# Variables
# ---------------------------------------------------------------------------------------------
# Shotgun server auth info
shotgun_conf = {
    'url':'https://asc.shotgunstudio.com',
    'name':'runThis',
    'key':'55b685383cfc7bfaad304dfd26d55a2685ee7e5efa03ca4f34408192b8ac288c'
    }

try:
    from shotgun_api3 import Shotgun
    # logger.info('SHOTGUN LOADED SUCCESSFULLY!')
except ImportError:
    # logger.error('SHOTGUN API FAILED TO LOAD! THE ENGINE WILL NOT RUN!!')
    pass

# ----------------------------------------------
# Extract Attachment id from entity field
# ----------------------------------------------

def extract_attachment_id(attachment):
    # extract the Attachment id from the url location
    attachment_id = attachment['url'].rsplit('\\',1)[1]
    try:
        attachment_id = int(attachment_id)
    except:
        # not an integer.
        return None
        # raise ShotgunException("invalid Attachment id returned. Expected an integer: %s "% attachment_id)

    return attachment_id


# -----------------------------------------------
# Run This
# -----------------------------------------------
def runThis(action):
    print 'This thing returns: %s' % action
    return action


# -----------------------------------------------
# Parse the URL and return the appropriate action and data
# -----------------------------------------------
def parseThis(url):
    # logger.info('PARSED GET STRING DATA FROM THE WEB:')
    returnData = {'column_display_names': [], 'cols': []}
    mainString = url.split('shotgun://')[1]
    if osSystem == 'Windows':
        action = mainString.split('/')[0]
        data = mainString.split('/')[1]
    else:
        action = mainString.split('?')[0]
        data = mainString.split('?')[1]
    stringData = data.strip('?')
    parseData = stringData.split('&')
    for entry in parseData:
        try:
            var, val = entry.split('=')
            if var == 'column_display_names' or var == 'cols':
                returnData[var].append(val)
            else:
                returnData[var] = val
            # logger.debug('Line Item = %s: %s' % (var, val))
        except:
            returnData[entry] = None
    #         logger.debug('No data found for %s' % entry)
    # logger.debug('Packaged Data = %s' % returnData)
    return action, returnData

# ----------------------------------------------
# Main Block
# ----------------------------------------------
if __name__ == "__main__":
    try:
        action = parseThis(sys.argv[1])
    except IndexError, e:
        raise ShotgunException("Missing POST arguments")

    sg = Shotgun(shotgun_conf['url'], shotgun_conf['name'], shotgun_conf['key'])

    # action[0] = url string code.   EX: url = shotgun://sendToday   action[0] = sendToday
    # action[1] = pre-parsed url post string.  It is a dictionary that returns something like the following:
    #       {'server_hostname': 'asc.shotgunstudio.com', 'user_id': '41', 'entity_type': 'Playlist',
    #       'user_login': 'adamb', 'title': '', 'cols': [''], 'ids': '77', 'selected_ids': '77',
    #       'referrer_path': '%2Fpage%2F3311', 'session_uuid': '37d33a22-2b75-11e7-83c0-0242ac110005',
    #       'page_id': '3311', 'column_display_names': None}

    if action[0] == 'tsheets':
        result = runThis(action[1])
        print result

