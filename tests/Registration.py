# coding=utf-8

import requests
import re, string, time
from requests_toolbelt.multipart.encoder import MultipartEncoder

filepath = "C:/Users/WS/Downloads/"


def uploadfile(filename, filepath):
    url = "http://wos-upload.wondershare.cn/upload?path=rms&from=2"
    headers = {"accept": "application/json", "Content-Length": "309047", "Host": "wos-upload.wondershare.cn",
               "Connection": "Keep-Alive", "Accept-Encoding": "gzip", "User-Agent": "okhttp/3.6.0"}

    multipart_encoder = MultipartEncoder(
        fields={
            'file': (filename, open(filepath, 'rb'),"multipart/form-data"),
        },
        boundary="1906af58-ed16-4699-bd0c-72109088f5ee"
    )
    headers['Content-Type'] = multipart_encoder.content_type
    # 发送post请求
    r = requests.post(url, data=multipart_encoder, headers=headers)
    print(r.text)


def Get_buginfo(name, sex, phone, email, positionsId, reason, effectiveTime, attachName, attachUrl, attachId):
    url = "https://gw.wondershare.cn/applicant/add-applicant-info"
    headers = {'accept-language': "zh-CN=",
               "authorization": "Basic MTcwNDI3Mjg6MWI4N2JiMjVjNDE0MzU4MThlYTJhMjQ4Yjc5MWNmNTg=",
               "access-control-allow-origin": "http://localhost",
               "Content-Type": "application/x-www-form-urlencoded; charset=utf-8", "Content-Length": "523",
               "Host": "gw.wondershare.cn", "Connection": "Keep-Alive", "Accept-Encoding": "gzip",
               "User-Agent": "okhttp/3.6.0"}
    body = '{"name":' + name + ',"sex":' + sex + ',"phone":' + phone + ',"email":' + email + ',"wx":null,"depId":"2221","sourceId":3,"positionsId":' + positionsId + ',"applicantBadge":"17042728","recommendReason":' + reason + ',"recommended":null,"effectiveTime":' + effectiveTime + ',"attachName":' + attachName + ',"attachUrl":' + attachUrl + ',"id":"","hrbpBadge":"17032645","attachId":' + attachId + '}'

    # 发送post请求
    r = requests.post(url, data=body, headers=headers, verify=False)
    print(r.text)

    # issueKeys = re.findall('issueKeys":(.*?),"jiraHasIssues', r.text)[0]
    # return issueKeys


if __name__ == '__main__':
    name = "李振平"
    sex = 1
    phone = "18814306675"
    email = "lizhenping@yeah.net"
    positionsId = 14648
    reason = "测试技术比较全面，系统测试和自动化是都有相应经验，熟悉音视频测试知识和测试方法"
    effectiveTime = "2020-02-19"
    # attachName =
    # attachUrl =
    # attachId =

    uploadfile("11.pdf", r"C:\Users\ws\Desktop\register\11.pdf")
