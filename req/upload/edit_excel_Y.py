#!/usr/bin/python
# -*- coding: utf-8 -*-#

# -------------------------------------------------------------------------------
# Name:         edit_excel
# Description:  在filepath目录下存在的文件，在exlPath里的执行状态改为y
# Author:       wanghao
# Date:         2018/11/7
# -------------------------------------------------------------------------------
import zipfile, os, json
from req.utils.ExcelUtil import MyExcelUtil

# filepath:修改文件的目录
filepath = r"C:\Users\ws\Desktop\Resource Packs\Title"
# exlPath:excel文件的目录
exlPath = r"E:\work\python\UI-Project\req\upload\file\Filmora_store.xls"


def edit(n):
    """
    修改文件，同步修改excel状态，清空文件夹
    :param filepath:修改文件的目录
    :param exlPath:excel文件的目录
    :param n:excel修改的sheet页
    """
    files = os.listdir(filepath)
    m = MyExcelUtil(exlPath)
    print files
    j = 0
    for f in files:
        for i in range(1, m.get_row_num(n)):
            # 匹配对应资源包名称
            d = m.get_rowCol_data(i, 2, n)
            if f == d:
                j = j + 1
                print d, j
                MyExcelUtil(exlPath).write_rowNum_data(i, 8,
                                                       MyExcelUtil.set_style(2),
                                                       n, "Y", "")
                # 删除资源包里的文件以及.zip文件
                # path = "E:\Filmore\package\Resource Packs\Title" + "\\" + f
                # for root, dirs, files in os.walk(path, topdown=False):
                #     # print root, dirs, files
                #     for name in files:
                #         os.remove(os.path.join(root, name))
                #     for name in dirs:
                #         os.rmdir(os.path.join(root, name))
                #     zip = root + ".zip"
                #     # print zip
                #     if os.path.exists(zip):
                #         os.remove(zip)


if __name__ == '__main__':
    edit(4)
