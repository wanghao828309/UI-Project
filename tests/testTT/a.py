# -*- coding:utf-8 -*-
import os, sys, shutil,datetime
import win32com.client
reload(sys)
sys.setdefaultencoding('utf8')

class a():
    def __init__(self):
        self.s = 1

    def test(self):
        k = 2
        # print self.s
        return self.s



def check_exsit(process_name):
    """
    判断进程是否存在
    """
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    if len(processCodeCov) > 0:
        return True
    else:
        print ('%s is not exists' % process_name)
        return False
def close_process(process_name):
    """
    Close all process by process name.
    """
    res = check_exsit(process_name)
    print res
    try:
        if res == True:
            print ('%s is exists' % process_name)
            os.system("taskkill /f /im " + process_name)
    except Exception:
        print ('%s is not exists' % process_name)


if __name__ == '__main__':
    close_process("firefox.exe")