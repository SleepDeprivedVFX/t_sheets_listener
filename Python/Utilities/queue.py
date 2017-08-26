import os
import time as t
import threading as th

class queue:
    def __init__(self):
        self._generator = None
        self._timerId = None
        self.set_timer = [0, 0, 1, 0]

    def loop_generator(self):
        s = 0
        m = 0
        h = 0
        d = 0
        # Counters c is short for Counter: cs = CounterSeconds = 5
        cs = int(self.set_timer[3])
        cm = int(self.set_timer[2])
        ch = int(self.set_timer[1])
        cd = int(self.set_timer[0])

        lastTime = [0, 0, 0, 0]
        while self._generator:
            # Time interval settings and counting
            if s < 59:
                s += 1
            else:
                if m < 59:
                    s = 0
                    m += 1
                    # Close the log file and reinitialize another one.
                elif m == 59 and h < 24:
                    h += 1
                    m = 0
                    s = 0
                elif m == 59 and h == 24:
                    d += 1
                    h = 0
                    m = 0
                    s = 0

            ts = s - cs
            tm = m - cm
            th = h - ch
            td = d - cd
            t_time = [abs(td), abs(th), abs(tm), abs(ts)]
            if t_time == lastTime:
                # reset lastTime
                lastTime = [d, h, m, s]
                # Begin timed event triggers
                # Run first thread here
            print(d, h, m, s)
            yield

    # ---------------------------------------------------------------------------------------------------------------
    # Timer Generator Events
    # ---------------------------------------------------------------------------------------------------------------
    def timerEvent(self, event):
        if self._generator is None:
            return
        try:
            next(self._generator)
        except StopIteration:
            self.stop()

    # ---------------------------------------------------------------------------------------------------------------
    # Stop Timer
    # ---------------------------------------------------------------------------------------------------------------
    def stop(self):
        if self._timerId is not None:
            self.killTimer(self._timerId)
            # logger.info('Loop Stopped!  Auto Publisher Paused!')
            # self.ui.set_days.setEnabled(True)
            # self.ui.set_hours.setEnabled(True)
            # self.ui.set_minutes.setEnabled(True)
            # self.ui.set_seconds.setEnabled(True)
        self._generator = None
        self._timerId = None

    # ---------------------------------------------------------------------------------------------------------------
    # Start Timer
    # ---------------------------------------------------------------------------------------------------------------
    def start(self):
        self.stop()
        days = 0
        hours = 0
        minutes = 0
        seconds = 30
        # self.dropbox = self.ui.watch_folder.text() + '/'
        # logger.info('Watch_folder set to %s' % self.dropbox)
        # self.ui.set_days.setEnabled(False)
        # self.ui.set_hours.setEnabled(False)
        # self.ui.set_minutes.setEnabled(False)
        # self.ui.set_seconds.setEnabled(False)
        self.set_timer = [days, hours, minutes, seconds]
        # logger.info('Timer set to %s' % self.set_timer)
        self._generator = self.loop_generator()
        self._timerId = t.localtime()
        # logger.info('Loop Started!  Beginning Auto Publisher...')

if __name__ == '__main__':
    run = queue()
    run.start()