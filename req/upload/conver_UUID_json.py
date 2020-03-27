#!/usr/bin/python
# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         c_json
# Description:  
# Author:       wanghao
# Date:         2018/10/26
# -------------------------------------------------------------------------------

from req.utils import xmlUtils
import os
import json
from req.utils.ExcelUtil import MyExcelUtil


def list_all_files(rootdir):
    """
     列出文件夹下所有的目录与文件
    :param rootdir: 文件目录
    :return:
    """
    _files = []
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isdir(path):
            _files.extend(list_all_files(path))
        if os.path.isfile(path):
            _files.append(path)
    return _files


def get_dataFile(fileList):
    """
    获取目录下的filter.xml
    :param fileList:
    :return:
    """
    dataFile = []
    i = 0
    for file in fileList:
        if "filter.xml" in file:
            i = i + 1
            dataFile.append(file)
            # print file
    # print i
    return dataFile


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
            # print line.find("GUID")
            if line.find("GUID") > 0 or line.find("xml") > 0 or line.find("Filter") > 0:
                # if line.split():
                # 去掉包含kVideoFilter_Param_0的这行
                # if line.find("kVideoFilter_Param_0")<0:
                outfopen.writelines(line.lstrip())
            else:
                outfopen.writelines("")
    finally:
        infopen.close()
        outfopen.close()


def get_guid(xmlPath):
    # 1. 读取xml文件
    tree = xmlUtils.read_xml(xmlPath)
    # A. 找到节点
    nodes = xmlUtils.find_nodes(tree, ".//Properties/Property")
    print nodes
    # B. 通过属性准确定位子节点
    result_nodes = xmlUtils.get_node_by_keyvalue(nodes, {"key": "z.FilterID"})
    if len(result_nodes) == 0:
        return
    print result_nodes
    GUID = result_nodes[0].get("value")
    if GUID is not None:
        return GUID
    else:
        print "GUID 不存在"


def get_guid2(xmlPath):
    # 1. 读取xml文件
    tree = xmlUtils.read_xml(xmlPath)
    # A. 找到节点
    nodes = xmlUtils.find_nodes(tree, ".//GUID")
    if len(nodes) > 0:
        return nodes[0].text



def get_excelValue(exlPath, val, n):
    """
    获取内置资源名称
    :param exlPath:
    :param val:
    :param n:sheet页
    :return:
    """
    m = MyExcelUtil(exlPath)
    for i in range(1, m.get_row_num(n)):
        d = m.get_rowCol_data(i, 5, n)
        # print d
        if d.lower() == val.lower():
            return m.get_rowCol_data(i, 8, n)

def get_store_excelValue(exlPath, val, n):
    """
    获取商城资源名称
    :param exlPath:
    :param val:
    :param n:sheet页
    :return:
    """
    m = MyExcelUtil(exlPath)
    for i in range(1, m.get_row_num(n)):
        d = m.get_rowCol_data(i, 3, n)
        # print d
        if d.lower() == val.lower():
            return m.get_rowCol_data(i, 6, n)


if __name__ == '__main__':
    DefaultFloder = r"C:\Users\ws\Desktop\store_package"
    copyFloder = []
    dict_trans = {}
    dict_filter= {}
    dict_overlay = {}

    # for xmlFile in copyFloder:
    #     print xmlFile
    #     path = xmlFile.split("_bat")[0]+".xml"
    #     GUID = get_guid(xmlFile)
    #     if GUID is not None:
    #         print GUID,path
    #         dict[GUID] = path
    # print dict
    # with open(r"C:\Users\ws\Desktop\record.json", "w") as f:
    #     json.dump(dict,f)

    # 获取filter.xml，并且复制到当前目录filter_bat.xml
    fileList = list_all_files(DefaultFloder)
    dataFile = get_dataFile(fileList)
    # print dataFile
    for dataXml in dataFile:
        copyPath = dataXml.split(".")[0] + "_bat." + dataXml.split(".")[1]
        delblankline(dataXml, copyPath)
        copyFloder.append(copyPath)


    for xmlFile in copyFloder:
        print xmlFile
        path = xmlFile.split("filter")[0]

        # 获取内置资源名称
        # sign = xmlFile.split("2_")[1].split("\\")[0]
        # print sign
        # name = get_excelValue(r"E:\work\python\UI-Project\req\upload\Filmora_default.xls", sign, 4)

        # 获取商城资源（transition）
        if xmlFile.find("2_")>0:
            sign = xmlFile.split("2_")[1].split("\\")[0]
            # print sign
            name = sign.replace("_", " ")
            # name = get_store_excelValue(r"E:\work\python\UI-Project\req\upload\file\Filmora_store.xls", sign, 5)
            print name
            GUID = get_guid2(xmlFile)
            if GUID is not None:
                print GUID, path
                dict_trans[GUID] = [path, name]

        # 获取商城资源（filter）
        if xmlFile.find("3_")>0:
            sign = xmlFile.split("3_")[1].split("\\")[0]
            # print sign
            name = sign.replace("_", " ")
            # name = get_store_excelValue(r"E:\work\python\UI-Project\req\upload\file\Filmora_store.xls", sign, 5)
            print name
            GUID = get_guid2(xmlFile)
            if GUID is not None:
                print GUID, path
                dict_filter[GUID] = [path, name]

        # 获取商城资源（OVERLAYS）
        if xmlFile.find("4_")>0:
            sign = xmlFile.split("4_")[1].split("\\")[0]
            # print sign
            # name = get_store_excelValue(r"E:\work\python\UI-Project\req\upload\file\Filmora_store.xls", sign, 3)
            name = sign.replace("_", " ")
            print name
            GUID = get_guid2(xmlFile)
            if GUID is not None:
                print GUID, path
                dict_overlay[GUID] = [path, name]

    # print dict_trans
    # with open(r"C:\Users\ws\Desktop\record_overlay.json", "w") as f:
    #     json.dump(dict_trans, f)

    print dict_filter
    with open(r"C:\Users\ws\Desktop\record_filter.json", "w") as f:
        json.dump(dict_filter, f)

    # print dict_overlay
    # with open(r"C:\Users\ws\Desktop\record_transitions.json", "w") as f:
    #     json.dump(dict_overlay, f)

