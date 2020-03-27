#!C:/Python27
# coding=utf-8
import argparse
import os, rarfile, shutil, time
import ftplib
import pymysql.cursors


def un_rar(rar_name, path):
    """unrar zip file"""
    if os.path.exists(rar_name):
        rar = rarfile.RarFile(rar_name)
        if os.path.isdir(path):
            pass
        else:
            os.makedirs(path)
        rar.extractall(path)
        rar.close()
    else:
        print "文件不存在：" + rar_name


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
        c_sourceSrcDir = sourceSrcDir + "\\" + c_child
        c_dstSrcDir = dstSrcDir + "\\" + c_child
        if os.path.isdir(c_sourceSrcDir) and os.path.exists(c_dstSrcDir):
            # print c_sourceSrcDir
            if os.path.exists(c_dstSrcDir):
                print dstSrcDir, '目录存在先删除'
                shutil.rmtree(c_dstSrcDir)
            shutil.copytree(c_sourceSrcDir, c_dstSrcDir)
        else:
            if os.path.exists(c_dstSrcDir):
                print dstSrcDir + " 目录已经存在文件：" + c_child
                pass
            else:
                shutil.copyfile(c_sourceSrcDir, c_dstSrcDir)


def mkdir(dirPath):
    if os.path.isdir(dirPath):
        shutil.rmtree(dirPath)
        time.sleep(1)
    os.makedirs(dirPath)


import fnmatch


def ignore_patterns(*names):
    return set(names)


def copyDir2(src, dst, *ignoreName):
    """
    递归复制文件夹(去除重复名称)
    :param sourceSrcDir:
    :param dstSrcDir:
    """
    if not os.path.isdir(src):
        return "{} 文件夹不存在".format(src)
    if not os.path.isdir(dst):
        shutil.copytree(src, dst)
    else:
        child = os.listdir(src)

        ignored_names = set(ignoreName)
        for c_child in child:
            if c_child in ignored_names:
                print "ignore dir：{}".format(c_child)
                continue
            c_src = os.path.join(src, c_child)
            c_dst = os.path.join(dst, c_child)
            # print c_src, c_dst
            if os.path.isdir(c_src):
                copyDir2(c_src, c_dst, ignoreName)
                pass
            else:
                if os.path.exists(c_dst):
                    print dst + " 目录已经存在文件：" + c_child
                else:
                    shutil.copyfile(c_src, c_dst)


if __name__ == "__main__":
    # 从共享网盘copy STL文件夹
    c_STL = r"\\192.168.10.177\Test resource new\Device\STL"
    # d_STL = r"D:\STL"
    # copyDir2(c_STL, d_STL, "压缩测试工程")
    child = os.listdir(c_STL)
    for c_child in child:
        print c_child
    # res = ignore_patterns("1")
    # print res

    pass
