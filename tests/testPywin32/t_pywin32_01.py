#!/usr/bin/python
#-*- coding:utf-8 -*-
# author:wanghao
# datetime:2018/12/13 14:23


import win32api,win32gui,win32con

def find_idxSubHandle(pHandle, winClass, index=0):
    """
                已知子窗口的窗体类名
                寻找第index号个同类型的兄弟窗口
    """
    assert type(index) == int and index >= 0
    handle = win32gui.FindWindowEx(pHandle, 0, winClass, None)
    while index > 0:
        handle = win32gui.FindWindowEx(pHandle, handle, winClass, None)
        index -= 1
    return handle

def find_subHandle(pHandle, winClassList):
    """
             递归寻找子窗口的句柄
    pHandle是祖父窗口的句柄
    winClassList是各个子窗口的class列表，父辈的list-index小于子辈
    """
    assert type(winClassList) == list
    if len(winClassList) == 1:
        return find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])
    else:
        pHandle = find_idxSubHandle(pHandle, winClassList[0][0], winClassList[0][1])
        return find_subHandle(pHandle, winClassList[1:])

# print win32api.GetCursorPos()
# hwnd = win32gui.FindWindow("Qt5QWindowIcon", None)
# print ("%x" % (hwnd))

hwnd = win32gui.FindWindow(None, "Wondershare Filmora9")
print ("%x" % (hwnd))
import time
time.sleep(2)

handle = win32gui.FindWindowEx(hwnd, None, None, None)
print ("%x" % (handle))

# editHandle = find_subHandle(hwnd, [("Edit", 0)])
# print ("%x" % (editHandle))