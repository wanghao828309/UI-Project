#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:wanghao
# datetime:2018/12/17 14:06

from uiautomation import *


parent = ToolBarControl(Name="运行应用程序")
if WaitForExist(parent,2):
    print parent.Handle
print "hello"