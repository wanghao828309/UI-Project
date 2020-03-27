# coding=utf-8


import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from time import sleep

GATEWAY_HOST = '10.14.1.138:8001'


def decorator(func):
    def wrapper(*args, **kw):
        for i in range(4):
            try:
                if i > 0:
                    print("第 " + str(i) + " 次重试")
                r = func(*args, **kw)
                return r
            except Exception as err:
                sleep(3)
                if i > 2:
                    _send_mail(str(err))
                    print('The one case fail by :%s' % err)
        raise Exception

    return wrapper


def _send_mail(mess):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "770834094@qq.com"  # 用户名
    mail_pass = "lmaxcmjvoeydbbjj"  # 口令

    sender = '770834094@qq.com'
    receivers = ['wanghao@dachentech.com.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(mess, 'plain', 'utf-8')
    message['From'] = '770834094@qq.com'
    message['To'] = 'wanghao@dachentech.com.cn'

    subject = '接口报错自动发送的邮件'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"


def _register(phone, password):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://effects.wondershare.com/login.html'
        }
        r = requests.post('https://{}/api/user/register'.format(GATEWAY_HOST), data={
            'email': phone,
            'password': password,
            'repassword': password,
            '__hash__': "45015900a44ff0764f1cbf5a4cf3dc5f_26c8ba545603d1dd8409fba15853d5fc",
        }, headers=headers, timeout=10)
    except requests.exceptions.ConnectTimeout:
        raise RuntimeError("接口请求超时Timeout>5 [error] http://{}/api/user/register".format(GATEWAY_HOST))
    except Exception:
        raise RuntimeError("Exception [error] http://{}/api/user/register".format(GATEWAY_HOST))

    # if r is None:
    #     raise RuntimeError("接口返回值为空 [error] http://{}/api/user/register".format(GATEWAY_HOST))
    # elif r.json().get('code') != 0:
    #     raise AssertionError("code is not 0 [error] http://{}/api/user/register".format(GATEWAY_HOST))
    return r


def _query_image():
    try:
        json_data = {
            "operationName": "null",
            "variables": {},
            "query": "query {image_list {file_name media_id format blob_uri type size duration thumb_uri trim_in trim_out res_w res_h aspect_w aspect_h}}"
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        }
        cookies = "sessionid=07p5tjnm5d4ldkfvjbepm20y44vcefhx"
        headers.setdefault("Cookie", cookies)

        r = requests.post('http://{}/graphqlex'.format(GATEWAY_HOST), json=json_data, headers=headers, timeout=10)
        print r.json()
    except requests.exceptions.ConnectTimeout:
        raise RuntimeError("接口请求超时")

    if r is None:
        raise RuntimeError("接口返回值为空 [error] http://{}/health/user/login".format(GATEWAY_HOST))
    return r.json()


def _delete_media(media_id):
    try:
        json_data = {
            "variables": {
                "media_id": media_id
            },
            "query": "mutation($media_id: String!) { delete_media(media_id: $media_id) { media_id } }"
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        }
        cookies = "sessionid=07p5tjnm5d4ldkfvjbepm20y44vcefhx"
        headers.setdefault("Cookie", cookies)

        r = requests.post('http://{}/graphqlex'.format(GATEWAY_HOST), json=json_data, headers=headers, timeout=10)
    except requests.exceptions.ConnectTimeout:
        raise RuntimeError("接口请求超时")

    if r is None:
        raise RuntimeError("接口返回值为空 [error] http://{}/health/user/login".format(GATEWAY_HOST))
    return r.json()


if __name__ == '__main__':
    #     print json_obj.json()
    image_list = _query_image()["data"]["image_list"]
    # print image_list
    for image in image_list:
        _delete_media(image["media_id"])
