from datetime import datetime

early_eod = '16:00'
today = datetime.now().date()
eod = datetime.strptime('%s %s' % (today, early_eod), '%Y-%m-%d %H:%M').time()
now = datetime.now().time()

if eod < now:
    print('Yea!')

