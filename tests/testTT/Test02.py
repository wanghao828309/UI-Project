# coding=utf-8

# class ClassTest(object):
#     __num = 0
#     @classmethod
#     def addNum(self):
#         self.__num += 1
#     @classmethod
#     def getNum(self):
#         return self.__num
#      
#     def __new__(self):
#         ClassTest.addNum()
#         return super(ClassTest,self).__new__(self)
#      
# class Student(ClassTest):
#     def __init__(self):
#         self.name = ''
#            
#  
# a = Student()
# b = Student()
# print ClassTest.getNum() 



class Student():
    def __init__(self):
        self.name = ''
        
    def __aa(self):
        print "aa"
        
    def bb(self):
        self.__aa()
        print "bb"
   
# from termcolor import colored, cprint
#
#
# class colour:
#     @staticmethod
#     def c(msg, colour):
#         try:
#             from termcolor import colored, cprint
#             p = lambda x: cprint(x, '%s' % colour)
#             return p(msg)
#         except:
#             print (msg)
#
#     @staticmethod
#     def show_verbose(msg):
# #         cprint("aaa", '%s' % msg)
#         colour.c(msg, 'white')
#
#     @staticmethod
#     def show_debug(msg):
#         colour.c(msg, 'blue')
#
#     @staticmethod
#     def show_info(msg):
#         colour.c(msg, 'green')
#
#     @staticmethod
#     def show_warn(msg):
#         colour.c(msg, 'yellow')
#
#     @staticmethod
#     def show_error(msg):
#         colour.c(msg, 'red')
#
        
        
# import sys  
# from termcolor import colored, cprint  
#   
# text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])  
# print(text)  
# cprint('Hello, World!', 'green', 'on_red')  
#   
# print_red_on_cyan = lambda x: cprint(x, 'red', 'on_cyan')  
# print_red_on_cyan('Hello, World!')  
# print_red_on_cyan('Hello, Universe!')  
#   
# for i in range(10):  
#     cprint(i, 'magenta', end=' ')  
#   
# cprint("Attention!", 'red', attrs=['bold'], file=sys.stderr)

from multiprocessing.dummy import Pool as ThreadPool
import time,sys,random,multiprocessing
 
def print_time( threadName, delay=1):
    count = 0
    while count < 2:
        time.sleep(delay)
        count += 1
        print count
        print "%s: %s" % ( threadName, time.ctime(time.time()) )
        
        
if __name__ == '__main__':
    
#     COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    pool = ThreadPool(3)
    phones=("thread0","thread1")
    phones2=("thread00","thread11")
    for item in pool.map   (print_time, phones):
        if item:
            print item
            
            
    # function_list=  [1, 2, 3, 4]
    #
    # pool=multiprocessing.Pool(4)
    # for func in function_list:
    #     pool.apply_async(func)     #Pool执行函数，apply执行函数,当有一个进程执行完毕后，会添加一个新的进程到pool中
    #
    # print 'Waiting for all subprocesses done...'
    # pool.close()
    # pool.join()    #调用join之前，一定要先调用close() 函数，否则会出错, close()执行后不会有新的进程加入到pool,join函数等待素有子进程结束
    # print 'All subprocesses done.'
#     print'测试: {}'.format(random.randint(0, 999))
#     print'测试2: %s' %(random.randint(0, 999))
#     print'测试3: '+str(random.randint(0, 999))
#     suite=[1,2]
#     a = [s for s in suite if s > 0]
#     print a
    

    
#     colour.show_verbose("white")
#     colour.show_debug("blue")
#     colour.show_info("green")
#     colour.show_warn("yellow")
    pass
#     Student().bb()
