from libs.pynput import mouse
import time
import ctypes
from ctypes import windll
import multiprocessing as mp

class ts_timer:
    def __init__(self):
        self.ts_timer, self.ts_mouse = mp.Pipe()
        self.run_time = True
        self.run_timer()

    def run_timer(self):
        s = 0
        while self.run_time:
            s += 0
            self.ts_timer.recv()

    def mouse_check(self):
        while self.run_time:
            if ctypes.windll.user32.GetKeyState(0x01) not in [0, 1]:
                self.ts_mouse.send(0)

ts_timer()
