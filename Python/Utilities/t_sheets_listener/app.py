from libs.pynput import mouse
import time
from datetime import datetime, timedelta
import ctypes
from ctypes import windll
import multiprocessing as mp

class ts_timer:
    def __init__(self):
        self.run_time = True
        self.run_timer()

    def run_timer(self):
        s = 0
        m = 0
        h = 0
        r = 0.0
        break_timer = False
        while self.run_time:
            r += 1.0
            t = float(r/1000)
            if t.is_integer():
                now_date = str(datetime.date(datetime.now()))
                now_time = str(datetime.time(datetime.now()))
                split_date = now_date.split('-')
                split_time = now_time.split(':')
                clock_h = int(split_time[0])
                clock_m = int(split_time[1])
                get_s = split_time[2].split('.')[0]
                clock_s = int(get_s)
                if s < 59:
                    s += 1
                else:
                    if m < 59:
                        s = 0
                        m += 1
                    elif m == 59 and h <= 22:
                        h += 1
                        m = 0
                        s = 0
                print '%s:%s:%s' % (h, m, s)
                if m >= 1 and not break_timer:
                    # this will eventually be set to 15 minutes
                    start_break = datetime.now() - timedelta(minutes=1)
                    print 'Start Break At: %s' % start_break
                    break_timer = True

            if ctypes.windll.user32.GetKeyState(0x01) not in [0, 1]:
                if break_timer:
                    end_break = datetime.now()
                    start_s = start_break.strftime('%Y-%m-%d %H:%M:%S')
                    end_s = end_break.strftime('%Y-%m-%d %H:%M:%S')
                    break_time = datetime.strptime(end_s, '%Y-%m-%d %H:%M:%S') - datetime.strptime(start_s, '%Y-%m-%d %H:%M:%S')
                    break_timer = False
                    print 'Break Time: %s' % break_time
                s = 0
                m = 0
                h = 0
            time.sleep(0.001)

ts_timer()


