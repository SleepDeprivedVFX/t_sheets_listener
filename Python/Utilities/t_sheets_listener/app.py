from libs.pynput import mouse
import time


class t_sheets_listener:
    def __init__(self):
        self.h = 0
        self.m = 0
        self.s = 0
        self.ts_timer = True
        self.run_loop()

    def run_loop(self):
        while self.ts_timer:
            self.s += 1
            print self.s
            time.sleep(1)
            if self.s > 20:
                self.ts_timer = False


# def on_click(x, y, button, pressed):
#     # print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
#     s = 0
#     m = 0
#     h = 0
#     if pressed:
#         print 'Pressed'

# Collect events until released
# with mouse.Listener(on_click=on_click) as listener:
#     # d = t_sheets_listener()
#     listener.join()

mouse.Listener(on_click=on_click)

