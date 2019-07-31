from ctypes import windll, Structure, c_long, byref
import time


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]



def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}


set_timer = None
# while True:
#     pos = queryMousePosition()
#     time.sleep(0.1)
#     if pos == queryMousePosition():
#         print 'Mouse stopped!'
#         if not set_timer:
#             set_timer = 1
#         else:
#             if set_timer > 200:
#                 print 'There is a long pause and...ds'
#             set_timer += 1
#     else:
#         print(pos)
#         set_timer = None
#     print 'set_timer: %s' % set_timer
#
path = r'\\skynet\Jobs\asc_promo\publish\2012\2012_I,Frankenstein\Adam-Close-2.jpg'
import os
import shutil
if os.path.exists(path):
    shutil.copy2(path, r'C:\Users\adamb\Desktop')