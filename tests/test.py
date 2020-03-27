#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:wanghao
# datetime:2019/8/27 16:56

aa = "123456"
lls=[1,2,3,4,5]
s = 'hEllo pYthon 123'


def test01(strs):
    res=""
    strs_len = len(strs)
    for i,s in enumerate(strs):
        res+= strs[strs_len-i-1]
    return res

def test02(strs):
    return "".join(reversed(strs))

def test03(strs):
    return aa[::-1]

#排序
def test04(lists):
    return sorted(lists,reverse=True)


def test05(lists):
    l_len=len(lists)
    for i in range(l_len):
        for j in range(l_len-i-1):
            if lists[j]<lists[j+1]:
                lists[j],lists[j+1]=lists[j+1],lists[j]

    return lists


#字符串大小写转化
def test06(s):
    s_list=[]
    for i in s:
        if i.isupper():
            s_list.append(i.lower())
        elif i.islower():
            s_list.append(i.upper())
        else:
            s_list.append(i)
    # print s_list
    return "".join(s_list)

import re
def test07(s):
    s_list = []
    p_low = re.compile("[a-z]")
    p_up = re.compile("[A-Z]")
    for i in s:
        low_f = re.findall(p_low,i)
        up_f = re.findall(p_up, i)
        if len(low_f)>0:
            s_list.append(i.upper())
        elif len(up_f) >0:
            s_list.append(i.lower())
        else:
            s_list.append(i)
    return "".join(s_list)


if __name__ == '__main__':
    print test07(s)

