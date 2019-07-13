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

import datetime
import logging
from dateutil import parser
from dateutil import relativedelta


class continuum(object):
    def __init__(self, sg=None):
        self.logger = logging.getLogger('psychic_paper.continuum')
        self.logger.info('Continuum Activated!')
        self.sg = sg

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
        self.logger.debug('Date type: %s' % type(date))
        if type(date) == datetime or datetime.datetime:
            self.logger.debug('datetime detected.  Converting date to string...')
            date = str(date)
            self.logger.info('Date converted: %s' % date)
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
                'entity'
            ]
            last_timesheet = self.sg.find_one('TimeLog', filters, fields, order=[{'field_name': 'id', 'direction': 'desc'}])
            if last_timesheet:
                return last_timesheet
            return None

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
            project_name = context['Project']['name']
            task_id = context['Task']['id']
            task_name = context['Task']['content']
            entity_id = context['Entity']['id']
            entity_name = context['Entity']['code']
            user_id = user['id']
            print context

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
                    h = '%02d' % int(split_time[0])
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
            except TypeError, e:
                self.logger.error('Yeah, the shit hit the fan: %s' % e)
        return running_time

    def get_daily_total(self, user=None):
        '''
        This method will search all of the timesheets for a given user, for a given day, and total up the hours.
        :param user: (dict) The main user data
        :return: A total daily hours number
        '''
        total_duration = 0.0
        if user:
            filters = [
                ['user', 'is', {'type': 'HumanUser', 'id': user['id']}],
                ['sg_task_start', 'in_calendar_day', 0]
            ]
            fields = [
                'user',
                'duration',
                'sg_task_start',
                'sg_task_end'
            ]
            timesheets = self.sg.find('TimeLog', filters, fields)
            if timesheets:
                for timesheet in timesheets:
                    total_duration += timesheet['duration']
        return total_duration

    def get_weekly_total(self, user=None):
        '''
        This method will find all the time sheets for a given user for the week and total them all up.
        :param user:
        :return:
        '''

