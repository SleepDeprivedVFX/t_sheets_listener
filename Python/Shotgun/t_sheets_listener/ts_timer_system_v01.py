
import ctypes
import sys
import time
from datetime import datetime

from ui import alert_dialog as ad
from ui import lunch_break_dialog as lbd

import sys, time
from PySide.QtGui import *
from PySide.QtCore import *

lunch_start_time = '00:00'
lunch_end_time = '23:59'
ts_buffer = QWaitCondition()
buffer_not_full = QWaitCondition()
mutex = QMutex()


class ts_signal(QObject):
    sig = Signal(str)
    lunch = Signal(str)
    alert = Signal(str)
