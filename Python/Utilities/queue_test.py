import threading as t
import Queue as q

test = ['Test 1', 'test 2', 'test 3', 'test 4', 'test 5', 'test 6', 'test 7', 'test 8', 'test 9', 'test 10']
que = q.Queue(maxsize=0)


def poop(que):
    print 'Thread Started'
    while not que.empty():
        print que.get()
        que.task_done()
        print 'Task Done'


for d in test:
    que.put(d)
    # print '%s added to queue' % d

que.put('Dickless wonder')

# que.join()

fart = t.Thread(target=poop, args=que)
fart.setDaemon(True)
fart.start()

# poop(que)