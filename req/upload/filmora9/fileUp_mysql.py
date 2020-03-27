#!/usr/bin/python
# -*- coding: UTF-8 -*-

import zipfile, os
from req.utils.ExcelUtil import MyExcelUtil
from req.upload.filmora9 import reqApi
from req.utils.mysqldbUtil import MysqldbHelper

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

# now = lambda time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))

def replace_space(data):
    symbol = (" - ", " -", "- ", " & ", " ", "-")
    for i in symbol:
        data = data.replace(i, "_")
    return data


def zip_ya(startdir, file_news):
    # startdir  #要压缩的文件夹路径
    # file_news = startdir +'.zip' # 压缩后文件夹的名字
    if os.path.exists(file_news):
        return 0
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir, '')  # 这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()


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


def replace_space2(data):
    firstData = data.replace(" - ", "_")
    firstData = firstData.replace(" & ", "/")
    firstData = firstData.replace(" ", "_")
    firstData = firstData.replace("'", "_")
    return firstData


def find_id(exlPath):
    m = MyExcelUtil(exlPath)
    mydb = MysqldbHelper(host='10.10.19.117', port=3306, user='root', password='root', db='filmora_es_admin')
    for j in range(4, 6):
        name = m.get_sheet_names()
        for i in range(1, m.get_row_num(j)):
            d = m.get_rowCol_data(i, 1, j)
            if name[j] == "MUSIC":
                value = 'sound_' + replace_space2(d).lower()
            elif name[j] == "TEXT":
                value = 'text_' + replace_space2(d).lower()
            elif name[j] == "TRANSITIONS":
                value = 'trans_' + replace_space2(d).lower()
            elif name[j] == "FILTERS":
                value = 'effect_' + replace_space2(d).lower()
            elif name[j] == "OVERLAYS":
                value = 'overlay_' + replace_space2(d).lower()
            elif name[j] == "ELEMENTS":
                value = 'element_' + replace_space2(d).lower()
            elif name[j] == "SPLIT":
                value = 'split_' + replace_space2(d).lower()
            if m.get_rowCol_data(i, 8, j).upper() == "Y":
                print value
                result = mydb.executeSqlOne(
                    'SELECT id,catdir from wx_resource_category where child = 0 and catdir = \"{}\"'.format(value))
                if result is not None:
                    print result["id"]
                    MyExcelUtil(exlPath).write_data(i, 5, result["id"], MyExcelUtil.set_style(8), j)
        #     if m.get_rowCol_data(i, 8, j).upper() == "Y":
        #         val = m.get_rowCol_data(i, 2, j)
        #         print str(i) + ": " + replace_space(val)
        #         MyExcelUtil(exlPath).write_data(i, 3, replace_space(val), MyExcelUtil.set_style(8), j)


def get_condict():
    """
    获取excel前两列数据
    :return: 元组
    """
    exlPath = r"E:\work\python\UI-Project\req\upload\pack_language.xls"
    data = []
    for i in range(1, MyExcelUtil(exlPath).get_row_num()):
        key = MyExcelUtil(exlPath).get_rowCol_data(i, 0)
        val = MyExcelUtil(exlPath).get_rowCol_data(i, 1)
        data.append((key, val))
    dict_data = dict(data)
    return dict_data


def convert_jp(key):
    """
    翻译日语，根据key，返回匹配的val
    :param key:
    :return:
    """
    data = get_condict()
    for i, v in data.items():
        if i == key:
            return v
    return ""


def copy_id(exlPath, exlPath2):
    dict_data = get_condict()
    for j in range(0, 6):
        print MyExcelUtil(exlPath2).get_row_num(j)
        for i in range(1, MyExcelUtil(exlPath2).get_row_num(j)):
            d = MyExcelUtil(exlPath2).get_rowCol_data(i, 10, j)
            print d
            for key, value in dict_data.items():
                if (d == key):
                    MyExcelUtil(exlPath2).write_data(i, 11, value,
                                                     MyExcelUtil.set_style(2),
                                                     j)
                    continue

    # for j in (0, 6):
    #     data = []
    #     data2 = []
    #     data3 = []
    #     row = MyExcelUtil(exlPath).get_row_num(j)
    #     for i in range(1, MyExcelUtil(exlPath).get_row_num(j)):
    #         val = MyExcelUtil(exlPath).get_rowCol_data(i, 1, j)
    #         print val.split(".")[0]
    #         data.append(val.split(".")[0])
    #         data2.append(MyExcelUtil(exlPath).get_rowCol_data(i, 0, j))
    #         data3.append(MyExcelUtil(exlPath).get_rowCol_data(i, 2, j))
    #
    #     for i in range(1, MyExcelUtil(exlPath2).get_row_num(j)):
    #         for d, d2, d3 in zip(data, data2, data3):
    #             fileupData = MyExcelUtil(exlPath2).get_rowCol_data(i, 5, j)
    #             if fileupData.equalsIgnoreCase(d):
    #                 print u"第" + str(i) + u"行: " + fileupData
    #                 MyExcelUtil(exlPath2).write_rowNum_data(i, 2,
    #                                                         MyExcelUtil.set_style(8), j,
    #                                                         d, d2, d3)
    #                 continue


def zip_dir(dir):
    childDir = list_dir(dir)
    print childDir
    for dd in childDir:
        zipDir = dd + '.zip'
        if os.path.exists(zipDir):
            pass
            # print("已经压缩")
        else:
            zip_ya(dd, zipDir)


def up_default_resource(exlPath):
    listDir = list_dir(r"E:\work\Filmora9\package\default")
    i = 1
    for d in listDir:
        zip_dir(d)

    m = MyExcelUtil(exlPath)
    dir = r"E:\work\Filmora9\package\default"
    time = 0
    for j in range(0, 7):
        for i in range(1, m.get_row_num(j)):
            if m.get_rowCol_data(i, 6, j).upper() == "Y":
                zipDir = dir + "\\"+m.get_rowCol_data(i, 2, j) + "\\" + m.get_rowCol_data(i, 4, j) + ".zip"
                # print zipDir
                if os.path.exists(zipDir):
                    print zipDir
                    if m.get_rowCol_data(i, 2, j).lower() == "title":
                        resource_type = 1
                    elif m.get_rowCol_data(i, 2, j).lower() == "transition":
                        resource_type = 2
                    elif m.get_rowCol_data(i, 2, j).lower() == "filter":
                        resource_type = 3
                    elif m.get_rowCol_data(i, 2, j).lower() == "overlay":
                        resource_type = 4
                    elif m.get_rowCol_data(i, 2, j).lower() == "splitscreen":
                        resource_type = 5
                    elif m.get_rowCol_data(i, 2, j).lower() == "audio":
                        resource_type = 6
                    elif m.get_rowCol_data(i, 2, j).lower() == "element":
                        resource_type = 7
                    try:
                        resUrl = reqApi.post_files(zipDir, 2)
                        resText = reqApi.post_ResourceAdd(m.get_rowCol_data(i, 8, j), resUrl,
                                                          m.get_rowCol_data(i, 5, j),
                                                          m.get_rowCol_data(i, 1, j), m.get_rowCol_data(i, 0, j),
                                                          resource_type)
                        if resText.find(u"操作成功") >= 0:
                            time = time + 1
                            print("操作成功 " + str(time))
                            MyExcelUtil(exlPath).write_rowNum_data(i, 6,
                                                                   MyExcelUtil.set_style(3),
                                                                   j, "N", "PASS")
                        else:
                            print("操作失败")
                            MyExcelUtil(exlPath).write_data(i, 7, "FAIL",
                                                            MyExcelUtil.set_style(2),
                                                            j)
                    except Exception as err:
                        print err
                        MyExcelUtil(exlPath).write_data(i, 7, "FAIL",
                                                        MyExcelUtil.set_style(2),
                                                        j)


def edit_default_resource(exlPath):
    dir =r"C:\Users\ws\Desktop\20181208"
    listDir = list_dir(dir)
    i = 1
    for d in listDir:
        zip_dir(d)

    m = MyExcelUtil(exlPath)
    time = 0
    for j in range(0, 7):
        for i in range(1, m.get_row_num(j)):
            if m.get_rowCol_data(i, 6, j).upper() == "Y":
                zipDir = dir +"\\"+ m.get_rowCol_data(i, 2, j) + "\\" + m.get_rowCol_data(i, 4, j) + ".zip"
                # print zipDir
                if os.path.exists(zipDir):
                    print zipDir
                    if m.get_rowCol_data(i, 2, j).lower() == "title":
                        resource_type = 1
                    elif m.get_rowCol_data(i, 2, j).lower() == "transition":
                        resource_type = 2
                    elif m.get_rowCol_data(i, 2, j).lower() == "filter":
                        resource_type = 3
                    elif m.get_rowCol_data(i, 2, j).lower() == "overlay":
                        resource_type = 4
                    elif m.get_rowCol_data(i, 2, j).lower() == "splitscreen":
                        resource_type = 5
                    elif m.get_rowCol_data(i, 2, j).lower() == "audio":
                        resource_type = 6
                    elif m.get_rowCol_data(i, 2, j).lower() == "element":
                        resource_type = 7
                    try:
                        resUrl = reqApi.post_files(zipDir, 2)
                        print resUrl
                        resText = reqApi.post_ResourceEdit(m.get_rowCol_data(i, 8, j), resUrl,
                                                           m.get_rowCol_data(i, 5, j),
                                                           m.get_rowCol_data(i, 1, j), m.get_rowCol_data(i, 0, j),
                                                           resource_type,"default Edit"
                                                           )
                        if resText.find(u"操作成功") >= 0:
                            time = time + 1
                            print("操作成功 " + str(time))
                            MyExcelUtil(exlPath).write_rowNum_data(i, 6,
                                                                   MyExcelUtil.set_style(3),
                                                                   j, "N", "PASS")
                        else:
                            print("操作失败")
                            MyExcelUtil(exlPath).write_data(i, 7, "FAIL",
                                                            MyExcelUtil.set_style(2),
                                                            j)
                    except Exception as err:
                        print err
                        MyExcelUtil(exlPath).write_data(i, 7, "FAIL",
                                                        MyExcelUtil.set_style(2),
                                                        j)


def up_store_resource(exlPath):
    dir = r"C:\Users\ws\Desktop\9.0_pack"
    m = MyExcelUtil(exlPath)
    listDir = list_dir(dir)
    for d in listDir:
        zip_dir(d)


    time = 0
    for j in range(0, 6):
        for i in range(1, m.get_row_num(j)):
            if m.get_rowCol_data(i, 8, j).upper() == "Y":
                zipDir = dir +"\\"+ m.get_rowCol_data(i, 7, j) + "\\" + m.get_rowCol_data(i, 2, j) + ".zip"
                # print zipDir
                if os.path.exists(zipDir):
                    print zipDir
                    # print type(zipDir)
                    if m.get_rowCol_data(i, 7, j).lower() == "title":
                        resource_type = 1
                    elif m.get_rowCol_data(i, 7, j).lower() == "transition":
                        resource_type = 2
                    elif m.get_rowCol_data(i, 7, j).lower() == "filter":
                        resource_type = 3
                    elif m.get_rowCol_data(i, 7, j).lower() == "overlay":
                        resource_type = 4
                    elif m.get_rowCol_data(i, 7, j).lower() == "audio":
                        resource_type = 6
                    elif m.get_rowCol_data(i, 7, j).lower() == "element":
                        resource_type = 7
                    try:
                        resUrl = reqApi.post_files(zipDir, 2)
                        print resUrl
                        resText = reqApi.post_ResourceAdd(m.get_rowCol_data(i, 6, j), resUrl,
                                                          m.get_rowCol_data(i, 3, j),
                                                          m.get_rowCol_data(i, 4, j), m.get_rowCol_data(i, 5, j),
                                                          resource_type,"store auto")
                        if resText.find(u"操作成功") >= 0:
                            time = time + 1
                            print("操作成功 " + str(time))
                            MyExcelUtil(exlPath).write_rowNum_data(i, 8,
                                                                   MyExcelUtil.set_style(3),
                                                                   j, "N", "PASS")
                        elif resText.find(u"唯一标识不能重复") >= 0:
                            print("唯一标识不能重复")
                            MyExcelUtil(exlPath).write_data(i, 9, "FAIL",
                                                            MyExcelUtil.set_style(2),
                                                            j)
                        else:
                            print("操作失败")
                            MyExcelUtil(exlPath).write_data(i, 9, "FAIL",
                                                            MyExcelUtil.set_style(2),
                                                            j)
                    except Exception as err:
                        print err
                        MyExcelUtil(exlPath).write_data(i, 9, "FAIL",
                                                        MyExcelUtil.set_style(2),
                                                        j)


# 编辑商城资源
def edit_store_resource(exlPath,e=1):
    path = r"C:\Users\ws\Desktop\20181208"
    #当e的值不为1时，代表不需要重新上传资源
    m = MyExcelUtil(exlPath)
    listDir = list_dir(path)
    for d in listDir:
        zip_dir(d)

    dir = path+"\\"
    time = 0
    for j in range(0, 6):
        for i in range(1, m.get_row_num(j)):
            if m.get_rowCol_data(i, 8, j).upper() == "Y":
                zipDir = dir + m.get_rowCol_data(i, 7, j) + "\\" + m.get_rowCol_data(i, 2, j) + ".zip"
                print zipDir
                if os.path.exists(zipDir):
                    # print zipDir
                    if m.get_rowCol_data(i, 7, j).lower() == "title":
                        resource_type = 1
                    elif m.get_rowCol_data(i, 7, j).lower() == "transition":
                        resource_type = 2
                    elif m.get_rowCol_data(i, 7, j).lower() == "filter":
                        resource_type = 3
                    elif m.get_rowCol_data(i, 7, j).lower() == "overlay":
                        resource_type = 4
                    elif m.get_rowCol_data(i, 7, j).lower() == "audio":
                        resource_type = 6
                    elif m.get_rowCol_data(i, 7, j).lower() == "element":
                        resource_type = 7
                    try:
                        if e==1:
                            resUrl = reqApi.post_files(zipDir, 2)
                            print resUrl
                        else:
                            resUrl = ""
                            print "资源不用上传"
                        resText = reqApi.post_ResourceEdit(m.get_rowCol_data(i, 6, j), resUrl,
                                                           m.get_rowCol_data(i, 3, j),
                                                           m.get_rowCol_data(i, 4, j), m.get_rowCol_data(i, 5, j),
                                                           resource_type,"store Edit")
                        if resText.find(u"操作成功") >= 0:
                            time = time + 1
                            print("操作成功 " + str(time))
                            MyExcelUtil(exlPath).write_rowNum_data(i, 8,
                                                                   MyExcelUtil.set_style(3),
                                                                   j, "N", "PASS")
                        else:
                            print("操作失败")
                            MyExcelUtil(exlPath).write_data(i, 9, "FAIL",
                                                            MyExcelUtil.set_style(2),
                                                            j)
                    except Exception as err:
                        print err
                        MyExcelUtil(exlPath).write_data(i, 9, "FAIL",
                                                        MyExcelUtil.set_style(2),
                                                        j)


def up_pack9_default():

        mydb = MysqldbHelper(host='10.10.19.117', port=3306, user='root', password='root', db='filmora_es_admin')
        resource_dict = mydb.executeSql('SELECT slug from wx_pack_9_resource where description IN (\"wang auto\" ,\"default Edit\") and resource_status = 3 and slug !=\"Shadow1\"')
        resource_name = []
        for name in resource_dict:
            # print name["slug"]
            resource_name.append(name["slug"])
        resource_name = list(set(resource_name))
        # print resource_name
        try:
            print "内置资源个数："+str(len(resource_name))
            resText = reqApi.post_Pack9Add("DefaultPackage", "", "DefaultPackage", resource_name)
            if resText.find(u"操作成功") >= 0:
                print("操作成功 " )
        except Exception as err:
            print err
            print("操作失败")


def up_pack9(exlPath):
    m = MyExcelUtil(exlPath)
    pack_name = []
    for j in range(0, 6):
        for i in range(1, m.get_row_num(j)):
            # print m.get_rowCol_data(i, 6, j)
            if m.get_rowCol_data(i, 5, j).upper() == "Y":
                data = m.get_rowCol_data(i, 4, j)
                pack_name.append(data)
                pack_name = list(set(pack_name))
    print pack_name
    time = 0
    for name in pack_name:
        resource_name = []
        for j in range(0, 6):
            for i in range(1, m.get_row_num(j)):
                if m.get_rowCol_data(i, 5, j).upper() == "Y" and m.get_rowCol_data(i, 4, j) == name:
                    resource_name.append(m.get_rowCol_data(i, 3, j))
                    MyExcelUtil(exlPath).write_rowNum_data(i, 5,
                                                           MyExcelUtil.set_style(3),
                                                           j, "N", "PASS")
        # print resource_name
        # jp = convert_jp(name)
        jp=""
        print(name, "", replace_space(name), resource_name)
        try:
            if len(resource_name)>0:
                resText = reqApi.post_Pack9Add(name, jp, replace_space(name), resource_name)
            if resText.find(u"操作成功") >= 0:
                time = time + 1
                print("操作成功 " + str(time))
        except Exception as err:
            print err
            print("操作失败")


def up_set9(exlPath):
    m = MyExcelUtil(exlPath)
    set_dict = {}
    set_dict2 = {}
    for i in range(1, m.get_row_num(6)):
        if m.get_rowCol_data(i, 2, 6).upper() == "Y":
            setName = m.get_rowCol_data(i, 1, 6)
            packName = m.get_rowCol_data(i, 0, 6)
            set_dict[packName] = setName
            set_dict2.update({setName: []})
    # print set_dict2

    for k,v in set_dict.items():
        if set_dict2.has_key(v):
            set_dict2[v].append(k)
        else:
            set_dict2[v] = []
    # print set_dict2
    time = 0
    for s,p in set_dict2.items():
        print p
        resource_name = []
        for j in range(0, 6):
            for i in range(1, m.get_row_num(j)):
                if m.get_rowCol_data(i, 4, j) in p:
                    resource_name.append(m.get_rowCol_data(i, 3, j))
                    MyExcelUtil(exlPath).write_data(i, 5, "PASS",
                                                    MyExcelUtil.set_style(3),
                                                    j)
        # print resource_name
        print(s, "", replace_space(s), resource_name)
        try:
            if len(resource_name)>0:
                resText = reqApi.post_Pack9Add(s, "", replace_space(s), resource_name)
            if resText.find(u"操作成功") >= 0:
                time = time + 1
                print("操作成功 " + str(time))
        except Exception as err:
            print err



def sql_filmora9(exlPath):

    # mydb = MysqldbHelper(host='10.10.19.117', port=3306, user='root', password='root', db='filmora_es_admin')
    # mydb = MysqldbHelper(host='10.10.18.252', port=33064, user='f_common', password='f_common@cloud', db='f_common')
    mydb = MysqldbHelper(host='192.168.11.82', port=3307, user='vp_filmora_read', password='ERatt##89235',
                         db='filmora_es_admin')
    m = MyExcelUtil(exlPath)
    pack_name = []
    for j in range(0, 6):
        for i in range(1, m.get_row_num(j)):
            # print m.get_rowCol_data(i, 6, j)
            if m.get_rowCol_data(i, 5, j).upper() == "Y":
                data = m.get_rowCol_data(i, 4, j)
                pack_name.append(data)
                pack_name = list(set(pack_name))
    # print pack_name
    for name in pack_name:
        sql = 'SELECT pack9_id,pack9_slug,pack9_url from wx_pack WHERE title="{}"  and siteid =1'.format(name)
        r = mydb.executeSqlOne(sql)
        # print r
        # sql_siteid = 'SELECT siteid from wx_pack WHERE title="{}"'.format(name)
        # print sql_siteid
        # result_siteid = mydb.executeSqlOne(sql_siteid)
        # print result_siteid
        if r is not None and len(r["pack9_url"])>1:
            # print r["pack9_url"]
            for i in range(2,21):
                sql3 = 'SELECT pack9_id,pack9_slug,pack9_url from wx_pack WHERE title="{}"  and siteid ={}'.format(name,i)
                result3 = mydb.executeSqlOne(sql3)
                if result3 is not None:
                    sql2 = 'UPDATE  wx_pack SET pack9_id = {},pack9_slug="{}",pack9_url="{}" WHERE title="{}" and siteid ={};'.format(
                        r["pack9_id"], r["pack9_slug"], r["pack9_url"],name,i)
                    print sql2
                    mydb2 = MysqldbHelper(host='192.168.11.82', port=3307, user='vp_filmora_read',
                                         password='ERatt##89235',
                                         db='filmora_es_admin')
                    # mydb2 = MysqldbHelper(host='10.10.19.117', port=3306, user='root', password='root',
                    #                      db='filmora_es_admin')
                    # mydb2 = MysqldbHelper(host='10.10.18.252', port=33064, user='f_common', password='f_common@cloud',
                    #                      db='f_common')
                    # mydb2.executeCommentSql(sql2)


if __name__ == "__main__":
    pass

    # zip_dir(r"E:\work\Filmora9\package\default\Transition")

    # find_id(r"C:\Users\ws\Desktop\Filmora_store_new.xls")
    # 上传内置资源
    # up_default_resource(r"E:\work\python\UI-Project\req\upload\Filmora_default.xls")
    # 编辑内置资源
    # edit_default_resource(r"E:\work\python\UI-Project\req\upload\file\Filmora_default.xls")
    # time.sleep(10)
    # 打包内置资源pack
    # up_pack9_default()


    # 上传商城资源
    # up_store_resource(r"E:\work\python\UI-Project\req\upload\file\Filmora_store_new.xls")
    # 编辑商城资源
    edit_store_resource(r"E:\work\python\UI-Project\req\upload\file\Filmora_store.xls",0)
    # 打包商城资源pack
    # up_pack9(r"C:\Users\ws\Desktop\pack9_new2.xls")
    # 打包商城资源set
    # up_set9(r"E:\work\python\UI-Project\req\upload\set9_store.xls")

    # sql_filmora9(r"E:\work\python\UI-Project\req\upload\file\pack9_new.xls")

    # l =  list_dir(r"E:\work\Filmora9\package\default\SplitScreen")
    # j = 0
    # for i in l:
    #     j =j +1
    #     print j
    #     MyExcelUtil(r"E:\work\python\UI-Project\req\fileup2.xls").write_data(j,4,i.split("\\")[-1].split(),MyExcelUtil.set_style(8), 6)


