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
    exlPath = r"C:\Users\ws\Desktop\filmora9.0_pack\pack.xls"
    MyExcelUtil(exlPath).write_rowNum_data(i, 2,
                                           MyExcelUtil.set_style(0),
                                           int(num), *data)


if __name__ == '__main__':
    exlPath = r"C:\Users\ws\Desktop\filmora9.0_pack\pack.xls"
    path = r"C:\Users\ws\Desktop\filmora9.0_pack"

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
        print dir_child_list
        for dir_child_zipName in dir_child_list:
            if "1_" in dir_child_zipName and 'lowerthird' in dir_child_zipName.lower() or 'opener' in dir_child_zipName.lower() or 'title' in dir_child_zipName.lower():
                dir_child_name = dir_child_zipName.split(".")[0]
                sign = dir_child_name.split("1_")[1]
                upload_name = replace_line(sign)
                print dir_child_name, sign, upload_name
                write_exl(i, 4, dir_child_name, sign, "", "", upload_name)
                i = i + 1

            if "2_" in dir_child_zipName and 'transition' in dir_child_zipName.lower():
                dir_child_name = dir_child_zipName.split(".")[0]
                sign = dir_child_name.split("2_")[1]
                upload_name = replace_line(sign)
                print dir_child_name, sign, upload_name
                write_exl(j, 5, dir_child_name, sign, "", "", upload_name)
                j = j + 1

            if "4_" in dir_child_zipName and 'overlay' in dir_child_zipName.lower():
                dir_child_name = dir_child_zipName.split(".")[0]
                sign = dir_child_name.split("4_")[1]
                upload_name = replace_line(sign)
                print dir_child_name, sign, upload_name
                write_exl(k, 3, dir_child_name, sign, "", "", upload_name)
                k = k + 1

            if "7_" in dir_child_zipName and 'element' in dir_child_zipName.lower():
                dir_child_name = dir_child_zipName.split(".")[0]
                sign = dir_child_name.split("7_")[1]
                upload_name = replace_line(sign)
                print dir_child_name, sign, upload_name
                write_exl(l, 1, dir_child_name, sign, "", "", upload_name)
                l = l + 1

            if "3_" in dir_child_zipName:
                dir_child_name = dir_child_zipName
                sign = dir_child_name.split("3_")[1]
                upload_name = replace_line(sign)
                print dir_child_name, sign, upload_name
                write_exl(l, 2, dir_child_name, sign, "", "", upload_name)
                l = l + 1