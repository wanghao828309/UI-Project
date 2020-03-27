#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
WONDERSHARE_HOST = "filmoraoa.wondershare.com"
def get_token():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        "referer": "filmoraoa.wondershare.com",
        "Cookie":"tp3_sessionid=v5fegqeg8r98q3jbe0afbs9lo3"
    }
    r = requests.get('http://{}/File/getUploadToken.html'.format(WONDERSHARE_HOST), headers=headers)
    if r.status_code != 200:
        print(r.status_code)
        raise AssertionError("status_code is not 200 [error] http://{}/File/getUploadToken.html".format(WONDERSHARE_HOST))
    else:
        return r.json()["data"]


print get_token()