"""
This is a partial start-over for the time_lord.  I feel like the original system may have inadvertently become too
cumbersome to make work, and was ending up being one patch after another, not really solving any of the problems, but
covering them up with ever more inhibiting drives to collect data.

SYSTEM NEEDS:
1. Needs a time system that runs the clocks
    a. Main clocks and start and end clocks should always keep running
    b. TRT (Total Running Time) clocks should be able to get new data from the most recent time-sheets, but keep running
2. Needs a time-based triggering system for updating data from outside of the application
    a. Get and implement changes to Daily/Weekly totals.
    b. Drag-n-Drop publishes or manual time changes.
3. Needs a broader tool kit for processing changes that doesn't lock up the clocks or user interface.
4. A signal system with clear ins and outs for all the main points of data, and it needs a unified point of data for
    all features.  No doubling up or redundant tasks.
5. Needs a global logger stream to handle logs across all tools!

WISH LIST:
1. Shotgun Listening system.
    a. Listens for Shotgun_TimeLog_New or Shotgun_TimeLog_Change events.
        This would remove the need for most of the data calls, as the data calls would be triggered by the events.
        One problem that may arise is that our own events will trigger the changes, thus:
            i. I collect the new UI created timesheet ID immediately, and if the emitted signal contains that ID, it is
                ignored
            ii. A timer might get introduced to minimize the number of calls; only 1 call allowed in a 2 second period.
                Because some of the routines create multiple entries in quick succession, and I wouldn't want to process
                multiple hits within a few microseconds.
"""

import shotgun_api3 as sgapi
import os
import sys
from PySide import QtGui, QtCore
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import cPickle as pickle

# Time Lord Libraries
from bin.time_continuum import continuum
from bin.companions import companions
from bin import configuration
from bin import shotgun_collect
from ui import time_lord_clock as tlu
import time

config = configuration.get_configuration()

# ------------------------------------------------------------------------------------------------------
# Create logging system
# ------------------------------------------------------------------------------------------------------
log_file = 'test_sheet.log'
log_root = os.path.join(sys.path[0], 'logs')
log_path = os.path.join(log_root, log_file)
debug = config['debug_logging']
if debug == 'True' or debug == 'true' or debug == True:
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger('test_sheet')
logger.setLevel(level=level)
fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                              backupCount=int(config['log_days']))
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
tl_time = continuum(sg, config=config, sub='time_lord')

# Setup and get users
users = companions(sg, config=config, sub='time_lord')
user = users.get_user_from_computer()

# setup shotgun data connection
sg_data = shotgun_collect.sg_data(sg, config=config, sub='time_lord')

lunch_task = sg_data.get_lunch_task(lunch_proj_id=int(config['admin_proj_id']),
                                    task_name=config['lunch'])

'''
The Following is pulled from the Event Listener system.  There's some good simple nuggets in there.  Parsing more...
_______________________________________________________________________________________________________________________
# This loop will trigger calls to new events and save heard calls to a database of some sort. More research needed...
        self.log.debug('Starting the event processing loop.')
        while self._continue:  # self._continue = True from the __init__()
            # Process events
            events = self._getNewEvents()  # This is the money maker.  This self._getNewEvents() gets the info I need
            for event in events:
                for collection in self._pluginCollections:  # This part doesn't apply to me.  Not processing events.
                    collection.process(event)
                self._saveEventIdData()  # This one is interesting.

            # if we're lagging behind Shotgun, we received a full batch of events
            # skip the sleep() call in this case
            if len(events) < self.config.getMaxEventBatchSize():
                try:
                    time.sleep(self._fetch_interval)
                except IOError:
                    time.sleep(5)

            # Reload plugins
            for collection in self._pluginCollections:
                collection.load()
                
            # Make sure that newly loaded events have proper state.
            self._loadEventIdData()

        self.log.debug('Shuting down event processing loop.')
-----------------------------------------------------------------------------------------------------------------------

# The Save Data routine from the loop above:
______________________________________________________________________________________________________________________

    def _saveEventIdData(self):
        """
        Save an event Id to persistant storage.

        Next time the engine is started it will try to read the event id from
        this location to know at which event it should start processing.
        """
        eventIdFile = self.config.getEventIdFile()  # This is the data file that is being saved to.
            # In the eventListener it's the: eventIdFile: C:/shotgun/shotgunEvents/shotgunEventDaemon.id from config
            # They're pickling the data somehow

        if eventIdFile is not None:
            for collection in self._pluginCollections:
                self._eventIdData[collection.path] = collection.getState()

            for colPath, state in self._eventIdData.items():
                if state:
                    try:
                        fh = open(eventIdFile, 'w')
                        pickle.dump(self._eventIdData, fh)
                        fh.close()
                    except OSError, err:
                        self.log.error('Can not write event id data to %s.\n\n%s', eventIdFile, traceback.format_exc(err))
                    break
            else:
                self.log.warning('No state was found. Not saving to disk.')
----------------------------------------------------------------------------------------------------------------------

# This opens and loads the afore mentioned file
______________________________________________________________________________________________________________________

    def _loadEventIdData(self):
        """
        Load the last processed event id from the disk

        If no event has ever been processed or if the eventIdFile has been
        deleted from disk, no id will be recoverable. In this case, we will try
        contacting Shotgun to get the latest event's id and we'll start
        processing from there.
        """
        eventIdFile = self.config.getEventIdFile()

        if eventIdFile and os.path.exists(eventIdFile):
            try:
                fh = open(eventIdFile)
                try:
                    self._eventIdData = pickle.load(fh)

                    # Provide event id info to the plugin collections. Once
                    # they've figured out what to do with it, ask them for their
                    # last processed id.
                    noStateCollections = []
                    for collection in self._pluginCollections:
                        state = self._eventIdData.get(collection.path)
                        if state:
                            collection.setState(state)
                        else:
                            noStateCollections.append(collection)

                    # If we don't have a state it means there's no match
                    # in the id file. First we'll search to see the latest id a
                    # matching plugin name has elsewhere in the id file. We do
                    # this as a fallback in case the plugins directory has been
                    # moved. If there's no match, use the latest event id 
                    # in Shotgun.
                    if noStateCollections:
                        maxPluginStates = {}
                        for collection in self._eventIdData.values():
                            for pluginName, pluginState in collection.items():
                                if pluginName in maxPluginStates.keys():
                                    if pluginState[0] > maxPluginStates[pluginName][0]:
                                        maxPluginStates[pluginName] = pluginState
                                else:
                                    maxPluginStates[pluginName] = pluginState

                        lastEventId = self._getLastEventIdFromDatabase()
                        for collection in noStateCollections:
                            state = collection.getState()
                            for pluginName in state.keys():
                                if pluginName in maxPluginStates.keys():
                                    state[pluginName] = maxPluginStates[pluginName]
                                else:
                                    state[pluginName] = lastEventId
                            collection.setState(state)

                except pickle.UnpicklingError:
                    fh.close()

                    # Backwards compatibility:
                    # Reopen the file to try to read an old-style int
                    fh = open(eventIdFile)
                    line = fh.readline().strip()
                    if line.isdigit():
                        # The _loadEventIdData got an old-style id file containing a single
                        # int which is the last id properly processed.
                        lastEventId = int(line)
                        self.log.debug('Read last event id (%d) from file.', lastEventId)
                        for collection in self._pluginCollections:
                            collection.setState(lastEventId)
                fh.close()
            except OSError, err:
                raise EventDaemonError('Could not load event id from file.\n\n%s' % traceback.format_exc(err))
        else:
            # No id file?
            # Get the event data from the database.
            lastEventId = self._getLastEventIdFromDatabase()
            if lastEventId:
                for collection in self._pluginCollections:
                    collection.setState(lastEventId)

            self._saveEventIdData()
'''

db_path = os.path.join(sys.path[0], 'data_io/time_capsule.tld')  # .tld for time lord data
if not os.path.exists(db_path):
    os.makedirs(db_path)
if os.path.exists(db_path):
    data = {}
    db_file = open(db_path, 'rb')
    print 'open file: %s' % db_file
    # try:
    test_db = pickle.load(db_file)
    db_file.close()
    print 'test_db returns: %s' % test_db
    for k, v in test_db.items():
        data[k] = v
    # except Exception as e:
    #     print e
    db_file = open(db_path, 'wb')
    data['fart'] = 'hammer'
    pickle.dump(data, db_file)
    db_file.close()



