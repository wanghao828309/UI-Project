#coding=utf-8
from ftplib import FTP
import sys,time,datetime,subprocess
import shutil
import os
reload(sys)
sys.setdefaultencoding( "utf-8" )

#8LE-22FK2-22RKB-22M

def ftpconnect(ftpserver,username,password):
    ftp=FTP()
    # ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
    ftp.connect(ftpserver,21) #连接
    ftp.login(username,password) #登录，如果匿名登录则用空串代替即可
    # print ftp.getwelcome() #显示ftp服务器欢迎信息
    return ftp

def downloadfile(ftpconnect,remoteparentpath,localpath):
    ftpconnect.cwd(remoteparentpath)    #设置FTP当前操作的路径
    list = ftpconnect.nlst()  # 获得目录列表
    bufsize = 1024 #设置缓冲块大小
    list.sort(reverse=True)
    fp = open(localpath,'wb') #以写模式在本地打开文件
    remotepath = remoteparentpath + list[0] + "/Filmora Scrn(x64).exe"
    print u"本次安装包包路径：",remotepath
    ftpconnect.retrbinary('RETR ' + remotepath,fp.write,bufsize) #接收服务器上文件并写入本地文件
    # ftp.set_debuglevel(0) #关闭调试
    fp.close()
    ftpconnect.quit() #退出ftp服务器
    return True

def uploadfile(ftpconnect,remotepath,localpath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftpconnect.storbinary('STOR ' + remotepath, fp, bufsize)  # 上传文件
    # ftp.set_debuglevel(0)  #关闭调试
    fp.close()  # 关闭文件
    ftpconnect.quit()
    return True

def get_latest_folder(strday,list):
    for name in list:
        if str(strday) in name:
            return name

    strday = strday - datetime.timedelta(days=1)
    return get_latest_folder(strday,list)

def ClearFolder(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        time.sleep(1)
    os.makedirs(path)


if __name__ == '__main__':

    # #清理历史报告文件
    # reportpath = "D:/Squish/TestResult"
    # ClearFolder(reportpath)
    # #清理运行过程中导出文件
    # ExportFilespath = "C:/Users/ws/Documents/FilmoraScreen/ExportFiles"
    # ClearFolder(ExportFilespath)
    #
    # #退出squish
    # os.system("taskkill /im squishide.exe /f")
    #
    # # ftp基本信息
    # ftpserver = 'ftp.wspublic.cn'
    # username = 'public'
    # password = 'wonder123'
    # parentpath = u"/Artifacts10-01/Git-FilmoraScreen/master/"
    # # parentpath = u"/Artifacts10-01/Git-FilmoraScreen_EveryDay/develop/"
    # dlocalpath = u'D:/Squish/Filmora Scrn(x64).exe'
    #
    # # 下载FilmoraScreen(x64).exe
    # ftp = ftpconnect(ftpserver,username,password)
    # start = datetime.datetime.now()
    # dresult = downloadfile(ftp,parentpath,dlocalpath)
    #
    # while not dresult:
    #     time.sleep(1)
    # end = datetime.datetime.now()
    # print u"下载Filmora Scrn(x64).exe耗时：",end - start
    #
    # # 静默安装Screen
    dlocalpath = r"E:\Jenkins\workspace\filmoraWin\work\Filmora9(x64).exe"
    if os.path.isfile(dlocalpath):
        os.system(dlocalpath.replace("Filmora9(x64).exe", "\"Filmora9(x64).exe\"") + " /VERYSILENT")
        time.sleep(20)

    #
    # #设置从recorder跳转至editor
    # squishpath = "C:/Users/ws/Squish for Qt 6.2.0/bin/dllpreload.exe"
    # screenpath = "C:/Program Files/Wondershare/Filmora Scrn"
    #
    # if os.path.exists(screenpath + "/FSEditor.exe"):
    #     os.rename(screenpath + "/FSEditor.exe", screenpath + "/FSEditor_.exe")
    # else:
    #     print "Filmoar install fail,quit."
    #     quit()
    #
    # shutil.copy(squishpath, screenpath)
    # time.sleep(1)
    # os.rename(screenpath + "/dllpreload.exe", screenpath + "/FSEditor.exe")
    #
    # #查看squishserver是否已启动，启动返回0，未启动返回1
    # process = os.system('tasklist | find "_squishserver.exe"')
    # if process == 1:
    #     # 启动squishserver
    #     subprocess.Popen("C:/Users/ws/Squish for Qt 6.2.0/bin/squishserver.exe")
    #     time.sleep(3)

    # #执行指定Test Suite
    # os.system("squishrunner --testsuite D:/Squish/TestSuites/suite_LZL_FilmoraScrn_Win --reportgen html,D:/Squish/TestResult")
    # os.system("squishrunner --testsuite C:/Users/ws/suite_WY_Filmorascrn_Win --reportgen html,D:/Squish/TestResult")
    #os.system("squishrunner --testsuite D:/Squish/TestSuites/suite_ZXY_FilmoraScrn_Win --reportgen html,D:/Squish/TestResult")

    # os.remove(screenpath + "/FSEditor.exe")
    # if os.path.exists(screenpath + "/FSEditor_.exe"):
    #     os.rename(screenpath + "/FSEditor_.exe", screenpath + "/FSEditor.exe")



