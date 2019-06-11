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

import shotgun_api3 as sgapi
import os
import sys
import datetime


class continuum(object):
    def __init__(self, sg=None, user_id=None):
        self.sg = sg
        self.user = user_id

    def start_of_week(self):
        # Get the first day of the week
        week_start = datetime.datetime.today() - datetime.timedelta(days=datetime.datetime.today().isoweekday() % 7)
        week_start = week_start.replace(tzinfo=None)
        return week_start

    def compare_latest_records(self):
        print 'Hello'
