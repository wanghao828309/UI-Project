#!/usr/bin/python
# -*- coding: UTF-8 -*-

data = [1, 2, 3]
data2 = [1, 2, 3]

# for i,i2 in zip(data,data2):
#     print(i)


a = 0.11
b = 0.110

# print abs(b-a)
#
# def foo(s):
#     n = int(s)
#     assert n != 0, 'n is zero!123'
#     return 10 / n
#
# try:
#     foo('0')
# except Exception as err:
#     print(err)


import base64
import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

def base64UrlEncode(s):
    data = base64.b64encode(s)
    res = data.replace("+", "-")
    res = res.replace("/", "_")
    res = res.replace("=", "")
    return res


def base64UrlDecode(s):
    res = s.replace("-", "+")
    res = res.replace("_", "/")
    res = base64.b64decode(res)
    return res


class prpcrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        if (count % length != 0):
            add = length - (count % length)
        else:
            add = 0
        text = text + ('\0' * add)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')


print base64UrlEncode("我是字符串")
print base64UrlDecode("5oiR5piv5a2X56ym5Liy")
