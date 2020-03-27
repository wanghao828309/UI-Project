#!C:/Python27
# coding=utf-8
import argparse
import os, rarfile, shutil, time
import ftplib
import pymysql.cursors
import zipfile


def copy(sourceSrcfile, dstDir):
    """
    复制文件到目录
    :param sourceSrcfile:
    :param dstDir:
    """
    if not os.path.exists(dstDir):
        print dstDir + " is not  exist"
    if not os.path.exists(sourceSrcfile):
        return sourceSrcfile + " is not exist"
    shutil.copy(sourceSrcfile, dstDir)


def copyfile(sourceSrcfile, dstSrcfile):
    """
    复制文件
    :param sourceSrcfile:
    :param dstSrcfile:
    """
    if os.path.exists(dstSrcfile):
        print dstSrcfile + " is exist"
        os.remove(dstSrcfile)
    if not os.path.exists(sourceSrcfile):
        return sourceSrcfile + " is not exist"
    shutil.copyfile(sourceSrcfile, dstSrcfile)


def copyDir(sourceSrcDir, dstSrcDir):
    """
    复制文件夹
    :param sourceSrcDir:
    :param dstSrcDir:
    """
    if not os.path.isdir(dstSrcDir):
        os.makedirs(dstSrcDir)
    child = os.listdir(sourceSrcDir)
    for c_child in child:
        c_sourceSrcDir = os.path.join(sourceSrcDir, c_child)
        c_dstSrcDir = os.path.join(dstSrcDir, c_child)
        # c_sourceSrcDir = sourceSrcDir + "\\" + c_child
        # c_dstSrcDir = dstSrcDir + "\\" + c_child
        if os.path.isdir(c_sourceSrcDir):
            # print c_sourceSrcDir
            if os.path.exists(c_dstSrcDir):
                print dstSrcDir, '目录存在先删除'
                shutil.rmtree(c_dstSrcDir)
            shutil.copytree(c_sourceSrcDir, c_dstSrcDir)
        else:
            if os.path.exists(c_dstSrcDir):
                print dstSrcDir + " 目录已经存在文件：" + c_child
                os.remove(c_dstSrcDir)
            shutil.copyfile(c_sourceSrcDir, c_dstSrcDir)


def mkdir(dirPath):
    if os.path.isdir(dirPath):
        shutil.rmtree(dirPath)
        time.sleep(1)
    os.makedirs(dirPath)


def get_args():
    '''
    解析命令行参数
    :return: 命令行参数命名空间
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store', dest='type_id', type=str, help='Type ID')
    parser.add_argument('-p', action='store', dest='dst_path', type=str, help='Dst Path')
    rst = parser.parse_args()
    return rst


class MysqldbHelper(object):
    """
                            操作mysql数据库，基本方法
    """

    def __init__(self, host="localhost", user="root", password="root", port=3306, db="test", charset='utf8mb4',
                 cursorclass=pymysql.cursors.DictCursor):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.charset = charset
        self.cursorclass = cursorclass
        self.con = None
        self.cur = None
        # self.con = pymysql.connect(host=self.host, user=self.user, passwd=self.password, port=self.port, db=self.db,
        #                            charset=charset, cursorclass=cursorclass)
        try:
            self.con = pymysql.connect(host=self.host, user=self.user, passwd=self.password, port=self.port, db=self.db,
                                       charset=charset, cursorclass=cursorclass)
            # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
            self.cur = self.con.cursor()
        except:
            raise Exception("DataBase doesn't connect,close connectiong error;please check the db config.")

    def reConnect(self):
        try:
            self.con.ping()
        except:
            print "重新连接"
            self.con

    def close(self):
        """关闭数据库连接

        """
        if self.con:
            self.cur.close()
            self.con.close()

    def executeSqlOne(self, sql=''):
        """执行sql语句，针对读操作返回结果集

            args：
                sql  ：sql语句
        """
        try:
            self.cur.execute(sql)
            records = self.cur.fetchone()
            return records
        except pymysql.Error, e:
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print error

    def executeCommentSql(self, sql=''):
        """执行sql语句，针对读操作返回结果集

            args：
                sql  ：sql语句
        """
        try:
            self.cur.execute(sql)
            self.cur.fetchone()
            self.con.commit()
        except pymysql.Error, e:
            self.con.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print error
        finally:
            self.cur.close()
            self.con.close()


class myFtp:
    ftp = ftplib.FTP()
    bIsDir = []
    path = ""

    def __init__(self, host, port='21'):
        # self.ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
        # self.ftp.set_pasv(0)      #0主动模式 1 #被动模式
        self.args = get_args()
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

    def DownLoadFileTree(self, LocalDir, RemoteDir):  # 下载整个目录下的文件
        # print "remoteDir:", RemoteDir
        if os.path.isdir(LocalDir) == False:
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        # print "RemoteNames", RemoteNames
        for i, file in enumerate(RemoteNames):
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
        self.bIsDir = []
        # self.path = path
        # this ues callback function ,that will change bIsDir value
        # print self.ftp.nlst()
        self.ftp.retrlines('LIST', self.show)
        return self.bIsDir

    def close(self):
        self.ftp.quit()

    def ftp_copyDown_file(self, cwdPath, type, LocalDir):
        """
        拷贝文件到本地
        :param cwdPath:
        :param type:
        :param LocalDir:
        :param RemoteDir:
        """
        self.ftp.cwd(cwdPath)
        fileName = self.ftp.nlst()[-1]
        print "\n-----------------------RemoteDir:" + fileName + "-----------------------\n"
        # # 在数据库查询是否有记录
        mydb = MysqldbHelper(host='192.168.11.83', port=3306, user='root', password='root', db='AutoTest')
        # sql = 'SELECT COUNT(*) FROM `Artifacts10_01` WHERE fileName = "{}"'.format(fileName)
        # r = mydb.executeSqlOne(sql)
        # print r
        # # 记录不存在是执行拷贝
        # if r["COUNT(*)"] == 0:
        if type == "Git-MultimediaPlatformNLE":
            Multimedia_path = os.path.join(LocalDir, "Multimedia")
            disPath = os.path.join(LocalDir, "All")
            RemoteDir = cwdPath + "/" + fileName + "/Release"
            print "\n----------------------------download ftpDir is:" + RemoteDir + "----------------------------\n"
            ftp.DownLoadFileTree(Multimedia_path, RemoteDir)
            mkdir(disPath)
            copyDir(Multimedia_path, disPath)
        elif type == "Git-NLEPlatformPro":
            # NLE_path = LocalDir + "\NLEPlatformPro"
            NLE_path = os.path.join(LocalDir, "NLEPlatformPro")
            mkdir(NLE_path)
            RemoteDir = cwdPath + "/" + fileName
            print "\n----------------------------download ftpDir is:" + RemoteDir + "----------------------------\n"
            ftp.DownLoadFileTree(NLE_path, RemoteDir)
            z = zipfile.ZipFile(os.path.join(NLE_path, "x64_Release.zip"), 'r')
            z.extractall(path=NLE_path)
            z.close()
            # print NLE_path+r"\x64_Release\Bin\Win\x64_Release"
            copyDir(os.path.join(NLE_path, "x64_Release", "Bin", "Mac", "Release"), os.path.join(LocalDir, "All"))
        elif type == "Git-CodecTest":
            CodecTest_path = os.path.join(LocalDir, "CodecTest")
            # CodecTest_path = LocalDir + "\CodecTest"
            print CodecTest_path
            mkdir(CodecTest_path)
            RemoteDir = cwdPath + "/" + fileName + "/bin"
            print "\n----------------------------download ftpDir is:" + RemoteDir + "----------------------------\n"
            ftp.DownLoadFileTree(CodecTest_path, RemoteDir)
            myzip = zipfile.ZipFile(os.path.join(CodecTest_path, "CodecTest-Win.zip"))
            mystr = myzip.filename.split(".")
            myzip.extractall(mystr[0])
            # un_rar(CodecTest_path + r"\CodecTest-Win.zip", CodecTest_path)
            copy(CodecTest_path + r"/CodecTest-Win/CodecTest.exe", os.path.join(LocalDir, "All"))
        elif type == "Git-NLEProTestTool":
            NLEProTestTool_path = os.path.join(LocalDir, "NLEProTestTool")
            # NLEProTestTool_path = LocalDir + "\NLEProTestTool"
            mkdir(NLEProTestTool_path)
            RemoteDir = cwdPath + "/" + fileName + "/Release"
            print "\n----------------------------download ftpDir is:" + RemoteDir + "----------------------------\n"
            ftp.DownLoadFileTree(NLEProTestTool_path, RemoteDir)
            copyDir(NLEProTestTool_path, os.path.join(LocalDir, "All"))
        # sql2 = 'INSERT INTO Artifacts10_01(type,fileName) VALUES("{}","{}")'.format(type, fileName)
        # mydb.executeCommentSql(sql2)


if __name__ == "__main__":
    ftp = myFtp('ftp.wspublic.cn')
    ftp.Login('public', 'wonder123')
    dst_path = ftp.args.dst_path
    type_id = ftp.args.type_id
    if type_id == "1":
        # 复制Git-MultimediaPlatformNLE文件
        ftp.ftp_copyDown_file("/Artifacts204/Git-MultimediaPlatformNLE/FULLGPU_FOR_OPENCL",
                              "Git-MultimediaPlatformNLE",
                              dst_path)
    elif type_id == "2":
        # 复制Git-NLEPlatformPro文件
        ftp.ftp_copyDown_file("/dbmac08-Artifacts39/Git-NLEPlatformProforMac/release",
                              "Git-NLEPlatformPro",
                              dst_path)
    elif type_id == "3":
        ftp.ftp_copyDown_file("/Artifacts10-01/CodecTest/full_gpu",
                              "Git-CodecTest",
                              dst_path)
    elif type_id == "4":
        ftp.ftp_copyDown_file("/Artifacts10-01/NLEProTestTool/develop",
                              "Git-NLEProTestTool",
                              dst_path)
    elif type_id == "5":
        # 复制exe文件
        print dst_path + "======================================"
        exePath = os.path.join(dst_path, "exe", "msvcr120.dll")
        dst_exePath = os.path.join(dst_path, "All", "msvcr120.dll")
        # exePath = dst_path + r"\exe\msvcr120.dll"
        # dst_exePath = dst_path + "\All\msvcr120.dll"
        copyfile(exePath, dst_exePath)
        exePath = os.path.join(dst_path, "exe", "vcomp120.dll")
        dst_exePath = os.path.join(dst_path, "All", "vcomp120.dll")
        # exePath = dst_path + r"\\exe\\vcomp120.dll"
        # dst_exePath = dst_path + "\\All\\vcomp120.dll"
        copyfile(exePath, dst_exePath)

        # exePath = dst_path + r"\\exe\\DecoderMgr.dll"
        # dst_exePath = dst_path + "\\All\\DecoderMgr.dll"
        # copyfile(exePath, dst_exePath)
        # exePath = dst_path + r"\\exe\\DemuxMgr.dll"
        # dst_exePath = dst_path + "\\All\\DemuxMgr.dll"
        # copyfile(exePath, dst_exePath)
        # exePath = dst_path + r"\\exe\\WS_DecMgr.dll"
        # dst_exePath = dst_path + "\\All\\WS_DecMgr.dll"
        # copyfile(exePath, dst_exePath)
    ftp.close()
