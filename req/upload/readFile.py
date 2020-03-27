#!/usr/bin/python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         tt
# Description:  
# Author:       wanghao
# Date:         2018/11/23
#-------------------------------------------------------------------------------


def delblankline(infile, outfile):
    """
    删除空行，匹配特定行，拷贝到新xml文件
    :param infile:
    :param outfile:
    """
    infopen = open(infile, 'r')
    outfopen = open(outfile, 'w')
    try:
        lines = infopen.readlines()
        for line in lines:
            print line
            print line.index("1")
            if line.find("GUID") > 0 or line.find("xml") > 0 or line.find("Filter") > 0:
                # if line.split():
                # 去掉包含kVideoFilter_Param_0的这行
                # if line.find("kVideoFilter_Param_0")<0:
                outfopen.writelines(line.lstrip())
            else:
                outfopen.writelines(line)
    finally:
        infopen.close()
        outfopen.close()

delblankline(r"C:\Users\ws\Desktop\11.sql",r"C:\Users\ws\Desktop\22.sql")