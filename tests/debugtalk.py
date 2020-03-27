# -*-coding:utf-8-*-
import requests, re, json

session = requests.Session()
header = {
    "Host": "www.filmstocks.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "Cookie": "",
    # 'Connection': 'close'
}

URL = "www.filmstocks.com"


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
                    import time
                    time.sleep(1)
                    print('【Exception】 The one case fail by :%s' % err.message)
            raise err

        return wrapper

    return decorator


import urllib2


def url_open(url):
    """
    访问主页获取wondershare_session_id与hash
    :param url:
    :return:
    """
    res = urllib2.Request(url)
    res.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36")
    response = urllib2.urlopen(res, timeout=10)
    return response


# def get_wondershare_session_id(bool=0, url="www.filmstocks.com"):
#     """
#     获取响应头cookie里的wondershare_session_id
#     :return:
#     """
#     response = url_open("https://{}".format(url))
#     res = {}
#     for h in response.info().headers:
#         if "wondershare_session_id" in h:
#             wondershare_session_id = h.split("wondershare_session_id=")[1].split(";")[0]
#             res["wondershare_session_id"] = wondershare_session_id
#
#     pattern = re.compile(r'<meta name="__hash__" content="(.*)">')
#     hash = pattern.findall(response.read())[0]
#     res["hash"] = hash
#     if int(bool) == 1:
#         return res["wondershare_session_id"]
#     return res

def request_open(url):
    res = session.get(url, headers=header,
                      verify=False)
    return res


def get_wondershare_session_id(bool=0, url="www.filmstocks.com"):
    """
    获取响应头cookie里的wondershare_session_id
    :return:
    """
    res = {}
    if "__hash__" in session.cookies.keys() and "wondershare_session_id" in session.cookies.keys():
        for item in session.cookies:
            if str(item.name) == "__hash__":
                res["hash"] = item.value
            if str(item.name) == "wondershare_session_id":
                res["wondershare_session_id"] = item.value
        return res

    response = request_open("https://{}/".format(url))
    cookie = response.headers["Set-Cookie"]
    if "wondershare_session_id" in cookie:
        wondershare_session_id = cookie.split("wondershare_session_id=")[1].split(";")[0]
        res["wondershare_session_id"] = wondershare_session_id
    if "__hash__" in cookie:
        hash = cookie.split("__hash__=")[1].split(";")[0]
        res["hash"] = hash
    if int(bool) == 1:
        return res["wondershare_session_id"]
    return res


def get_login_cookies():
    """
    生成登录cookie
    :return:
    """

    login_header = header
    if "__hash__" in session.cookies.keys() and "wondershare_session_id" in session.cookies.keys():
        res = {}
        for item in session.cookies:
            if str(item.name) == "__hash__":
                res["hash"] = item.value
            if str(item.name) == "wondershare_session_id":
                res["wondershare_session_id"] = item.value
        login_cookie = "wondershare_session_id={};__hash__={}".format(res["wondershare_session_id"],
                                                                      res["hash"])
        return login_cookie
    heads = get_wondershare_session_id()
    # print heads
    login_header["Cookie"] = "wondershare_session_id={};__hash__={}".format(heads["wondershare_session_id"],
                                                                            heads["hash"])
    # r = session.get("https://www.filmstocks.com/login.html?redirect=https%3A%2F%2Fwww.filmstocks.com%2F",
    #                 headers=header, verify=False)
    # if "__hash__" in r.headers["Set-Cookie"]:
    #     hash = r.headers["Set-Cookie"].split("__hash__=")[1].split(";")[0]
    # else:
    #     raise Exception("hash,不存在")
    # login_header["Cookie"] = "wondershare_session_id={};__hash__={}".format(heads["wondershare_session_id"], hash)
    return login_header["Cookie"]


def get_hash(bool=0, url="www.filmstocks.com"):
    """
    获取响应体content里的hash
    :return:
    """
    if bool == 0:
        if "__hash__" in session.cookies.keys():
            return session.cookies.get("__hash__")
    else:
        if "__hash__" in session.cookies.keys():
            session.cookies.pop("__hash__")
    login_header = header
    heads = get_wondershare_session_id()
    login_header["Cookie"] = "wondershare_session_id={};__hash__={}".format(heads["wondershare_session_id"],
                                                                            heads["hash"])
    r = session.get("https://{}/login.html?redirect=https%3A%2F%2Fwww.filmstocks.com%2F".format(url),
                    headers=header, verify=False)
    if "__hash__" in r.headers["Set-Cookie"]:
        hash = r.headers["Set-Cookie"].split("__hash__=")[1].split(";")[0]
    else:
        raise Exception("hash,不存在")
    return hash


# @repeatTime(3)
def get_login_token(bool=0, url="www.filmstocks.com"):
    """
    获取登录接口响应体content里的token
    :return:
    """
    if "auth_token" in session.cookies.keys():
        token = session.cookies.get("auth_token")
        wondershare_session_id = session.cookies.get("wondershare_session_id")
        if str(bool) == "1":
            hash = session.cookies.get("__hash__")
            result = "auth_token={} ;wondershare_session_id={};__hash__={};".format(token,
                                                                                    wondershare_session_id,
                                                                                    hash)
        else:
            result = "auth_token={} ;wondershare_session_id={};".format(token,
                                                                        wondershare_session_id)
        return result

    login_header = header
    heads = get_wondershare_session_id()
    login_header["Cookie"] = "wondershare_session_id={};__hash__={}".format(heads["wondershare_session_id"],
                                                                            heads["hash"])
    data = {"email": "wanghao@wondershare.cn", "password": "123456", "__hash__": heads["hash"], "remember": "0"}
    res = session.post("https://{}/api/user/login".format(url), headers=login_header, verify=False, data=data)
    print res.content
    token = json.loads(res.content)["data"]["token"]
    result = "auth_token={} ;wondershare_session_id={};".format(token,
                                                                heads["wondershare_session_id"])
    return result


def get_login_cookies2(url="www.filmstocks.com"):
    """
    生成登录cookie
    :return:
    """

    login_header = header
    heads = {}
    response = request_open("https://{}/".format(url))
    cookie = response.headers["Set-Cookie"]
    if "wondershare_session_id" in cookie:
        wondershare_session_id = cookie.split("wondershare_session_id=")[1].split(";")[0]
        heads["wondershare_session_id"] = wondershare_session_id
    if "__hash__" in cookie:
        hash = cookie.split("__hash__=")[1].split(";")[0]
        heads["hash"] = hash

    login_header["Cookie"] = "wondershare_session_id={};__hash__={}".format(heads["wondershare_session_id"],
                                                                            heads["hash"])
    return login_header["Cookie"]



def test_shopcart(site = "shopcart.wondershare.com",goods_id = "4460"):
    url = "https://" + site + "/pay/checkout.html?goods_id=" + goods_id + "&currency=USD"

    if "__hash__" in session.cookies.keys() and "wondershare_session_id" in session.cookies.keys():
        res = {}
        for item in session.cookies:
            if str(item.name) == "__hash__":
                res["hash"] = item.value
            if str(item.name) == "wondershare_session_id":
                res["wondershare_session_id"] = item.value
        login_cookie = "wondershare_session_id={};__hash__={}".format(res["wondershare_session_id"],
                                                                      res["hash"])
        return login_cookie

    rp = session.get(url = url,verify = False)
    cookie = str(rp.cookies)
    ha = re.compile("__hash__=+(.*?)[ ]").findall(cookie)
    ha = "".join(ha)  #str.join(元组，列表，字典，字符串)  将此转化成字符串
    sid = re.compile("wondershare_session_id=+(.*?)[ ]").findall(cookie)
    sid = "".join(sid)
    #获取cart_code
    cart_code = re.compile("_ws_cart_code=+(.*?)[ ]").findall(cookie)
    cart_code = "".join(cart_code)
    cie = 'wondershare_session_id=' + sid + ';__hash__=' + ha + ';_ws_cart_code=' + cart_code
    return cie


def get_shopcart_cookie(site="shopcart.wondershare.com", goods_id="4460"):
    url = "https://" + site + "/pay/checkout.html?goods_id=" + goods_id + "&currency=USD"

    if "__hash__" in session.cookies.keys():
        for item in session.cookies:
            if str(item.name) == "__hash__":
                return item.value

    rp = session.get(url=url, verify=False)
    cookie = str(rp.cookies)
    ha = re.compile("__hash__=+(.*?)[ ]").findall(cookie)
    ha = "".join(ha)  # str.join(元组，列表，字典，字符串)  将此转化成字符串
    return ha


if __name__ == '__main__':
    # print get_hash()
    # print get_login_token()

    # print get_login_token(1)
    print get_shopcart_cookie()
    print "----------------------"
    print test_shopcart()
    # tt()
