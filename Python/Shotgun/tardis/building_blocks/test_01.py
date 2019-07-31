from PySide import QtGui
import sys
import time
import subprocess
import random


def run_popup():
    msg = QtGui.QMessageBox()
    msg.setText('Fuckin A')
    msg.setInformativeText('Wiki wiki whack!')
    msg.setWindowTitle('Fart Knocker')
    msg.setDetailedText('The eating of shit is disgusting.')
    msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
    msg.buttonClicked.connect(fart)
    msg.exec_()


def counter():
    turd = True
    msgs = [
        'Are you sure you want to delete this file?  Hit OK to delete!',
        'This file is corrupted.  Would you like to delete it?  Hit OK to remove corrupted files.',
        'The file you are trying to open has been corrupted.',
        'The length of this file name is too thick',
        'Maya has actively crashed and opened only to crash again.',
        'Trent has actively deleted your reference files. Good luck.',
        'Seriously... It\'s all getting deleted.  Like everything...'
    ]

    # Settings
    amps = 10
    time_exponent = -2

    # Engine
    time_mult = pow(10, time_exponent)
    send_time = amps
    i = send_time
    initial_time = send_time
    t = 1
    random_slider = 1
    while int(send_time) > 0:
        if i == int(send_time):
            random_slider = int(round((1 - (send_time/initial_time)) * (len(msgs)))) + 2
            if random_slider >= (len(msgs) + 1):
                random_slider = len(msgs) + 1
            print 'NEW SEND TIME!  %s' % int(send_time)
            rando = random.randrange(0, random_slider)
            send_user_message('ryan', '10.0.1.139', msgs[rando])
            print msgs[rando]
            # run_popup()
            print 'random_slider: %s' % random_slider
            # random_slider = 2
            i = 0
            t += 1
        time.sleep(1)
        send_time = -(time_mult * (t ** 2)) + amps
        print '%i: send_time: %s' % (i, int(send_time)), send_time
        i += 1


def fart(msg):
    print 'Here\'s some shit to say %s to.' % msg.text()


def send_user_message(user=None, ip=None, msg=None):
    if user and ip:
        subprocess.call("msg /time:300 /server:%s %s %s" % (ip, user, msg))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    w.hide()
    counter()
    sys.exit(app.exec_())
