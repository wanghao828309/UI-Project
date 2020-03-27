#!C:/Python27
# coding=utf-8

from ctypes import *
import os,rarfile,shutil
import sys
import ftplib


def un_rar(rar_name,path):
    """unrar zip file"""
    if os.path.exists(rar_name):
        rar = rarfile.RarFile(rar_name)
        if os.path.isdir(path):
            pass
        else:
            os.mkdir(path)
        rar.extractall(path)
        rar.close()
    else:
        print "文件不存在："+rar_name

def copyDir(sourceSrcDir,dstSrcDir):
    child = os.listdir(sourceSrcDir)
    for c_child in child:
        c_sourceSrcDir = sourceSrcDir+"\\"+c_child
        c_dstSrcDir = dstSrcDir + "\\" + c_child
        if os.path.isdir(c_sourceSrcDir):
            # print c_sourceSrcDir
            if os.path.exists(c_dstSrcDir):
                print dstSrcDir, '目录存在先删除'
                shutil.rmtree(c_dstSrcDir)
            shutil.copytree(c_sourceSrcDir, c_dstSrcDir)
        else:
            if os.path.exists(c_dstSrcDir):
                print dstSrcDir+" 目录已经存在文件："+c_child
                os.remove(c_dstSrcDir)
            shutil.copyfile(c_sourceSrcDir,c_dstSrcDir)


class myFtp:
    ftp = ftplib.FTP()
    bIsDir = []
    path = ""

    def __init__(self, host, port='21'):
        # self.ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
        # self.ftp.set_pasv(0)      #0主动模式 1 #被动模式
        self.ftp.connect(host, port)

    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        print self.ftp.welcome

    def DownLoadFile(self, LocalFile, RemoteFile):  # 下载当个文件
        file_handler = open(LocalFile, 'wb')
        # print file_handler
        self.ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write)  # 接收服务器上文件并写入本地文件
        file_handler.close()
        return True

    def UpLoadFile(self, LocalFile, RemoteFile):
        if os.path.isfile(LocalFile) == False:
            return False
        file_handler = open(LocalFile, "rb")
        self.ftp.storbinary('STOR %s' % RemoteFile, file_handler, 4096)  # 上传文件
        file_handler.close()
        return True

    def UpLoadFileTree(self, LocalDir, RemoteDir):
        if os.path.isdir(LocalDir) == False:
            return False
        print "LocalDir:", LocalDir
        LocalNames = os.listdir(LocalDir)
        print "list:", LocalNames
        print RemoteDir
        self.ftp.cwd(RemoteDir)
        for Local in LocalNames:
            src = os.path.join(LocalDir, Local)
            if os.path.isdir(src):
                self.UpLoadFileTree(src, Local)
            else:
                self.UpLoadFile(src, Local)

        self.ftp.cwd("..")
        return

    def DownLoadFileTree(self, LocalDir, RemoteDir):  # 下载整个目录下的文件
        print "remoteDir:", RemoteDir
        if os.path.isdir(LocalDir) == False:
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        print "RemoteNames", RemoteNames
        for i,file in enumerate(RemoteNames):
            # print i,file
            Local = os.path.join(LocalDir, file)
            print Local
            if self.isDir()[i]:
                print self.isDir()[i]
                self.DownLoadFileTree(Local, file)
            else:
                print self.isDir()[i]
                self.DownLoadFile(Local, file)
        self.ftp.cwd("..")
        return

    def show(self, list):
        result = list.lower().split(" ")
        # print result
        # print result[0]
        if self.path in result and "d" in result[0]:
            # print "aaa"
            self.bIsDir.append(True)
        else:
            self.bIsDir.append(False)

    def isDir(self):
        self.bIsDir=[]
        # self.path = path
        # this ues callback function ,that will change bIsDir value
        # print self.ftp.nlst()
        self.ftp.retrlines('LIST', self.show)
        return self.bIsDir


    def close(self):
        self.ftp.quit()


if __name__ == "__main__":

    ftp = myFtp('ftp.wspublic.cn')
    ftp.Login('public', 'wonder123')
    ftp.ftp.cwd("/Artifacts10-01/Git-MultimediaPlatformNLE/FULLGPU_FOR_OPENCL/x64")
    print ftp.ftp.nlst()
    # print ftp.isDir()
    # ftp.DownLoadFileTree( r"C:\Users\ws\Desktop\Release","/Artifacts10-01/Git-MultimediaPlatformNLE/FULLGPU_FOR_OPENCL/x64/2018-12-21_19-37-55_626/Bin/x64/Release")
    # ftp.DownLoadFileTree(r"C:\Users\ws\Desktop\Release2",
    #                      "/Artifacts10-01/Git-NLEPlatformPro/release/2018-12-24_14-29-56_868")

    # un_rar(r"C:\Users\ws\Desktop\Release2\x64_Release.rar","C:\Users\ws\Desktop\Release2")
    # copyDir(r"C:\Users\ws\Desktop\Release2\x64_Release\Bin\Win\x64_Release","C:\Users\ws\Desktop\Release")
