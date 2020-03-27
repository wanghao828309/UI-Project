#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
class MyGetPathUtil(object):

    
    
    @staticmethod
    def get_AppAuto_path():
        pwd = os.getcwd()
#         path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
        path = pwd.split("UI-Project")[0]+"UI-Project"
        return path
    
    @staticmethod
    def get_file_name(path):
        name = path.split("\\")[-1].split(".")[0]
#         print name
        return name
    
if __name__ == '__main__':
    
    # filePath=MyGetPathUtil.get_AppAuto_path()+"\\config\\\yaml2\\loginModel\\registered_loginSucc.yaml"
    print MyGetPathUtil.get_AppAuto_path()
    # print os.path.abspath(".")