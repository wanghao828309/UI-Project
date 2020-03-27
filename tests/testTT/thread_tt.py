#coding=utf-8
import threading,time
from time import ctime,sleep


def music(func):
    for i in range(2):
        print "I was listening to %s. %s" %(func,ctime())
        sleep(1)

def move(func):
    for i in range(2):
        print "I was at the %s! %s" %(func,ctime())
        sleep(2)
        print "I was at the %s! %s" % (func, ctime())

def print_time( threadName, delay=1):
    count = 0
    while count < 2:
        time.sleep(1)
        # print delay
        count += 1
        # print count
        print "%s: %s" % ( threadName, time.ctime(time.time()) )

threads = []
t1 = threading.Thread(target=music,args=(u'爱情买卖',))
threads.append(t1)
t2 = threading.Thread(target=move,args=(u'阿凡达',))
threads.append(t2)

if __name__ == '__main__':
    threads = []
    for i in range(0,6):
        threads.append(threading.Thread(target=print_time, args=(u'爱',i)))
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

    # print "\nall over %s" %ctime()