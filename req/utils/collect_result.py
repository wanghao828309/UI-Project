#!C:/Python27
# coding=utf-8
import argparse
import os, rarfile, shutil, time
import ftplib
import pymysql.cursors





def copyfile(sourceSrcfile, dstSrcfile):
    """
    复制文件
    :param sourceSrcfile:
    :param dstSrcfile:
    """
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
        c_sourceSrcDir = sourceSrcDir + "\\" + c_child
        c_dstSrcDir = dstSrcDir + "\\" + c_child
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

def get_last_dir(dirPath):
    dirs = os.listdir(dirPath)
    dirs.sort()
    return dirPath+"\\"+dirs[-1]

def get_last_file(dirPath):
    file = os.listdir(dirPath)
    return file[0]


def get_args():
    '''
    解析命令行参数
    :return: 命令行参数命名空间
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose','-p', action='store', dest='dst_path', type=str, help='Dst Path')
    rst = parser.parse_args()
    return rst





if __name__ == "__main__":
    # os.listdir("C:\Users\ws\Desktop\\tt")
    arg = get_args()
    dst_path = arg.dst_path+"\\Report"
    s_path = arg.dst_path + "\\result"
    result_dir = get_last_dir(dst_path)
    result_html = get_last_file(result_dir)
    mkdir(s_path)
    # print result_dir+"\\"+result_html,s_path+"\\"+result_html
    copyfile(result_dir+"\\"+result_html,s_path+"\\index.html")

