from ctypes import windll, Structure, c_long, byref
import time
import psutil
import subprocess


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
# path = r'\\skynet\Jobs\asc_promo\publish\2012\2012_I,Frankenstein\Adam-Close-2.jpg'
# import os
# import shutil
# if os.path.exists(path):
#     shutil.copy2(path, r'C:\Users\adamb\Desktop')

class tardis_test:
    def main(self):
        while True:
            print '-' * 120
            test = True
            for proc in psutil.process_iter():
                try:
                    print proc.name().lower()
                    if 'notepad.exe' == proc.name().lower():
                        print 'SHIT YEAH'
                        test = False
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            if test:
                subprocess.Popen('C:\\Windows\\notepad.exe', close_fds=True | subprocess.CREATE_NEW_PROCESS_GROUP)


if __name__ == '__main__':
    t = tardis_test()
    t.main()