#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:wanghao
# datetime:2019/9/12 10:42

from req.utils.FileParserUtil import MyFileParserUtil
import os, shutil

path = r"E:\work\python\UI-Project\req\upload\file\Resource_Online2.ini"
m = MyFileParserUtil(path)


def get_option(section):
    option_list = m.get_option(
        section)
    for tuple in option_list:
        yield tuple[0]


def remove_dir(path):
    dirs = os.listdir(path)
    print dirs
    sections = m.get_section()
    for section in sections:
        k_options = get_option(section)
        for k_option in k_options:
            for dir_name in dirs:
                # print type(k_option)
                # print k_option.lower(),dir_name.lower()
                if section + "_" + k_option.lower() == dir_name.lower():
                    print k_option.lower(), dir_name.lower()
                    child_path = os.path.join(path, dir_name)
                    child_dirs = os.listdir(child_path)
                    for child_dir_name in child_dirs:
                        child_child_path = os.path.join(child_path, child_dir_name)
                        # print child_child_path
                        if os.path.isdir(child_child_path):
                            shutil.rmtree(child_child_path)


def remove_Font(path):
    dirs = os.listdir(path)
    print dirs
    for dir_name in dirs:
        if "1_" in dir_name:
            child_path = os.path.join(path, dir_name)
            child_dirs = os.listdir(child_path)
            for child_dir_name in child_dirs:
                child_child_path = os.path.join(child_path, child_dir_name)
                # print child_child_path
                if "Font" in child_dir_name:
                    print child_child_path
                    shutil.rmtree(child_child_path)


if __name__ == '__main__':
    remove_dir(r"C:\Users\ws\Desktop\DefaultPackage")
    remove_Font(r"C:\Users\ws\Desktop\DefaultPackage")
