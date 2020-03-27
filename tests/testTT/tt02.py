#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json,time
import xmltodict
import platform
#定义xml转json的函数
def xmltojson(xml_path):
    #获取xml文件
    xml_file = open(xml_path, 'r')
    #读取xml文件内容
    xml_str = xml_file.read()
    #parse是的xml解析器
    xmlparse = xmltodict.parse(xml_str)
    #json库dumps()是将dict转化成json格式，loads()是将json转化成dict格式。
    #dumps()方法的ident=1，格式化json
    jsonstr = json.dumps(xmlparse,indent=1)
    print(jsonstr)
CONSTANT = 0
def modifyConstant():
        global CONSTANT
        print CONSTANT
        CONSTANT += 1
        return


if __name__ == '__main__':
    # modifyConstant()
    # print CONSTANT

    timestamp = 1535357428.654038

    #转换成localtime
    time_local = time.localtime(timestamp)
    #转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)

    print dt

