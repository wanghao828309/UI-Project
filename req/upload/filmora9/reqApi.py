#!/usr/bin/python
# -*- coding: UTF-8 -*-
# from urllib3 import encode_multipart_formdata
import requests, random, string, json
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder
from req.utils.mysqldbUtil import MysqldbHelper
from req.utils.LogUtil import Logger

logger = Logger(logger="reqApi_log").getlog()

WONDERSHARE_HOST = "omp.wondershare.com"

# 测试环境
# custom_cdn_domain = "http://vpcdn10.wondershare.cn"
# GATEWAY_HOST = 'vp-fsapi.wondershare.com'
# 灰度环境
custom_cdn_domain = "http://vpcdn11.wondershare.com"
GATEWAY_HOST = 'vp-fsapi.wondershare.com'

filmora_cookies = "_ga=GA1.2.728978294.1554170243; ws_visit_id=2_190402102749237_3611; _ws_device_id=9709cac32b1dc49d; uts_id=uts1560150865.649; _hjid=31b491b8-8969-4222-938a-c480b05aafb7; _gcl_aw=GCL.1575421325.EAIaIQobChMIr7-P0eWa5gIVyLWWCh3ZzAkaEAAYASAAEgJfDvD_BwE; _gac_UA-4839360-2=1.1575421329.EAIaIQobChMIr7-P0eWa5gIVyLWWCh3ZzAkaEAAYASAAEgJfDvD_BwE; web_client_sign=%257B60070580-4155-4818-99E5-AD8D11F57CD7%257D; siteid=1; _gcl_au=1.1.930452447.1578726279; _ws_id.101.de8e=9709cac32b1dc49d.pyc6xg.21.q3xkzs.q3xkzs.7f6T02b4; tp3_sessionid=f4m4t7oq9c1eho7i65tm80uph4; jump_page=%2FResource%2Findex.html%3Fcid%3D561%26p%3D530; HTTP_REFERER=%2FResource%2Fedit%3Fid%3D39152"


def gen_random_string(str_len):
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len))


def getTime():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_token():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        "referer": WONDERSHARE_HOST,
        'Cookie': filmora_cookies
    }
    r = requests.get('https://{}/File/getUploadToken.html'.format(WONDERSHARE_HOST), headers=headers, verify=False)
    if r.status_code != 200:
        print(r.status_code)
        raise AssertionError(
            "status_code is not 200 [error] http://{}/File/getUploadToken.html".format(WONDERSHARE_HOST))
    else:
        return r.json()["data"]


def post_files(filepath, file_type=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        "referer": WONDERSHARE_HOST,
        "Connection": "close"
    }
    res = get_token()
    filename = filepath.split("\\")[-1]
    # f = open(filepath, 'rb')
    # print filename
    try:
        # files = {"field1": (filename, open(filepath, 'rb'),"image/jpeg")}
        # data = {'file_type': file_type}
        multipart_encoder = MultipartEncoder(
            fields={
                'file_type': str(file_type),
                'file': (filename, open(filepath, 'rb')),
                # 测试环境cn，线上环境com
                "custom_cdn_domain": custom_cdn_domain,
                "upload_image_url": 'http://{}/file/upload'.format(GATEWAY_HOST),
                "token": res["token"],
                # "Filename":"b00bec66d4905d1ac6d7798b14732651.zip",
                "slot": res["slot"]
            },
            boundary="--------------------------540102534916200623112597"
        )
        headers['Content-Type'] = multipart_encoder.content_type
        print  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        r = requests.post('http://{}/file/upload'.format(GATEWAY_HOST), headers=headers, data=multipart_encoder,
                          timeout=300)
        print  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    except requests.exceptions.ConnectTimeout:
        raise RuntimeError("接口请求超时 [error] http://{}/file/upload".format(GATEWAY_HOST))
    except Exception as e:
        print e.message
    if r.status_code != 200:
        print("接口返回状态码：{}".format(r.status_code))
        raise AssertionError("status_code is not 200 [error] http://{}/file/upload".format(GATEWAY_HOST))
    # print(r.json())
    if r.json()["code"] == 0:
        return (r.json()["data"]["url"])
    elif r.json()["code"] == 10001 or r.json()["code"] == 10006:
        raise AssertionError("code is 10001 [error] http://{}/file/upload NO Permission Auth".format(GATEWAY_HOST))
    else:
        raise AssertionError("code is not 0 [error] http://{}/file/upload 接口传递File的内容为空".format(GATEWAY_HOST))


def exce_pack9_multi_language(slug):
    mydb = MysqldbHelper(host='192.168.11.83', port=3306, user='root', password='root', db='Wang_Test')
    sql = 'SELECT en,fr,de,es,it,pt,jp FROM pack9_multi_language WHERE  en = \"{}\"'.format(slug)

    # mydb = MysqldbHelper(host='192.168.11.82', port=3307, user='vp_filmora_read', password='ERatt##89235',
    #                      db='filmora_es_admin')
    # sql = 'SELECT title FROM wx_pack_9_resource WHERE  slug = \"{}\" ORDER BY updatetime'.format(slug)
    result = mydb.executeSqlOne(sql)
    return result


def post_ResourceAdd(filename, url, slug, id1, id2, resource_type, description="wang auto"):
    """
    新增商城资源接口
    :param filename:
    :param url:
    :param slug:
    :param id1:
    :param id2:
    :param resource_type:
    :param description:
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
    }
    # filename = filepath.split("\\")[-1]
    de, es, fr, it, jp, pt = "", "", "", "", "", ""
    # if description == "store auto":
    #     de, es, fr, it, jp, pt = "", "", "", "", "", ""
    # else:
    #     file_list = filename.split(" ")
    #     val = str(file_list[-1])
    #     de, es, fr, it, jp, pt = "Geteilter Bildschirm {}".format(str(file_list[-1])), "Pantalla Dividida {}".format(
    #         str(file_list[-1])), "Écran partagé {}".format(str(file_list[-1])), "Schermo Diviso {}".format(
    #         str(file_list[-1])), "分割表示 {}".format(
    #         str(file_list[-1])), "Tela Dividida {}".format(str(file_list[-1]))
    #     en = "Split Screen {}".format(str(file_list[-1]))
    #     print de, es, fr, it, jp, pt, en
    #     # r = exce_pack9_multi_language(filename)
    #     # if r is not None:
    #     #     de = r["de"]
    #     #     es = r["es"]
    #     #     fr = r["fr"]
    #     #     it = r["it"]
    #     #     jp = r["jp"]
    #     #     pt = r["pt"]

    multipart_encoder = MultipartEncoder(
        fields={
            'info[title][de]': de,
            'info[title][en]': filename,
            'info[title][es]': es,
            'info[title][fr]': fr,
            'info[title][it]': it,
            'info[title][jp]': jp,
            'info[title][pt]': pt,
            'info[description]': description,
            'info[download_url]': url,
            'info[resource_status]': '3',
            'info[resource_type]': str(resource_type),
            'info[resource_version]': "1.0.0",
            'info[status]': '99',
            'inputtime': getTime(),
            'info[slug]': slug,
            'dosubmit': "提交",
            'category_id[0]': str(id1),
            'category_id[1]': str(id2),
            '__hash__': "93d0d292eba73d9a40c9bcc82c4039f6_27090f865c3c4055c63c1f8c1742b664"
            # 'file': (os.path.basename(argv_dict['file']), open(argv_dict['file'], 'rb'), 'application/octet-stream')
        },
        boundary='----WebKitFormBoundary' + gen_random_string(16)
    )

    headers['Content-Type'] = multipart_encoder.content_type
    # 请求头必须包含一个特殊的头信息，类似于Content-Type: multipart/form-data; boundary=${bound}
    cookies = {
        'Cookie': filmora_cookies
    }
    url = "https://{}/Resource/add?".format(WONDERSHARE_HOST)
    r = requests.post(url, data=multipart_encoder, headers=headers, cookies=cookies, verify=False)
    # print(r.text)
    return r.text


def post_ResourceEdit(filename, download_url, slug, id1, id2, resource_type, description="wang edit"):
    """
    编辑资源接口
    :param filename:
    :param download_url:
    :param slug:
    :param id1:
    :param id2:
    :param resource_type:
    :param description:
    :return:
    """
    # 灰度环境
    mydb = MysqldbHelper(host='192.168.11.82', port=3308, user='vp_f_read', password='vSYaTqhjmtJ+l7ix',
                         db='f_common')
    # 测试环境
    # mydb = MysqldbHelper(host='10.10.18.252', port=33064, user='f_common', password='f_common@cloud', db='f_common')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
    }
    # filename = filepath.split("\\")[-1]
    sql = 'SELECT id,resource_version,download_url from wx_pack_9_resource  where slug = \"{}\" and (resource_status = 3 or resource_status = 1)'.format(
        slug)
    # print sql
    r = mydb.executeSqlOne(sql)
    # print r
    if r is not None:
        url = "https://{}/Resource/edit?id={}".format(WONDERSHARE_HOST, r['id'])
    else:
        print 'SELECT id,resource_version from wx_pack_9_resource  where slug = \"{}\" and resource_status = 3'.format(
            slug) + " 查询的结果为空"
        return
        # print url
    if download_url == "":
        download_url = r["download_url"]

    # file_list = filename.split(" ")
    # val  = str(file_list[-1])
    # de, es, fr, it, jp, pt = "Geteilter Bildschirm {}".format(str(file_list[-1])), "Pantalla Dividida {}".format(
    #     str(file_list[-1])), "Écran partagé {}".format(str(file_list[-1])), "Schermo Diviso {}".format(str(file_list[-1])), "分割表示 {}".format(
    #     str(file_list[-1])), "Tela Dividida {}".format(str(file_list[-1]))
    # en = "Split Screen {}".format(str(file_list[-1]))
    # print de, es, fr, it, jp, pt, en
    # de, es, fr, it, jp, pt = "", "", "", "", "", ""

    res = exce_pack9_multi_language(filename)
    if res is not None:
        # r = json.loads(res)
        # de = r["title"]["de"]
        # es = r["title"]["es"]
        # fr = r["title"]["fr"]
        # it = r["title"]["it"]
        # jp = r["title"]["jp"]
        # pt = r["title"]["pt"]

        de = res["de"]
        es = res["es"]
        fr = res["fr"]
        it = res["it"]
        jp = res["jp"]
        pt = res["pt"]
    else:
        de, es, fr, it, jp, pt = "", "", "", "", "", ""
        if description == "default Edit":
            logger.error(
                'SELECT title FROM wx_pack_9_resource WHERE  slug = \"{}\" ORDER BY updatetime'.format(slug) + " 结果为空")

    print filename
    fields = {
        'id': str(r['id']),
        'info[title][de]': de,
        'info[title][en]': filename,
        'info[title][es]': es,
        'info[title][fr]': fr,
        'info[title][it]': it,
        'info[title][jp]': jp,
        'info[title][pt]': pt,
        'info[description]': description,
        'info[download_url]': download_url,
        'info[resource_status]': '3',
        'info[resource_type]': str(resource_type),
        'info[resource_version]': str(r["resource_version"]),
        'info[status]': '99',
        'inputtime': getTime(),
        'info[slug]': slug,
        'dosubmit': "提交",
        '__hash__': "a1656aff97b26f16d588a13310b9d39f_80cd895355f9b9d6b96a7d63d921bf7c"
    }
    j = 0
    id = []
    id.append(id1)
    id.append(id2)
    for i in id:
        if i != " " and i != "":
            # print j
            fields["category_id[" + str(j) + "]"] = str(i)
            j = j + 1

    multipart_encoder = MultipartEncoder(
        fields=fields,
        boundary='----WebKitFormBoundary' + gen_random_string(16)
    )

    headers['Content-Type'] = multipart_encoder.content_type
    # 请求头必须包含一个特殊的头信息，类似于Content-Type: multipart/form-data; boundary=${bound}
    cookies = filmora_cookies
    headers.setdefault("Cookie", cookies)
    # cookies = {
    #     'Cookie': filmora_cookies
    # }
    r = requests.post(url, data=multipart_encoder, headers=headers, verify=False)
    # print r.text
    return r.text


def post_Pack9Add(en, jp, slug, resource_name):
    # # 灰度环境
    mydb = MysqldbHelper(host='192.168.11.82', port=3308, user='vp_f_read', password='vSYaTqhjmtJ+l7ix', db='f_common')
    # 测试环境
    # mydb = MysqldbHelper(host='10.10.18.252', port=33064, user='f_common', password='f_common@cloud', db='f_common')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
    }
    resource = []
    for name in resource_name:
        # print name
        sql = 'SELECT id from wx_pack_9_resource where slug = \"{}\"'.format(
            name) + "ORDER BY id DESC"
        result = mydb.executeSqlOne(sql)
        if result is not None:
            key = "resource_ids[" + name + "]"
            resource.append((key, result["id"]))
        else:
            print "数据库查询结果为空：" + sql
    # print resource
    fields = {
        'info[title][de]': '',
        'info[title][en]': en,
        'info[title][es]': '',
        'info[title][fr]': '',
        'info[title][it]': '',
        'info[title][jp]': jp,
        'info[title][pt]': '',
        'info[status]': '99',
        'inputtime': getTime(),
        'info[slug]': slug,
        'dosubmit': "提交",
        '__hash__': "93d0d292eba73d9a40c9bcc82c4039f6_27090f865c3c4055c63c1f8c1742b664"
        # 'file': (os.path.basename(argv_dict['file']), open(argv_dict['file'], 'rb'), 'application/octet-stream')
        # file为路径
    }
    for key, value in dict(resource).items():
        fields[key] = str(value)
    # print fields

    multipart_encoder = MultipartEncoder(
        fields=fields,
        boundary='----WebKitFormBoundary' + gen_random_string(16)
    )

    headers['Content-Type'] = multipart_encoder.content_type
    # 请求头必须包含一个特殊的头信息，类似于Content-Type: multipart/form-data; boundary=${bound}
    cookies = {
        'Cookie': filmora_cookies
    }
    # headers.setdefault("Cookie", cookies)

    url = "https://{}/Pack9/add".format(WONDERSHARE_HOST)
    r = requests.post(url, data=multipart_encoder, headers=headers, cookies=cookies,verify=False)
    if r.status_code != 200:
        print("接口返回状态码：{}".format(r.status_code))
        return
    # print(r.text)
    return r.text


# -----------------------------------------------------神剪手-----------------------------------------------------#

SHENCUT_UPLOAD_HOST = "uploadapi.shencut.com"
SHENCUT_ADMIN_HOST = "admin.shencut.com"
shencut_cookies = "td_cookie=18446744070925971448; _ga=GA1.2.361015770.1559631642; _ws_device_id=551bea637e312eb9; siteid=1; last_linkid=follow_effect; affsrc=affilate%3Dfollow_effect%26active_id%3Dcaddy_148; Affilate_Cookies=follow_effect%26active_id%3Dcaddy_148; Hm_lvt_a4cb73a16fc635e34a65e273baf02a96=1583809157; Hm_lvt_afe3c799763cf9ac9db4d0c5da6419b3=1583809157; _ws_id.105.15bc=551bea637e312eb9.pwkymf.11.q6yiza.q6yiyt.8dZH4FmX; hhailuo_sessionid=b3ojt27f1f6e3ts26qd6undb65"


def post_shenCut_files(filepath):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        "referer": WONDERSHARE_HOST
    }
    filename = filepath.split("\\")[-1]
    print filename
    try:
        multipart_encoder = MultipartEncoder(
            fields={
                'fileSizeLimit': "700 MB",
                'Filedata': (filename, open(filepath, 'rb'), "application/octet-stream"),
                "fileTypeExts": "fmrp|zip",
                "watermark_enable": "0",
                "Filename": filename,
            },
            boundary="--------------------------540102534916200623112597"
        )
        headers['Content-Type'] = multipart_encoder.content_type
        print  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        r = requests.post('http://{}/upload.html'.format(SHENCUT_UPLOAD_HOST), headers=headers, data=multipart_encoder)
        print  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    except requests.exceptions.ConnectTimeout:
        raise RuntimeError("接口请求超时 [error] http://{}/upload.html".format(SHENCUT_UPLOAD_HOST))
    if r.status_code != 200:
        print("接口返回状态码：{}".format(r.status_code))
        raise AssertionError("status_code is not 200 [error] http://{}/upload.html".format(SHENCUT_UPLOAD_HOST))
    print(r.json())
    if r.json()["code"] == 0:
        return ("http://download.shencut.com/" + r.json()["data"]["url"])
    elif r.json()["code"] == 10001 or r.json()["code"] == 10006:
        raise AssertionError(
            "code is 10001 [error] http://{}/upload.html NO Permission Auth".format(SHENCUT_UPLOAD_HOST))
    else:
        raise AssertionError("code is not 0 [error] http://{}/upload.html 接口传递File的内容为空".format(SHENCUT_UPLOAD_HOST))


def post_shenCutAdd(filename, url, slug, id1, id2, resource_type, description="SamplePackage shenCut auto"):
    """
    新增神剪手商城资源接口
    :param filename:
    :param url:
    :param slug:
    :param id1:
    :param id2:
    :param resource_type:
    :param description:
    :return:
    """
    # # 灰度环境
    # mydb = MysqldbHelper(host='192.168.11.43', port=3306, user='vp_store_read', password='ppYDC##821348', db='store')
    # url = ""
    # sql = 'SELECT id,resource_version,download_url from wx_pack_9_resource  where slug = \"{}\" and (resource_status = 3 or resource_status = 1)'.format(
    #     slug)
    # # print sql
    # r = mydb.executeSqlOne(sql)
    # # print r
    # if r is None:
    #     print 'SELECT id,resource_version from wx_pack_9_resource  where slug = \"{}\" and resource_status = 3'.format(
    #         slug) + " 查询的结果为空"
    #     return
    # if url == "":
    #     url = r["download_url"]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
    }

    multipart_encoder = MultipartEncoder(
        fields={
            'info[title][zh]': str(filename),
            'info[description]': description,
            'info[download_url]': url,
            'info[resource_status]': '3',
            'info[resource_type]': str(resource_type),
            'info[resource_version]': "1.0.0",
            'info[status]': '99',
            'info[thumb]': '',
            'inputtime': getTime(),
            'info[slug]': slug,
            'dosubmit': "提交",
            'category_id[0]': str(id1),
            'category_id[1]': str(id2),
            '__hash__': "0240adbf4b02a721a8e21ae4bc2b741d_e4ac70633e0e11532d9d99842deb45b7"
            # 'file': (os.path.basename(argv_dict['file']), open(argv_dict['file'], 'rb'), 'application/octet-stream')
        },
        boundary='----WebKitFormBoundary2ryjSaId7' + gen_random_string(16)
    )

    headers['Content-Type'] = multipart_encoder.content_type
    # 请求头必须包含一个特殊的头信息，类似于Content-Type: multipart/form-data; boundary=${bound}
    cookies = shencut_cookies
    headers.setdefault("Cookie", cookies)
    url = "http://{}/Resource/add?".format(SHENCUT_ADMIN_HOST)
    r = requests.post(url, data=multipart_encoder, headers=headers)
    # print(r.text)
    return r.text


def post_shenCutEdit(filename, download_url, slug, id1, id2, resource_type, description="wang edit"):
    """
    编辑资源接口
    :param filename:
    :param download_url:
    :param slug:
    :param id1:
    :param id2:
    :param resource_type:
    :param description:
    :return:
    """
    # 灰度环境
    mydb = MysqldbHelper(host='192.168.11.43', port=3306, user='vp_store_read', password='ppYDC##821348', db='store')
    # slug = slug+"_vlog"
    # 测试环境
    # mydb = MysqldbHelper(host='10.10.19.117', port=3306, user='root', password='root', db='store')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
    }
    # filename = filepath.split("\\")[-1]
    sql = 'SELECT id,resource_version,download_url from wx_pack_9_resource  where slug = \"{}\" and (resource_status = 3 or resource_status = 1)'.format(
        slug)
    # print sql
    r = mydb.executeSqlOne(sql)
    # print r
    if r is not None:
        url = "http://{}/Resource/edit?id={}".format(SHENCUT_ADMIN_HOST, r['id'])
    else:
        print 'SELECT id,resource_version from wx_pack_9_resource  where slug = \"{}\" and (resource_status = 3 or resource_status = 1)'.format(
            slug) + " 查询的结果为空"
        return
        # print url
    if download_url == "":
        download_url = r["download_url"]

    print filename
    fields = {
        'id': str(r['id']),
        'info[title][zh]': filename,
        'info[description]': description,
        'info[download_url]': download_url,
        'info[resource_status]': '3',
        'info[resource_type]': str(resource_type),
        'info[resource_version]': str(r["resource_version"]),
        'info[status]': '99',
        'inputtime': getTime(),
        'info[slug]': slug,
        'dosubmit': "提交",
        '__hash__': "a1656aff97b26f16d588a13310b9d39f_80cd895355f9b9d6b96a7d63d921bf7c"
    }
    j = 0
    id = []
    id.append(id1)
    id.append(id2)
    for i in id:
        if i != " " and i != "":
            # print j
            fields["category_id[" + str(j) + "]"] = str(i)
            j = j + 1

    multipart_encoder = MultipartEncoder(
        fields=fields,
        boundary='----WebKitFormBoundary' + gen_random_string(16)
    )

    headers['Content-Type'] = multipart_encoder.content_type
    # 请求头必须包含一个特殊的头信息，类似于Content-Type: multipart/form-data; boundary=${bound}
    cookies = shencut_cookies
    headers.setdefault("Cookie", cookies)
    r = requests.post(url, data=multipart_encoder, headers=headers)
    # print r.text
    return r.text


def post_shenCutPackAdd(zh, jp, slug, resource_name):
    """
    打包神剪手
    :param en:
    :param slug:
    :param resource_name:
    :return:
    """
    # # 灰度环境
    mydb = MysqldbHelper(host='192.168.11.43', port=3306, user='vp_store_read', password='ppYDC##821348', db='store')
    # 测试环境
    # mydb = MysqldbHelper(host='10.10.19.117', port=3306, user='root', password='root', db='store')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
    }
    resource = []
    for name in resource_name:
        # print name
        sql = 'SELECT id from wx_pack_9_resource where slug = \"{}\"'.format(
            name) + "ORDER BY id DESC"
        result = mydb.executeSqlOne(sql)
        if result is not None:
            key = "resource_ids[" + name + "]"
            resource.append((key, result["id"]))
        else:
            print "数据库查询结果为空：" + sql
    # print resource
    fields = {
        'info[title][zh]': zh,
        'info[status]': '99',
        'inputtime': getTime(),
        'info[slug]': slug,
        'dosubmit': "提交",
        '__hash__': "93d0d292eba73d9a40c9bcc82c4039f6_27090f865c3c4055c63c1f8c1742b664"
        # 'file': (os.path.basename(argv_dict['file']), open(argv_dict['file'], 'rb'), 'application/octet-stream')
        # file为路径
    }
    for key, value in dict(resource).items():
        fields[key] = str(value)
    # print fields

    multipart_encoder = MultipartEncoder(
        fields=fields,
        boundary='----WebKitFormBoundary' + gen_random_string(16)
    )

    headers['Content-Type'] = multipart_encoder.content_type
    # 请求头必须包含一个特殊的头信息，类似于Content-Type: multipart/form-data; boundary=${bound}
    cookies = shencut_cookies
    headers.setdefault("Cookie", cookies)

    url = "http://{}/Pack9/add".format(SHENCUT_ADMIN_HOST)
    r = requests.post(url, data=multipart_encoder, headers=headers)
    if r.status_code != 200:
        print("接口返回状态码：{}".format(r.status_code))
        return
    # print(r.text)
    return r.text


if __name__ == '__main__':
    pass
    # print post_files(r"C:\Users\ws\Desktop\Beach.zip")
    # print mydb
    # url = post_shenCut_files(r"C:\Users\ws\Desktop\Arp Intro.zip")
    # print post_shenCutAdd("Arp Intro", "http://download.shencut.com/downloads/2019-03-11/5c861a42878ea.zip", "Arp_Intro", 273, 281, 1)

    # test()
    # print(get_token())
    # print post_ResourceEdit("test04","http://resimg.wondershare.com/s3/f224cb6d4e9872c20e3c73797dbc6fdb.zip","test","44","78","1")
    # post_files(u"C:\\Users\ws\Desktop\éclat.zip", 2)b
    # post_ResourceAdd("Beep","","","","","")

    # m = MyExcelUtil("C:\Users\ws\Desktop\wang.xls")
    # l = []
    # for j in range(0, 190):
    #     v = m.get_rowCol_data(j, 0)
    #     l.append(v)
    #     # print v
    # for i in range(1, m.get_row_num(0)):
    #     r = m.get_rowCol_data(i, 1)
    #     if r not in l:
    #         print r
    #         MyExcelUtil(r"C:\Users\ws\Desktop\wang.xls").write_data(i, 3, r,
    #                                         MyExcelUtil.set_style(8),
    #                                         0)
