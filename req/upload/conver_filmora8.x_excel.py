#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:wanghao
# datetime:2018/11/27 19:29

import os
from req.utils.ExcelUtil import MyExcelUtil


def replace_space(data):
    symbol = (" - ", " -", "- ", " & ", " ", "-")
    for i in symbol:
        data = data.replace(i, "_")
    return data


def replace_line(data):
    symbol = ("_")
    for i in symbol:
        data = data.replace(i, " ")
    return data


def list_dir(filepath):
    dir = []
    files = os.listdir(filepath)
    # print(files)
    for f in files:
        path = os.path.join(filepath, f)
        if os.path.isdir(path):
            # print(path)
            dir.append(path)
    return dir


def write_exl(i, num, *data):
    exlPath = r"C:\Users\ws\Desktop\filmora8.x_pack\pack.xls"
    MyExcelUtil(exlPath).write_rowNum_data(i, 2,
                                           MyExcelUtil.set_style(0),
                                           int(num), *data)


if __name__ == '__main__':
    exlPath = r"C:\Users\ws\Desktop\filmora8.x_pack\pack.xls"
    path = r"C:\Users\ws\Desktop\filmora8.x_pack"

    # 前置把excel为空行
    m = MyExcelUtil(exlPath)
    for j in range(0, 6):
        print m.get_row_num(j)
        if m.get_row_num(j) > 1:
            for i in range(1, m.get_row_num(j)):
                write_exl(i, j, "", "", "", "", "")

    # 循环遍历目录获取资源名称
    dir_list = list_dir(path)
    print dir_list
    i, j, k, l = 1, 1, 1, 1
    for dir_child in dir_list:
        dir_child_list = os.listdir(dir_child)
        # print dir_child_list
        for dir_child_zipName in dir_child_list:
            d_type = dir_child_zipName.split("#")[0]
            d_pack = dir_child_zipName.split("#")[1]
            d_name = dir_child_zipName.split("#")[2]
            d_sign = replace_space(d_name)
            if str(d_type) == "1":
                print d_type, d_pack, d_name, d_sign
                write_exl(i, 4, d_name, d_sign, d_pack, "", d_name)
                i = i + 1

            if str(d_type) == "2":
                print d_type, d_pack, d_name, d_sign
                write_exl(j, 5, d_name, d_sign, d_pack, "", d_name)
                j = j + 1

            if str(d_type) == "4":
                print d_type, d_pack, d_name, d_sign
                write_exl(k, 3, d_name, d_sign, d_pack, "", d_name)
                k = k + 1

            if str(d_type) == "5":
                print d_type, d_pack, d_name, d_sign
                write_exl(l, 1, d_name, d_sign, d_pack, "", d_name)
                l = l + 1
