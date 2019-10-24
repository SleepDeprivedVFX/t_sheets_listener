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

__author__ = 'Adam Benson'
__version__ = '0.1.0'

import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys
from dateutil import parser
from dateutil import relativedelta
import time


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
            self.logger.info('prev_day: %s' % prev_day)

            is_last_week = self.time_from_last_week(start_time=prev_day)
            self.logger.info('is last week? %s' % is_last_week)

            is_weekday = self.date_is_weekday(date=prev_day)
            is_wd = is_weekday[0]
            weekday = is_weekday[1]
            if is_wd:
                self.logger.info('is_weekday: %s' % weekday)
                if weekday in regular_days:
                    self.logger.info('Regular day %s' % weekday)
            else:
                self.logger.info('NOT a weekday! %s' % weekday)
                while weekday not in regular_days:
                    prev_day = prev_day - relativedelta.relativedelta(days=1)
                    is_weekday = self.date_is_weekday(date=prev_day)
                    weekday = is_weekday[1]
                self.logger.info('Now the weekday is: %s' % weekday)
                self.logger.info('And the new date is: %s' % prev_day)

        return prev_day

    def get_last_timesheet(self, user=None):
        if user:
            self.logger.info('Finding the last timesheet for %s' % user['name'])
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
                last_timesheet = self.sg.find_one('TimeLog', filters, fields, order=[{'field_name': 'id',
                                                                                      'direction': 'desc'}])
                self.logger.debug('Timesheet found: %s' % last_timesheet)
            except (AttributeError, Exception), e:
                self.logger.error('Something unexpected happened while getting the last timesheet: %s' % e)
                last_timesheet = None
            if last_timesheet:
                return last_timesheet
            return {'sg_task_end': None, 'entity': None, 'project': None, 'date': '', 'sg_task_start': None}

    def assume_end_time(self, start_time=None, eod=None):
        self.logger.info('Assuming an end time from the date and configuration...')
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
            self.sg.update('TimeLog', timesheet['id'], data)
            self.logger.info('Timesheet updated.')

    def create_new_timesheet(self, user=None, context=None, start_time=None, entry='User'):
        '''
        Creates a new timesheet.  Works with Stand alone, DCC and drag-n-drop publisher
        :param user: (dict) Contains the Shotgun User ID number
        :param context: (dict) A Shotgun Context Object. Can be built manually.
        :param start_time: (datetime) a date and time to start the clock, usually datetime.now()
        :param entry: (str) This tells the system where it camer from:
                                User = Standalone
                                DCC  = SG Integrated Software
                                Auto = Drag-n-Drop Publisher
        :return: New timesheet.
        '''
        if user and context:
            project_id = context['Project']['id']
            task_id = context['Task']['id']
            user_id = user['id']
            self.logger.debug(context)

            if start_time and type(start_time) == datetime or datetime.datetime:
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
            timesheet = self.sg.create('TimeLog', data)
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
            self.logger.info('Looking to see if %s is clocked in....' % user['name'])
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
                clocked_in = self.sg.find_one('TimeLog', filters, fields, order=[{'field_name': 'id',
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
                        return False
                    else:
                        self.logger.error('Bad connection.  Trying again...')
                        conn_attempts += 1
                        time.sleep(2)
                if timesheet:
                    return timesheet
        return None


