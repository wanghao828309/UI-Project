#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:wanghao
# datetime:2019/3/19 14:35
import requests

WONDERSHARE_HOST = "account.wondershare.cn"
COOKIES = "thinkphp_show_page_trace=0|0; UM_distinctid=169c70a3a22b05-02ba517d49804c-5f123917-1fa400-169c70a3a23b3f; ws_lang=zh-cn; PHPSESSID=uboi0l1fu9iibs6tnuirnjv3u2"


def get_email_code(email):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        "referer": "https://app.bugsplat.com/v2/summary"
    }
    cookies = {
        'Cookie': COOKIES
    }

    data = {"search_arr[0][msg_type]": "", "search_arr[0][email]": "", "search_arr[0][now_page]": "1",
            "search_arr[0][limit_length]": "15", "search_arr[0][startDate]": "发送时间",
            "search_arr[0][endDate]": ""}
    r = requests.post(
        'http://{}/admin/usermanage.user_email/getData'.format(
            WONDERSHARE_HOST), data=data, headers=headers, cookies=cookies, verify=False)
    if r.status_code != 200:
        raise AssertionError(
            "status_code is not 200 [error] http://{}/admin/usermanage.user_email/getData".format(
                WONDERSHARE_HOST))
    elif r.json()["status"] == "0":
        raise AssertionError('r.json()["status"] !=0')
    else:
        return r.json()["data"]["list"][0]["body"]


if __name__ == '__main__':
    print get_email_code("770834094@qq.com")
    pass
