#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ConfigParser
import re


def del_headerr(path):
    content = open(path).read()
    content = re.sub(r"\xfe\xff", "", content)
    content = re.sub(r"\xff\xfe", "", content)
    content = re.sub(r"\xef\xbb\xbf", "", content)
    open(path, 'w').write(content)


class MyFileParserUtil(object):

    def __init__(self, config_file_path):
        self.path = config_file_path
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.path)

    def get_fileValue(self, section, options):
        try:
            value = self.cf.get(section, options)
        except:
            print ("获取的值不存在")
        else:
            print ("获取的【" + section + "】下  " + options + " 的值为：" + value)
            return value

    def get_option(self, section):
        try:
            option_list = self.cf.items(section)
            return option_list
        except:
            print ("获取的{} 不存在".format(section))

    def get_section(self):
        sections_list = self.cf.sections()
        return sections_list

    def add_fileValue(self, section, v_options, val):
        self.cf.add_section(section)
        for option in v_options:
            self.cf.set(section, option, val)

    def write_fileValue(self, section, v_options, val):
        self.cf.set(section, v_options, val)
        self.cf.write(open(self.path, "r+"))


if __name__ == '__main__':
    path = r"E:\work\python\UI-Project\req\upload\file\Resource_Online2.ini"
    # del_headerr(path)
    m = MyFileParserUtil(path)
    section = m.get_section()
    print section


