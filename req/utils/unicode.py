#!/usr/bin/python
#-*- coding:utf-8 -*-
# author:wanghao
# datetime:2019/8/28 13:50
def unicode_decode(val):
    return val.decode('unicode-escape')




a = {"code":10501,"message":"[\u53d1\u7968\u5e73\u53f0] \u63a5\u53e3\u8fd4\u56de\u7684\u6570\u636e\u6709\u8bef","data":[]}
print unicode_decode(a["message"])