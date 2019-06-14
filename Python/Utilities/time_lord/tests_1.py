from datetime import datetime
from dateutil import parser

test_date_1 = '2019/6/12'
test_date_2 = '2019-06-12 12:59:27,226'
test_date_3 = datetime.now()
test_date_4 = '06/08/19 02:00pm'
print test_date_1
print test_date_2
print test_date_3


def process_shit(date=None):
    print type(date)
    if type(date) == str:
        if '/' in date:
            date = date.replace('/', '-')
        date = datetime.strptime(date, 'YYYY-MM-DD')
    force_date = datetime.date(date)
    print force_date

# process_shit(test_date_4)
# print test_date_3.weekday()

this = datetime.now()

def date(d=None):
    if type(d) == datetime:
        print 'Yes'
        d = str(d)
    else:
        print 'No'
    print parser.parse(d).time()
    print parser.parse(d).date()

date(test_date_1)
