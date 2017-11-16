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
            now_hour = datetime.now().hour
            now_min = datetime.now().minute
            r += 1.0
            t = float(r/1000)
            if t.is_integer():
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
                if s >= 15 and not break_timer:
                    if now_hour >= 1 and now_min >= 15:
                        print 'Min Time condition met'
                        if now_hour < 14 and now_min < 35:
                            print 'Max time condition met'
                            # this will eventually be set to 15 minutes
                            start_break = datetime.now()  # - timedelta(minutes=1)
                            print 'Start Break At: %s' % start_break
                            break_timer = True

            if ctypes.windll.user32.GetKeyState(0x01) not in [0, 1]:
                if break_timer:
                    end_break = datetime.now()
                    break_time = end_break - start_break
                    print 'Open Lunch Menu'
                    break_timer = False
                    print 'Break Time: %s' % break_time
                s = 0
                m = 0
                h = 0
            time.sleep(0.001)

ts_timer()


