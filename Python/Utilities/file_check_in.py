import sys, os, platform, time
import logging as logger
import subprocess
import re
from datetime import datetime, timedelta

import shotgun_api3 as sgtk

import json
import urllib, urllib2

# ----------------------------------------------------------------------------------------------------------------------
# Global Variables
# ----------------------------------------------------------------------------------------------------------------------

# Define system variables
osSystem = platform.system()

if osSystem == 'Windows':
    base = '//hal'
    env_user = 'USERNAME'
else:
    base = '/Volumes'
    env_user = 'USER'

# Build Shotgun connection string.  This will be obsolete in the main version
shotgun_conf = {
    'url':'https://asc.shotgunstudio.com',
    'name':'runThis',
    'key':'55b685383cfc7bfaad304dfd26d55a2685ee7e5efa03ca4f34408192b8ac288c'
    }

sg = sgtk.Shotgun(shotgun_conf['url'], shotgun_conf['name'], shotgun_conf['key'])

# T-Sheets Authorization.  This needs to be acquired from Shotgun.
authorization = 'S.4__b0c48a6b9e2e5bc810e2c402496f5549df7fb16a'

url = 'https://rest.tsheets.com/api/v1/'

headers = {
    'Authorization': 'Bearer %s' % authorization
}

user_params = {'per_page': '50', 'active': 'yes'}
jobs_params = {'active': 'yes'}

class file_check_in:
    def __init__(self):
        pass

    def
