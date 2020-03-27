#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:wanghao
# datetime:2019/3/19 14:35
import requests
import time
from req.utils.sqldb import Database

WONDERSHARE_HOST = "app.bugsplat.com"
DATABASE = "Wondershare_filmora_9_0_win"
COOKIES = "_ga=GA1.2.208329902.1554369815; BsPageSize=25; __hstc=18090534.7311c009f14bdfbadf0ddc9d32a31bbb.1554712755491.1554712755491.1554712755491.1; hubspotutk=7311c009f14bdfbadf0ddc9d32a31bbb; fs_intercom=5665286442778624:6648961192755200; fs_uid=rs.fullstory.com`2MZHG`5665286442778624:6730249337634816`wanghl%40wondershare.cn`; _lo_uid=156150-1560861101687-3113866fd2f69cc5; _gid=GA1.2.641935156.1576552347; PHPSESSID=ns5du9aihl5suuc8bc8golapv7; user=wanghl%40wondershare.cn; lo_session_in=1; _lo_v=6; _lorid=156150-1576552421229-120d37426345b74f; __lotl=https%3A%2F%2Fapp.bugsplat.com%2Fv2%2Fsummary%3Fdatabase%3DWondershare_filmora_9_0_win; _gat_gtag_UA_30134220_1=1; intercom-session-g1t18z9q=OUxFU3ZVVFhVNFBNV0lNQ0prek9NaWtmRmltMGQ4WDdpSjJXVC9nNzVjZ0kvWi8wUmt4WFpucTUwbXhBYzhXay0tSE91YXdITzBmb3JIV01hZTc2b3FOUT09--c35c17263103a8e2c172dc8d1aedf050c95734a6"
VERSION = '9.3.0.23'


def repeatTime(arg):
    """
    装饰器：用于对方法的装饰，包括（1.捕获方法的异常输出的html报告 2.控制方法出错重复执行）
    :param arg: int（出错重复执行的次数）
    :return:
    """

    def decorator(func):
        def wrapper(*args, **kw):
            for i in range(int(arg)):
                try:
                    if i > 0:
                        print ("第 " + str(i) + " 次重试")
                    r = func(*args, **kw)
                    return r
                except Exception as err:
                    time.sleep(1)
                    print('【Exception】 The one case fail by :%s' % err.message)
            # raise Exception

        return wrapper

    return decorator


@repeatTime(2)
def get_first_data(pagenum, versions):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        "referer": "https://app.bugsplat.com/v2/summary"
    }
    cookies = {
        'Cookie': COOKIES
    }

    url = 'https://{}/summary/?data&filterscount=0&pagenum={}&pagesize=100&sortdatafield=crashSum&sortorder=desc&database={}&appNames=Wondershare%20Filmora%209.0,WondershareFilmora9.0&versions={}'.format(
        WONDERSHARE_HOST, pagenum, DATABASE, versions)
    print url
    r = requests.get(url, headers=headers, cookies=cookies, verify=False)
    if r.status_code != 200:
        print(r.status_code)
        raise AssertionError(
            "status_code is not 200 [error] http://{}/summary/?data&filterscount=0&pagenum={}&pagesize=10&sortdatafield=crashSum&sortorder=desc&database={}&appNames=Wondershare%20Filmora%209.0,WondershareFilmora9.0&versions={}".format(
                WONDERSHARE_HOST, pagenum, DATABASE, versions))
    elif len(r.text) == 0:
        return r.text
        # raise AssertionError("result is None")
    else:
        return r.json()


# @repeatTime(2)
def get_second_data(stackKeyId, pagenum):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        "referer": "https://app.bugsplat.com/v2/summary"
    }
    cookies = {
        'Cookie': COOKIES
    }
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    multipart_encoder = MultipartEncoder(
        fields={
            "stackKeyId": str(stackKeyId),
            "database": DATABASE,
            "pagenum": str(pagenum),
            "pagesize": "100",
            "filterscount": "0",
            "sortorder": "desc",
            "sortdatafield": "id"
        },
        boundary="-----------WebKitFormBoundaryFc1hUBsTqnP20MCX"
    )
    headers['Content-Type'] = multipart_encoder.content_type
    url = 'https://{}/browse/keycrash.php/?data&crashTimeSpan'.format(
        WONDERSHARE_HOST)
    print url
    r = requests.post(url, headers=headers, cookies=cookies, verify=False, data=multipart_encoder)
    if r.status_code != 200:
        print(r.status_code)
        raise AssertionError(
            "status_code is not 200 [error] https://{}/browse/keycrash.php/?data&crashTimeSpan".format(
                WONDERSHARE_HOST))
    elif len(r.text) == 0:
        return r.text
        # raise AssertionError("result is None")
    else:
        return r.json()


@repeatTime(2)
def get_third_data(id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        "referer": "https://app.bugsplat.com/v2/summary"
    }
    cookies = {
        'Cookie': COOKIES
    }

    r = requests.get(
        'https://{}/individualCrash/?id={}'.format(
            WONDERSHARE_HOST, id), headers=headers, cookies=cookies, verify=False)
    if r.status_code != 200:
        print(r.status_code)
        raise AssertionError(
            "status_code is not 200 [error] https://{}/individualCrash/?id={}".format(
                WONDERSHARE_HOST, id))
    # elif len(r.text) == 0:
    #     raise AssertionError("result is None")
    else:
        return r.text


@repeatTime(2)
def get_fourth_data(id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        "referer": "https://app.bugsplat.com/v2/summary"
    }
    cookies = {
        'Cookie': COOKIES
    }
    url = 'https://{}/browse/showzipcontents.php?item=log0.txt&id={}&database={}'.format(
        WONDERSHARE_HOST, id, DATABASE)
    print url
    r = requests.get(url, headers=headers, cookies=cookies, verify=False, timeout=60)
    if r.status_code != 200:
        print(r.status_code)
        raise AssertionError(
            "status_code is not 200 [error] https://{}/browse/showzipcontents.php?item=log0.txt&id={}&database={}".format(
                WONDERSHARE_HOST, id, DATABASE))
    # elif len(r.text) == 0:
    #     raise AssertionError("result is None")
    else:
        # print r.text
        return r.text


@repeatTime(2)
def get_fifth_data(id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        "referer": "https://app.bugsplat.com/v2/summary"
    }
    cookies = {
        'Cookie': COOKIES
    }
    url = 'https://{}/browse/showzipcontents.php?item=NLELog.txt&id={}&database={}'.format(
        WONDERSHARE_HOST, id, DATABASE)
    print url
    r = requests.get(url, headers=headers, cookies=cookies, verify=False, timeout=60)
    if r.status_code != 200:
        print(r.status_code)
        raise AssertionError(
            "status_code is not 200 [error] https://{}/browse/showzipcontents.php?item=NLELog.txt&id={}&database={}".format(
                WONDERSHARE_HOST, id, DATABASE))
    # elif len(r.text) == 0:
    #     raise AssertionError("result is None")
    else:
        # print r.text
        return r.text


@repeatTime(2)
def get_sixth_data(id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        "referer": "https://app.bugsplat.com/v2/summary"
    }
    cookies = {
        'Cookie': COOKIES
    }
    url = 'https://{}/browse/showzipcontents.php?item=NLELog.txt&id={}&database={}'.format(
        WONDERSHARE_HOST, id, DATABASE)
    print url
    r = requests.get(url, headers=headers, cookies=cookies, verify=False, timeout=60)
    if r.status_code != 200:
        print(r.status_code)
        raise AssertionError(
            "status_code is not 200 [error] https://{}/browse/showzipcontents.php?item=NLELog.txt&id={}&database={}".format(
                WONDERSHARE_HOST, id, DATABASE))
    # elif len(r.text) == 0:
    #     raise AssertionError("result is None")
    else:
        # print r.text
        return r.text


if __name__ == '__main__':
    # print get_first_data(0,VERSION)
    # print get_second_data(12409,0)
    # for i in [377427,421980]:
    #     print get_fourth_data(i)
    # import time
    # time.sleep(100)

    mydb = Database('192.168.11.83', 3306, 'root', 'root', 'Wang_Test')
    stackKeyIds = []
    ids = []
    num = 0
    while 1:
        first_data = get_first_data(num, VERSION)
        if len(first_data)>0:
            row_list = first_data[0]["Rows"]
            # print row_list
            for data in row_list:
                if data["comments"] is None:
                    data["comments"] = ""
                elif len(data["comments"])>0 and data["comments"][-1] == "\\":
                    data["comments"] = data["comments"][0:-1]
                sql = 'INSERT INTO bugsplat_stackTable(data_base,stackKeyId,stackKey,crashSum,comments,lastReport,firstReport) VALUES("{}","{}","{}","{}","{}","{}","{}")'.format(
                    first_data[0]["Database"], data["stackKeyId"], data["stackKey"], data["crashSum"],
                    data["comments"], data["lastReport"], data["firstReport"])
                print sql
                mydb.execNoQuery(sql)
                stackKeyIds.append(data["stackKeyId"])
            if len(row_list) < 100:
                break
            else:
                num += 1
    print stackKeyIds
    # stackKeyIds =[ u'433']
    #
    for stackKeyId in stackKeyIds:
        num = 0
        while 1:
            second_data = get_second_data(stackKeyId, num)
            if len(second_data) > 0:
                row_list2 = second_data[0]["Rows"]
                print row_list2
                for data in row_list2:
                    if data["appDescription"] is None:
                        data["appDescription"] = ""
                    data["IpAddress"] = data["IpAddress"].split('">')[-1].split('<')[0]
                    sql = 'INSERT INTO bugsplat_appTable(appid,stackKeyId,appName,appVersion,appDescription,IpAddress,crashTime) VALUES("{}","{}","{}","{}","{}","{}","{}")'.format(
                        data["id"], second_data[0]["PageData"]["stackKeyId"], data["appName"], data["appVersion"],
                        data["appDescription"], data["IpAddress"], data["crashTime"])
                    mydb.execNoQuery(sql)
                    ids.append(data["id"])
                if len(row_list2) < 100:
                    break
                else:
                    num += 1
            else:
                break
    print ids

    sql = "SELECT appid from bugsplat_appTable"
    res = mydb.execQuery(sql)
    print res
    # res = ((476669,),)
    for id in res:
        print id[0]
        fourth_data = get_fourth_data(id[0])
        # print fourth_data
        # print len(fourth_data.strip())
        if fourth_data is not None and len(fourth_data) > 0:
            try:
                memory = fourth_data.split("Memory:")[1].split("System:")[0].strip()
                system = fourth_data.split("System:")[1].split("SystemID:")[0].strip()
                systemID = fourth_data.split("SystemID:")[1].split("Metrics:")[0].strip()
                metrics = fourth_data.split("Metrics:")[1].split("Language:")[0].strip()
                language = fourth_data.split("Language:")[1].split("LogFileImpl:")[0].strip()
                logFileImpl = \
                fourth_data.split("LogFileImpl:")[1].split("-------------------------------------------------")[
                    0].strip()
                sql = 'INSERT INTO bugsplat_log0Table(appid,memory,system,systemID,metrics,language,logFileImpl) VALUES("{}","{}","{}","{}","{}","{}","{}")'.format(
                    id[0], memory, system, systemID, metrics, language, logFileImpl)
                mydb.execNoQuery(sql)
            except IndexError:
                sql = 'INSERT INTO bugsplat_log0Table(appid,memory,system,systemID,metrics,language,logFileImpl) VALUES("{}","{}","{}","{}","{}","{}","{}")'.format(
                    id[0], "#", "#", "#", "#", "#", "#")
                mydb.execNoQuery(sql)
    #
    # for id in ids:
    #     fourth_data = get_fourth_data(id)
    #     if len(fourth_data)>0:
    #         memory = fourth_data.split("Memory:")[1].split("System:")[0].strip()
    #         system = fourth_data.split("System:")[1].split("SystemID:")[0].strip()
    #         systemID = fourth_data.split("SystemID:")[1].split("Metrics:")[0].strip()
    #         metrics = fourth_data.split("Metrics:")[1].split("Language:")[0].strip()
    #         language = fourth_data.split("Language:")[1].split("LogFileImpl:")[0].strip()
    #         logFileImpl = fourth_data.split("LogFileImpl:")[1].split("-------------------------------------------------")[
    #             0].strip()
    #         sql = 'INSERT INTO bugsplat_log0Table(appid,memory,system,systemID,metrics,language,logFileImpl) VALUES("{}","{}","{}","{}","{}","{}","{}")'.format(
    #             id, memory, system, systemID, metrics, language, logFileImpl)
    #         mydb.execNoQuery(sql)

    for id in res:
        print id[0]
        fifth_data = get_fifth_data(id[0])
        print fifth_data
        print len(fourth_data.strip())
        if fifth_data is not None and len(fifth_data) > 0:
            try:
                chipType_list = fifth_data.split("ChipType:")
                # print len(chipType_list)
                if len(chipType_list) == 2:
                    chipType = fifth_data.split("ChipType:")[1].split("[")[0].strip()
                    driverVersion = fifth_data.split("DriverVersion:")[1].split("[")[0].strip()
                    print "1：", chipType, driverVersion
                    sql = 'INSERT INTO bugsplat_NLELogTable(appid,chipType,driverVersion) VALUES("{}","{}","{}")'.format(
                        id[0], chipType, driverVersion)
                    mydb.execNoQuery(sql)
                elif len(chipType_list) < 2:
                    chipType = "#"
                    driverVersion = "#"
                    sql = 'INSERT INTO bugsplat_NLELogTable(appid,chipType,driverVersion) VALUES("{}","{}","{}")'.format(
                        id[0], "#", "#")
                    mydb.execNoQuery(sql)
                    print "2：", chipType, driverVersion
                else:
                    chipType = fifth_data.split("ChipType:")[1].split("[")[0].strip()
                    driverVersion = fifth_data.split("DriverVersion:")[1].split("[")[0].strip()
                    sql = 'INSERT INTO bugsplat_NLELogTable(appid,chipType,driverVersion) VALUES("{}","{}","{}")'.format(
                        id[0], chipType, driverVersion)
                    mydb.execNoQuery(sql)

                    chipType2 = fifth_data.split("ChipType:")[2].split("[")[0].strip()
                    driverVersion2 = fifth_data.split("DriverVersion:")[2].split("[")[0].strip()
                    sql = 'INSERT INTO bugsplat_NLELogTable(appid,chipType,driverVersion) VALUES("{}","{}","{}")'.format(
                        id[0], chipType2, driverVersion2)
                    mydb.execNoQuery(sql)
                    print "3：", chipType, driverVersion, chipType2, driverVersion2

            except IndexError:
                pass
                sql = 'INSERT INTO bugsplat_NLELogTable(appid,chipType,driverVersion) VALUES("{}","{}","{}")'.format(
                    id[0], "#", "#")
                mydb.execNoQuery(sql)

