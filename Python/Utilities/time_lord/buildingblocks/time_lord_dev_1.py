import shotgun_api3 as sgapi
import os
import sys
import datetime
import ConfigParser

# Engines
from bin.time_continuum import continuum

sys_path = sys.path
config_file = 'tardis_config.cfg'
try:
    print('Finding configuration file...')
    config_path = [f for f in sys_path if os.path.isfile(f + '/' + config_file)][0] + '/' + config_file
    config_path = config_path.replace('\\', '/')
    print('Configuration found!')
except IndexError, e:
    raise e

configuration = ConfigParser.ConfigParser()
print('Reading the configuration file...')
configuration.read(config_path)

cfg_sg_url = configuration.get('Shotgun', 'sg_url')
cfg_sg_key = configuration.get('Shotgun', 'sg_key')
cfg_sg_name = configuration.get('Shotgun', 'sg_name')

sg = sgapi.Shotgun(cfg_sg_url, cfg_sg_name, cfg_sg_key)

# set the continuum
cont = continuum()

# Get the first day of the week
week_start = cont.start_of_week()

right_now = datetime.datetime.now()

# List by a specific user
filters = [
    ['user', 'is', {'type': 'HumanUser', 'id': 41}],
    ['sg_task_end', 'is', None],
    ['sg_task_start', 'is_not', None],
    ['sg_task_start', 'greater_than', week_start]
]
fields = [
    'user',
    'date',
    'sg_task_start',
    'sg_task_end'
]
no_out_time = sg.find('TimeLog', filters, fields)
print(no_out_time)

filters = [
    ['user', 'is', {'type': 'HumanUser', 'id': 41}],
    ['sg_task_start', 'is_not', None],
    ['sg_task_start', 'greater_than', week_start]
]
all_recent_time = sg.find('TimeLog', filters, fields)
print(all_recent_time)
i = 1

# sort them so that they are in order of start time (manual entries can be anything!)
sorted_no_out_time = sorted(no_out_time, key=lambda i: i['sg_task_start'])
sorted_all_recent_time = sorted(all_recent_time, key=lambda i: i['sg_task_start'])

if len(sorted_no_out_time) > 1:
    # Check for too many active time cards
    flag = 'A red flag!  Too many empty times!'
    print(flag)

    # save the latest time sheet into it's own variable.  This will be our "master" time sheet.
    # Compare the latest empty to the latest all records
    latest_no_out_time = sorted_no_out_time[-1]
    latest_all_recent_time = sorted_all_recent_time[-1]
    print 'The latest empty: %s' % latest_no_out_time
    print 'The latest all records: %s' % latest_all_recent_time
    if latest_all_recent_time != latest_no_out_time:
        print 'OH FUCK!!!!'
    print 'length of test: %s' % len(sorted_no_out_time)

    # Now reverse the order of the list for some additive comparisons.
    # test = sorted(test, reverse=-1)
    # print 'reversed test = %s' % test
    # Go through the errant time sheets and set the clock out times.
    # TODO: Eventually this will need to check against previous day and weekend times.  But for now...
    #       This will also need to check for skipped time entries:
    #           Clockin: Friday @ 10am - Clockout: None
    #           Clockin: Monday @ 10am - Clockout: Monday @ 1pm
    #           Clockin: Monday @ 2pm  - Clockout: Monday @ 3pm
    #           Clockin: Monday @ 3pm  - Clockout: None
    #       It will have to be able to check not only previous times, but previous records.
    #       This might take several comparable databases or entry comparisons.
    for ot in range(0, len(sorted_no_out_time)):
        print 'ot: %s' % ot
        # Now to get the previous start time. To do this, I will need to get the ID from the sorted_no_out_time and
        # then cycle through the sorted_all_recent_time list to find a matching ID number AND index from the
        # sorted_all_recent_time record, so that I can add 1 to that index and retrieve the next start time from there.
        no_out_ID = sorted_no_out_time[ot]['id']
        next_start_time = None
        for this in sorted_all_recent_time:
            if this['id'] == no_out_ID:
                recent_id = sorted_all_recent_time.index(this)
                next_id = recent_id + 1

                # Check to see if the list is longer than the indexes
                if next_id > (len(sorted_all_recent_time) - 1):
                    print 'LIST TOO LONG: %s' % len(sorted_all_recent_time)
                    break
                next_start_time = sorted_all_recent_time[next_id]['sg_task_start']
                break

        try:
            if next_start_time:
                new_end = next_start_time
            else:
                new_end = sorted_no_out_time[ot + 1]['sg_task_start']
            print 'new_end: %s' % new_end
            # Apply it or the latest time sheet's start time to the last time sheet's end time.
            try:
                sorted_no_out_time[ot]['sg_task_end'] = new_end
                data = {
                    'sg_task_end': new_end
                }
                t_id = sorted_no_out_time[ot]['id']
                sg.update('TimeLog', t_id, data)
            except IndexError, KeyError:
                sorted_no_out_time[ot]['sg_task_end'] = latest_no_out_time['sg_task_start']
                data = {
                    'sg_task_end': latest_no_out_time['sg_task_start']
                }
                t_id = sorted_no_out_time[ot]['id']
                sg.update('TimeLog', t_id, data)
            print 'task end: %s' % sorted_no_out_time[ot]['sg_task_end']
        except:
            pass


for t in sorted_no_out_time:
    if t['sg_task_start']:
        # Check the current start time against the first of the week.

        # Important IF:
        #   If someone forgets to clock out last weekend, then the system will either have to auto-clock them out at
        #   7PM (configurable) or it will have to do a soft filter and a hard filter.
        #   Hard filter:
        #       Filters out anything greater than date X, let's say one month.
        #   Soft filter:
        #       Filters out anything greater than the first of the week.
        #   This way, it's easy to do by the week calculations (and trigger events) for the big numbers, and absolute
        #   cut off dates for old time sheets has a limit.
        start_time = t['sg_task_start']
        start_time = start_time.replace(tzinfo=None)
        print 'start_time: %s' % start_time
        print 't[sg_task_end]: %s' % t['sg_task_end']
        print 'week start: %s' % week_start
        if start_time > week_start:
            # At this point checks for multiple time sheets can come into play.
            user = t['user']
            ts_date = t['date']
            end_time = t['sg_task_end']




# from sys import argv, exit
# from PySide import QtCore, QtGui
#
#
# class Clock(QtGui.QWidget):
#    def __init__(self, parent=None):
#         super(Clock, self).__init__(parent)
#         # timer
#         # NOT SURE WHAT THIS IS DOING OR WHERE TO PUT IT IN MY OWN CONTEXT
#         # Might need to create a signal for this.  Not sure yet, but I'll make it work.
#         # The ...connect(self.update) belongs with the QWidget, since that's what's being updated.
#         timer = QtCore.QTimer(self)
#         timer.timeout.connect(self.update)
#         timer.start(1000)
#
#         # DON'T NEED THIS FOR TIMER
#         # window
#         self.setWindowIcon(QtGui.QIcon('Default.png'))
#         self.setWindowTitle('Clock')
#         self.resize(200, 200)
#         # hour pointer
#
#         # DON'T NEED THIS FOR TIMER
#         self.hPointer = QtGui.QPolygon([
#          QtCore.QPoint(6, 7),
#          QtCore.QPoint(-6, 7),
#          QtCore.QPoint(0, -50)
#         ])
#         # minute pointer
#         self.mPointer = QtGui.QPolygon([
#          QtCore.QPoint(6, 7),
#          QtCore.QPoint(-6, 7),
#          QtCore.QPoint(0, -70)
#         ])
#         # second pointer
#         self.sPointer = QtGui.QPolygon([
#          QtCore.QPoint(1, 1),
#          QtCore.QPoint(-1, 1),
#          QtCore.QPoint(0, -90)
#         ])
#         # colors
#         self.bColor = QtGui.QColor('#0000aa') #hours and minutes
#         self.sColor = QtGui.QColor('#aa0087')
#
#    def paintEvent(self, event):
#         rec = min(self.width(), self.height())
#         tik = QtCore.QTime.currentTime()
#         # painter
#         painter = QtGui.QPainter(self)
#         # zipping code to draw pointers
#
#         def drawPointer(color, rotation, pointer):
#             painter.setBrush(QtGui.QBrush(color))
#             painter.save()
#             painter.rotate(rotation)
#             painter.drawConvexPolygon(pointer)
#             painter.restore()
#
#         # tune up painter
#         painter.setRenderHint(QtGui.QPainter.Antialiasing)
#         painter.translate(self.width() / 2, self.height() / 2)
#         painter.scale(rec / 200, rec / 200)
#         painter.setPen(QtCore.Qt.NoPen)
#         # draw pointers
#         drawPointer(self.bColor, (30 * (tik.hour() + tik.minute() / 60)), self.hPointer)
#         drawPointer(self.bColor, (6 * (tik.minute() + tik.second() / 60)), self.mPointer)
#         drawPointer(self.sColor, (6 * tik.second()), self.sPointer)
#         # draw face
#         painter.setPen(QtGui.QPen(self.bColor))
#         for i in range(0, 60):
#             if (i % 5) != 6:
#                 painter.drawLine(87, 0, 97, 0)
#             painter.rotate(6)
#         painter.end()
#
#
# if __name__ == '__main__':
#    app = QtGui.QApplication(argv)
#    win = Clock()
#    win.show()
#    exit(app.exec_())