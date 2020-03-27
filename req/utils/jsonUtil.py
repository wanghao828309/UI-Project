#!/usr/bin/python
# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         jsonUtil
# Description:  
# Author:       wanghao
# Date:         2018/11/8
#-------------------------------------------------------------------------------
import json

def save_jsonFile(dict,f):
    with open(f, "w") as f:
        json.dump(dict,f)

def read_jsonFile(f):
    with open(f, 'r') as load_f:
        load_dict = json.load(load_f)
        print(load_dict)
        return load_dict


dict = read_jsonFile(r"C:\Users\ws\Desktop\record.json")

for k,v in dict.items():
    print k,v