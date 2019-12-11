"""
The Time Continuum utility will check to make sure that only one time sheet is active at a time, and that all previous
entries conform to excpected dates, times and over-time statuses.
For instance:
    User forgets to clock out on Friday.  Monday the user clocks in, but last week's entry is still open.
    User forgets to clock out the day before.  Chances are strong they're not still working from the day before.
This will handle the logic that makes sure days and weeks are sorted out, and that hours can be adjusted automatically,
or that appropriate pop ups can be issued reminding the user to update their time sheet.

This engine is going to handle the logic only.  Calls to users will be handled by other engines.
"""

__author__ = 'Adam Benson - AdamBenson.vfx@gmail.com'
__version__ = '0.3.4'

import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
from dateutil import parser
from dateutil import relativedelta
import time
import inspect


class continuum(object):
    def __init__(self, sg=None, config=None, sub=None):
        # self.logger = logging.getLogger('time continuum')
        self.sg = sg

        # ------------------------------------------------------------------------------------------------------
        # Create logging system
        # ------------------------------------------------------------------------------------------------------
        # Find out if the logger already exists.  If not, open a file.
        log_file = 'continuum_report.log'
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
        log_name = 'continuum'
        if sub:
            log_name = '%s_%s' % (sub, log_name)
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(level=level)
        fh = TimedRotatingFileHandler(log_path, when='%s' % config['log_interval'], interval=1,
                                      backupCount=int(config['log_days']))
        fm = logging.Formatter(fmt='%(asctime)s - %(name)s | %(levelname)s : %(lineno)d - %(message)s')
        fh.setFormatter(fm)
        self.logger.addHandler(fh)
        self.logger.info('Continuum Activated!')

        # Days of the week in an iteratable list
        self.weekdays = [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ]

        # get time configurations
        self.double_time_mins = int(config['dt_hours']) * 60

    def start_of_week(self):
        # Get the first day of the week
        week_start = datetime.datetime.today() - datetime.timedelta(days=datetime.datetime.today().isoweekday() % 7)
        week_start = week_start.replace(tzinfo=None)
        return week_start

    def time_from_last_week(self, start_time=None):
        '''
        Checks to see if the given start time is from last week or earlier
        :param start_time: a datetime value.
        :return:
        '''
        if start_time and start_time < self.start_of_week():
            return True
        return False

    def date_is_weekday(self, date=None):
        '''
        Check to see if the given date is a weekday
        :param date: (str) a string formatted date
        :return: (tuple) (True/False, "day" string) - True if a weekday, False if not. Name returned either way.
        '''
        if type(date) == datetime or datetime.datetime:
            date = str(date)
        weekday = parser.parse(date).weekday()
        day = self.weekdays[weekday]
        if weekday < 5:
            return True, day
        return False, day

    def aint_today(self, date=None):
        '''
        A check to see if the time card is from another day.  This should precede calls to date is weekday
        :param date: a date value
        :return: True or False
        '''
        if type(date) == datetime or datetime.datetime:
            date = str(date)
            self.logger.debug('Date converted: %s' % date)
        in_date = parser.parse(date).date()
        now_date = datetime.datetime.now().date()
        if in_date != now_date:
            return True
        return False

    def get_previous_work_day(self, date=None, regular_days=[]):
        '''
        This method will take a date and return the previous working day.
        :param date: A date to count back from
        :param regular_days: [list] A list of active days from the config file
        :return: previous_day: a date
        '''
        prev_day = None
        self.logger.info('Getting the previous work day...')
        if date:
            if type(date) == str:
                self.logger.debug('String type date detected.  Converting...')
                date = parser.parse(date)

            # subtract a day
            prev_day = date - relativedelta.relativedelta(days=1)
            self.logger.debug('prev_day: %s' % prev_day)

            is_last_week = self.time_from_last_week(start_time=prev_day)
            self.logger.debug('is last week? %s' % is_last_week)

            is_weekday = self.date_is_weekday(date=prev_day)
            is_wd = is_weekday[0]
            weekday = is_weekday[1]
            if is_wd:
                self.logger.debug('is_weekday: %s' % weekday)
                if weekday in regular_days:
                    self.logger.debug('Regular day %s' % weekday)
            else:
                self.logger.debug('NOT a weekday! %s' % weekday)
                tries = 0
                while weekday not in regular_days and tries < 5:
                    prev_day = prev_day - relativedelta.relativedelta(days=1)
                    is_weekday = self.date_is_weekday(date=prev_day)
                    weekday = is_weekday[1]
                    tries += 1
                self.logger.debug('Now the weekday is: %s' % weekday)
                self.logger.debug('And the new date is: %s' % prev_day)

        return prev_day

    def get_latest_timesheet(self, user=None):
        if user:
            self.logger.debug('Finding the last timesheet for %s' % user['name'])
            user_id = user['id']
            self.logger.debug('USER ID: %s' % user_id)

            # List all the timesheets for the user
            filters = [
                ['user', 'is', {'type': 'HumanUser', 'id': user_id}]
            ]
            fields = [
                'user',
                'date',
                'sg_task_start',
                'sg_task_end',
                'project',
                'entity',
                'code'
            ]
            try:
                latest_timesheet = self.sg.find_one('TimeLog', filters, fields, order=[{'field_name': 'sg_task_start',
                                                                                        'direction': 'desc'},
                                                                                       {'field_name': 'id',
                                                                                        'direction': 'desc'}])
                self.logger.debug('Timesheet found: %s' % latest_timesheet)
            except (AttributeError, Exception), e:
                self.logger.error('Something unexpected happened while getting the last timesheet: %s' % e)
                latest_timesheet = None
            if latest_timesheet:
                return latest_timesheet
            return {'sg_task_end': None, 'entity': None, 'project': None, 'date': '', 'sg_task_start': None}

    def assume_end_time(self, start_time=None, eod=None):
        self.logger.debug('Assuming an end time from the date and configuration...')
        if start_time:
            if type(eod) == str:
                self.logger.debug('Converting time to datetime type...')
                eod = parser.parse(eod).time()
            raw_date = datetime.datetime.date(start_time)
            new_datetime = datetime.datetime.combine(raw_date, eod)
            self.logger.debug('End date assumed: %s' % new_datetime)
            return new_datetime

    def clock_out_time_sheet(self, timesheet=None, clock_out=None):
        start = timesheet['sg_task_start']
        start_time = start.time()
        start_date = start.date()
        clock_in = parser.parse('%s %s' % (start_date, start_time))
        diff = clock_out - clock_in

        total = (diff.total_seconds() / 60)
        if timesheet:
            self.logger.debug('Timesheet: %s' % timesheet)
            data = {
                'sg_task_end': clock_out,
                'duration': total
            }
            try:
                update = self.sg.update('TimeLog', timesheet['id'], data)
                print('Successfully clocked out. %s' % update)
                self.logger.info('Timesheet updated.')
            except Exception as e:
                print('Failed to connect.  Trying again... %s' % e)
                update = self.clock_out_time_sheet(timesheet=timesheet, clock_out=clock_out)
            return update
        return None

    def create_new_timesheet(self, user=None, context=None, start_time=None, entry='User'):
        """
        Creates a new timesheet.  Works with Stand alone, DCC and drag-n-drop publisher
        :param user: (dict) Contains the Shotgun User ID number
        :param context: (dict) A Shotgun Context Object. Can be built manually.
        :param start_time: (datetime) a date and time to start the clock, usually datetime.now()
        :param entry: (str) This tells the system where it camer from:
                                User = Standalone
                                DCC  = SG Integrated Software
                                Auto = Drag-n-Drop Publisher
        :return: New timesheet.
        """
        print('create_new:', inspect.stack()[0][3], inspect.stack()[1][3])
        if user and context:
            project_id = context['Project']['id']
            task_id = context['Task']['id']
            user_id = user['id']
            self.logger.debug(context)

            if start_time and type(start_time) == datetime or type(start_time) == datetime.datetime:
                task_start = start_time
            else:
                task_start = datetime.datetime.now()
            data = {
                'entity': {'type': 'Task', 'id': task_id},
                'sg_task_start': task_start,
                'user': {'type': 'HumanUser', 'id': user_id},
                'project': {'type': 'Project', 'id': project_id},
                'description': 'Time Lord %s Entry' % entry
            }
            try:
                timesheet = self.sg.create('TimeLog', data)
            except Exception as e:
                print('Something failed.  Trying again... %s' % e)
                timesheet = self.create_new_timesheet(user=user, context=context, start_time=start_time, entry=entry)
            return timesheet

    def get_running_time(self, timesheet=None):
        '''
        Calculate the total running time since clocked in.
        :param timesheet: (dict) a timesheet from Shotgun
        :return: running_time: (str) a six digit string object
        '''
        running_time = {
            'rt': '000000',
            'h': '00',
            'm': '00',
            's': '00'
        }
        if timesheet:
            try:
                if not timesheet['sg_task_end']:
                    start_datetime = timesheet['sg_task_start']
                    self.logger.debug('~' * 50)
                    self.logger.debug('start_datetime: %s' % start_datetime)
                    self.logger.debug('start_datetime TYPE: %s' % type(start_datetime))
                    if type(start_datetime) != datetime.datetime:
                        return running_time
                    start_date = start_datetime.date()
                    start_time = start_datetime.time()
                    start = parser.parse('%s %s' % (start_date, start_time))
                    current_date = datetime.datetime.now()
                    date_diff = current_date - start
                    split_time = str(date_diff).split(':')
                    try:
                        h = '%02d' % int(split_time[0])
                        m = '%02d' % int(split_time[1])
                        s = float(split_time[2])
                        s = '%02d' % int(s)
                    except ValueError, e:
                        if 'days,' in split_time[0]:
                            split_hours = split_time[0].split('days,')
                            d = int(split_hours[0])
                            d_to_h = d * 24
                            h = int(split_hours[1])
                            h = '%02d' % int(d_to_h + h)
                        elif 'day,' in split_time[0]:
                            split_hours = split_time[0].split('day,')
                            d = int(split_hours[0])
                            d_to_h = d * 24
                            h = int(split_hours[1])
                            h = '%02d' % int(d_to_h + h)
                        else:
                            self.logger.error('Can\'t parse the hours!')
                            raise e
                        m = '%02d' % int(split_time[1])
                        s = float(split_time[2])
                        s = '%02d' % int(s)
                    rt = h + m + s
                    running_time = {
                        'rt': rt,
                        'h': h,
                        'm': m,
                        's': s
                    }
            except (AttributeError, TypeError) as e:
                self.logger.error('Yeah, the shit hit the fan: %s' % e)
        return running_time

    def get_daily_total(self, user=None, lunch_id=None, break_id=None):
        '''
        This method will search all of the timesheets for a given user, for a given day, and total up the hours.
        :param user: (dict) The main user data
        :return: A total daily hours number
        '''
        total_duration = 0.0
        if user:
            filters = [
                ['user', 'is', {'type': 'HumanUser', 'id': user['id']}],
                {
                    "filter_operator": "any",
                    "filters": [
                        ['sg_task_start', 'in_calendar_day', 0],
                        ['sg_task_start', 'in_calendar_day', -1]
                    ]
                }
            ]
            if lunch_id:
                filters.append(
                    ['entity', 'is_not', {'type': 'Task', 'id': lunch_id}]
                )
            if break_id:
                filters.append(
                    ['entity', 'is_not', {'type': 'Task', 'id': break_id}]
                )
            fields = [
                'user',
                'duration',
                'sg_task_start',
                'sg_task_end'
            ]
            try:
                # This will get time sheets from "today" and "yesterday" because Shotgun considers anything after 6PM to
                # be "yesterday".  Thus, the in_calendar_day query has to test for both, or not all records will be
                # acquired.  Then I can iterate through them to get dates from "today"
                timesheets = self.sg.find('TimeLog', filters, fields)
            except (AttributeError, Exception), e:
                self.logger.error('Time sheet failed to acquire: %s' % e)
                timesheets = None
            if timesheets:
                for timesheet in timesheets:
                    if not self.aint_today(timesheet['sg_task_start']):
                        if timesheet['sg_task_end']:
                            end_datetime = timesheet['sg_task_end']
                            end_date = end_datetime.date()
                            end_time = end_datetime.time()
                            end = parser.parse('%s %s' % (end_date, end_time))
                        else:
                            end = datetime.datetime.now()
                        start_datetime = timesheet['sg_task_start']
                        start_date = start_datetime.date()
                        start_time = start_datetime.time()
                        start = parser.parse('%s %s' % (start_date, start_time))

                        diff = end - start
                        total_duration += ((diff.total_seconds() / 60.0) / 60)
        return total_duration

    def get_weekly_total(self, user=None, lunch_id=None, break_id=None):
        '''
        This method will find all the time sheets for a given user for the week and total them all up.
        :param user:
        :return:
        '''
        total_duration = 0.0
        if user:
            filters = [
                ['user', 'is', {'type': 'HumanUser', 'id': user['id']}],
                {
                    "filter_operator": "any",
                    "filters": [
                        ['sg_task_start', 'in_calendar_week', 0],
                        ['sg_task_start', 'in_calendar_week', -1]
                    ]
                }
            ]
            if lunch_id:
                filters.append(
                    ['entity', 'is_not', {'type': 'Task', 'id': lunch_id}]
                )
            if break_id:
                filters.append(
                    ['entity', 'is_not', {'type': 'Task', 'id': break_id}]
                )
            fields = [
                'user',
                'duration',
                'sg_task_start',
                'sg_task_end'
            ]
            try:
                timesheets = self.sg.find('TimeLog', filters, fields)
            except (AttributeError, Exception), e:
                self.logger.error('Failed to get the timesheet! %s' % e)
                timesheets = None
            if timesheets:
                for timesheet in timesheets:
                    this_date = timesheet['sg_task_start'].date()
                    if this_date > self.start_of_week().date():
                        if timesheet['sg_task_end']:
                            end_datetime = timesheet['sg_task_end']
                            end_date = end_datetime.date()
                            end_time = end_datetime.time()
                            end = parser.parse('%s %s' % (end_date, end_time))
                        else:
                            end = datetime.datetime.now()
                        start_datetime = timesheet['sg_task_start']
                        start_date = start_datetime.date()
                        start_time = start_datetime.time()
                        start = parser.parse('%s %s' % (start_date, start_time))

                        diff = end - start
                        total_duration += ((diff.total_seconds() / 60.0) / 60)
        return total_duration

    def get_todays_lunch(self, user=None, lunch_id=None, lunch_proj_id=None):
        if user and lunch_id:
            user_id = user['id']
            filters = [
                ['project', 'is', {'type': 'Project', 'id': lunch_proj_id}],
                ['user', 'is', {'type': 'HumanUser', 'id': user_id}],
                ['entity', 'is', {'type': 'Task', 'id': lunch_id}],
                {
                    "filter_operator": "any",
                    "filters": [
                        ['sg_task_start', 'in_calendar_day', 0]
                    ]
                }
            ]
            fields = [
                'user',
                'date',
                'sg_task_start',
                'sg_task_end',
                'project',
                'entity',
                'duration'
            ]
            try:
                get_lunch = self.sg.find('TimeLog', filters, fields)
            except AttributeError, e:
                print('Get Lunch failed.  Trying again.')
                get_lunch = self.get_todays_lunch(user=user, lunch_id=lunch_id, lunch_proj_id=lunch_proj_id)
            if get_lunch:
                print('lunch_returns: %s' % get_lunch)
                return get_lunch
            else:
                print('No lunch for you!')
                return False

    def create_lunch_break(self, user=None, lunch_id=None, task_id=None):
        if user:
            print('hello')

    def is_user_clocked_in(self, user=None):
        if user:
            self.logger.debug('Looking to see if %s is clocked in....' % user['name'])
            user_id = user['id']

            # List all the timesheets for the user
            filters = [
                ['user', 'is', {'type': 'HumanUser', 'id': user_id}]
            ]
            fields = [
                'user',
                'sg_task_start',
                'sg_task_end'
            ]
            try:
                clocked_in = self.sg.find_one('TimeLog', filters, fields, order=[{'field_name': 'sg_task_start',
                                                                                  'direction': 'desc'},
                                                                                 {'field_name': 'id',
                                                                                  'direction': 'desc'}])
            except Exception, e:
                self.logger.error('Could not check clocked in: %s' % e)
                clocked_in = None

            if clocked_in and clocked_in['sg_task_end']:
                return False
            return True

    def get_timesheet_by_id(self, tid=None):
        if tid:
            filters = [
                ['id', 'is', tid]
            ]
            fields = [
                'user',
                'sg_task_start',
                'sg_task_end',
                'project',
                'entity',
                'duration'
            ]
            conn_attempts = 0
            timesheet = None
            while True:
                try:
                    timesheet = self.sg.find_one('TimeLog', filters, fields)
                except Exception as e:
                    if conn_attempts > 5:
                        self.logger.error('Failed to connect!')
                        break
                    else:
                        self.logger.error('Bad connection.  Trying again...')
                        conn_attempts += 1
                        time.sleep(2)
                if timesheet:
                    return timesheet
        return None

    def timesheet_cleanup(self, user=None):
        """
        This method is designed to check for dead or accidental timesheets.  Time sheets that are not current, and
        which still have open ended records. i.e. More than one timesheet that hasn't been clocked out.
        It gets a collection of open ended timesheets for a user.
        If there is more than one record, then it double checks that the opened one is the most recent (might need to
        do that anyways)
        If there is more than one record, then a new collection gets all the timesheets surrounding the empty timesheet.
        It will check the next record's start time. If the start time is the same, either delete the duplicate record,
        or set its out time to the in time.
        If it aint_today, then it will check for EOD status, and clock it out at the EOD, or thereafter.
        :return: 'Cleaned' or 'Clean'
        """
        if user:
            filters = [
                ['user', 'is', {'type': 'HumanUser', 'id': user['id']}],
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
                empties = self.sg.find('TimeLog', filters, fields, order=[{'field_name': 'id', 'direction': 'desc'}])
            except Exception as e:
                self.logger.error('Couldn\'t get emtpies. Connection failure: %s' % e)
                empties = None
            if empties:
                latest_timesheet = {'project': None}
                tries = 0
                while not latest_timesheet['project'] and tries < 10:
                    latest_timesheet = self.get_latest_timesheet(user=user)
                    tries += 1
                    time.sleep(5)
                if not latest_timesheet['project']:
                    return False
                latest_id = latest_timesheet['id']
                for empty in empties:
                    if empty['id'] != latest_id:
                        date = empty['date']
                        if type(date) != datetime or type(date) != datetime.datetime:
                            date = parser.parse(date).date()
                        sell_by_date = datetime.datetime.date(datetime.datetime.now()) - datetime.timedelta(days=30)
                        if date > sell_by_date:
                            if not empty['sg_task_start'] and not empty['sg_task_end']:
                                print('Total shitshow.  Ignore or delete.')
                            elif empty['sg_task_start'] and not empty['sg_task_end']:
                                next_ts = None
                                get_next_id = empty['id'] + 1
                                while not next_ts:
                                    try_next = self.get_timesheet_by_id(tid=get_next_id)
                                    if try_next and try_next['user']['id'] == user['id']:
                                        print('Found Next!')
                                        next_ts = try_next
                                        break
                                    get_next_id += 1
                                next_start = next_ts['sg_task_start']
                                print(type(next_start))
                                if type(next_start) != datetime.datetime:
                                    next_start = parser.parse(next_start)
                                if self.aint_today(next_start):
                                    print('Current timesheet is from previous day!')
                                    # Compare start time to EOD, if before: set EOD, else: set start time + 5 minutes.
                                else:
                                    data = {
                                        'sg_task_end': next_ts['sg_task_start'],
                                        'description': 'Time Lord Cleanup Processed'
                                    }
                                    tries = 0
                                    try:
                                        update = self.sg.update('TimeLog', empty['id'], data)
                                    except Exception as e:
                                        # FIXME: This does nothing!
                                        tries += 1
                                        self.logger.error('Cleanup process failed while updating... '
                                                          'Making another atempt: #%i' % tries)
                                        self.logger.error('Issue: %s' % e)
                                        if tries > 10:
                                            self.logger.error('Total Failure! %s' % e)
                                            return False
                                        update = None

                                    print('Updated: %s' % update)
                return empties

        return False

    def timesheet_consistency_cleanup(self, user=None, clock_out=False):
        end = datetime.datetime.now()
        start = (end - datetime.timedelta(days=1))
        filters = [
            ['user', 'is', {'type': 'HumanUser', 'id': user['id']}],
            {
                "filter_operator": "all",
                "filters": [
                    ['sg_task_start', 'greater_than', start],
                ]
            }
        ]
        if clock_out:
            filters.append(
                {
                    "filter_operator": "any",
                    "filters": [
                        ['sg_task_end', 'less_than', end],
                        ['sg_task_end', 'is', None]
                    ]
                }
            )
        else:
            filters.append(
                ['sg_task_end', 'less_than', end]
            )
        fields = [
            'user',
            'duration',
            'sg_task_start',
            'sg_task_end'
        ]
        try:
            get_timesheets = self.sg.find('TimeLog', filters, fields, order=[{'field_name': 'id', 'direction': 'desc'}])
        except Exception:
            print(Exception)
            return False
        try:
            ordered_timesheets = sorted(get_timesheets, key=lambda x: (x['sg_task_start'], x['sg_task_end']),
                                        reverse=True)
        except TypeError as e:
            self.logger.warning('Missing data for sort.  Switching methods')
            ordered_timesheets = sorted(get_timesheets, key=lambda x: (x('sg_task_start'), x['id']), reverse=True)
        except Exception as e:
            self.logger.error('Could not order the timesheets!')
            return False
        ts_count = len(ordered_timesheets)
        updates = []

        for ts in range(0, ts_count):
            current_start = ordered_timesheets[ts]['sg_task_start']
            current_end = ordered_timesheets[ts]['sg_task_end']

            # Check for timesheets that have excessive hours, or go across days
            if type(current_start) == datetime.datetime and type(current_end) == datetime.datetime:
                current_start_date = current_start.date()
                current_end_date = current_end.date()
                if current_start_date != current_end_date:
                    data = {
                        'sg_needs_approval': True
                    }
                    update = self.sg.update('TimeLog', ordered_timesheets[ts]['id'], data)
                    print 'Update Needs Approval'
                    updates.append(update)

            # Check Duration
            duration = ordered_timesheets[ts]['duration']
            if duration > self.double_time_mins or duration < 0:
                data = {
                    'sg_needs_approval': True
                }
                update = self.sg.update('TimeLog', ordered_timesheets[ts]['id'], data)
                print 'Update Needs Approval on Duration'
                updates.append(update)

            # Check against previous time sheets
            if (ts + 1) > ts_count:
                break
            try:
                previous_start = ordered_timesheets[ts+1]['sg_task_start']
                previous_end = ordered_timesheets[ts+1]['sg_task_end']
                previous_id = int(ordered_timesheets[ts+1]['id'])
            except Exception as e:
                print('Timesheet consistency error: %s' % e)
                previous_start = None
                previous_end = None
                previous_id = None
            if previous_end and current_start:
                if previous_end > current_start:
                    if ts == ts_count - 1:
                        previous_end = ordered_timesheets[ts-1]['sg_task_start']
                    else:
                        previous_end = current_start
                    data = {
                        'sg_task_end': previous_end
                    }
                    try:
                        update = self.sg.update('TimeLog', previous_id, data)
                        print 'update output: %s' % update
                        updates.append(update)
                    except AttributeError as e:
                        self.logger.error('Failed to update the TimeLog.')
                        # NOTE: I could probably add a retry here.

        return updates

    def get_user_total_in_range(self, user=None, start=None, end=None, lunch_id=None, break_id=None):
        total_duration = 0.0
        if user and start and end:
            start = parser.parse(start)
            end = parser.parse(end)

            filters = [
                ['user', 'is', {'type': 'HumanUser', 'id': user}],
                {
                    "filter_operator": "all",
                    "filters": [
                        ['sg_task_start', 'greater_than', start],
                        ['sg_task_end', 'less_than', end]
                    ]
                },
                ['duration', 'greater_than', 0.0]
            ]
            if lunch_id:
                filters.append(
                    ['entity', 'is_not', {'type': 'Task', 'id': lunch_id}]
                )
            if break_id:
                filters.append(
                    ['entity', 'is_not', {'type': 'Task', 'id': break_id}]
                )
            fields = [
                'user',
                'duration',
                'sg_task_start',
                'sg_task_end'
            ]
            get_timesheets = self.sg.find('TimeLog', filters, fields, order=[{'field_name': 'id', 'direction': 'desc'}])
            if get_timesheets:
                for timesheet in get_timesheets:
                    total_duration += (float(timesheet['duration']) / 60.0)
        return total_duration

