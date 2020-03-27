# -*-coding:utf-8-*-
import requests
import re

session = requests.Session()
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Host": "testgit.wondershare.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
}

def getToken():
    html = session.get('http://testgit.wondershare.cn/users/sign_in', headers=header)
    pattern = re.compile(r'<input type="hidden" name="authenticity_token" value="(.*)" />')

    authenticity_token = pattern.findall(html.content)[0]
    return authenticity_token

def auth():
    payload = {'username': 'wanghao',
               'password': 'Hello789',
               'authenticity_token': getToken(),
               'utf8': '%E2%9C%93'}
    r = session.post('http://testgit.wondershare.cn/users/auth/ldapmain/callback', data=payload, headers=header)
    return r


r = auth()
if r.status_code == 200:
    if "AutoMagic自动化测试平台代码以及自动化用例代码" in r.content:
        print "成功登录git"
    else:
        raise Exception("AutoMagic自动化测试平台代码以及自动化用例代码：不在返回结果里")
else:
    raise Exception("接口请求返回status_code不为：200")
