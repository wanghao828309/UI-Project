#coding=utf-8
import threading,time
import zipfile, os
from req.utils.ExcelUtil import MyExcelUtil

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

def up_store_resource(exlPath,j):
    m = MyExcelUtil(exlPath)
    listDir = list_dir(r"E:\work\Filmora9\package\packs")
    n = -1
    for d in listDir:
        i = 1
        n = n + 1
        childDir = list_dir(d)
        for dd in childDir:
            i = i + 1
            zipDir = dd + '.zip'
            if os.path.exists(zipDir):
                pass
            else:
                zip_ya(dd, zipDir)


    dir = r"E:\work\Filmora9\package\packs\\"
    time = 0
    for i in range(1, m.get_row_num(j)):
        if m.get_rowCol_data(i, 8, j).upper() == "Y":
            zipDir = dir + m.get_rowCol_data(i, 7, j) + "\\" + m.get_rowCol_data(i, 6, j) + ".zip"
            # print zipDir
            if os.path.exists(zipDir):
                print zipDir
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

                MyExcelUtil(exlPath).write_rowNum_data(i, 8,
                                                       MyExcelUtil.set_style(3),
                                                       j, "N", "PASS")
                # try:
                #     resUrl = reqApi.post_files(zipDir, 2)
                #     print resUrl
                #     resText = reqApi.post_ResourceAdd(m.get_rowCol_data(i, 6, j), resUrl,
                #                                       m.get_rowCol_data(i, 3, j),
                #                                       m.get_rowCol_data(i, 4, j), m.get_rowCol_data(i, 5, j),
                #                                       resource_type)
                #     if resText.find(u"操作成功") >= 0:
                #         time = time + 1
                #         print("操作成功 " + str(time))
                #         MyExcelUtil(exlPath).write_rowNum_data(i, 8,
                #                                                MyExcelUtil.set_style(3),
                #                                                j, "N", "PASS")
                #     else:
                #         print("操作失败")
                #         MyExcelUtil(exlPath).write_data(i, 9, "FAIL",
                #                                         MyExcelUtil.set_style(2),
                #                                         j)
                # except Exception as err:
                #     print err
                #     MyExcelUtil(exlPath).write_data(i, 9, "FAIL",
                #                                     MyExcelUtil.set_style(2),
                #                                     j)
if __name__ == '__main__':
    threads = []
    for i in range(0,6):
        threads.append(threading.Thread(target=up_store_resource, args=(r"E:\work\python\UI-Project\req\upload\Filmora_store.xls",i)))
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()

    # print "\nall over %s" %ctime()