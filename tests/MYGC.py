# -*- coding: utf-8 -*-
import subprocess
from uiautomation import *
import time
import cv2
import numpy as np
from PIL import Image, ImageGrab



def gui_findTga(tga):
    st=time.time()
    im=ImageGrab.grab()
    arr=np.array(im)
    temp=cv2.imread(tga)
    # x1 = 0
    # y1 = 0
    # x2 = 1920
    # y2 = 1080
    # arr = arr[y1:y2,x1:x2]
    roi=arr[...,::-1]
    # roi=arr[200:270,1100:1350]

    temp_h, temp_w, _= temp.shape
    match_score=cv2.matchTemplate(roi, temp, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc=cv2.minMaxLoc(match_score)

    x=max_loc[0]+int(temp_w/2)
    y=max_loc[1]+int(temp_h/2)
    print("match_score : %f"%max_val)
    print("Used time %f seconds\n"%(time.time()-st))
    print(x,y)
    assert isinstance(max_val,object)
    return (x, y,max_val)


def gui_Click(imgpath):
    """通过图标对比识别元素，并点击"""
    res = gui_findTga(imgpath)
    if res[2] > 0.9:
        p_x = res[0]
        p_y = res[1]
        Click(p_x, p_y, 1.5)
    else:
        print("Can not find {}".format(imgpath))


def gui_SendKeys(imgpath,content):
    """"通过图标对比识别元素，并输入内容"""
    res = gui_findTga(imgpath)
    if res[2] > 0.9:
        p_x = res[0]
        p_y = res[1]
        Click(p_x, p_y, 1.5)
        SendKeys(content)
    else:
        print("Can not find {}".format(imgpath))

def gui_Assert(imgpath):
    """"通过图标对比识别元素，判断是否出现指定图片"""
    res = gui_findTga(imgpath)
    if res[2] > 0.9:
        print("Can find {}".format(imgpath))
    else:
        raise Exception("Can not find {}".format(imgpath))



if __name__ == '__main__':

    #打开Filmora9
    subprocess.Popen('C:\Program Files\Wondershare\Filmora9\Wondershare Filmora9.exe')
    # subprocess.Popen(r'C:\Program Files\Wondershare\喵影工厂\Wondershare Filmora9.exe')
    homepage = PaneControl(searchDepth=1, ClassName='Qt5QWindowIcon')
    import time
    time.sleep(5)
    if WaitForExist(homepage, 30):
        gui_Click(r"C:\Users\ws\Desktop\image\1.png")
        # newproject = ButtonControl(searchFromControl=homepage, searchDepth=2, foundIndex=3)
        # newproject.Click()
    #
    # time.sleep(3)
    # if gui_findTga("D:\opencv\mylogo.jpg")[2] < 0.9:
    #
    #     homepage = PaneControl(searchDepth=1, ClassName='Qt5QWindowIcon', Name=u'喵影工厂')
    #     ButtonControl(searchFromControl=homepage, searchDepth=4, foundIndex=1).Click()
    #
    #     time.sleep(1)
    #     ButtonControl(searchFromControl=homepage, Name=u"退出程序 Enter").Click()
    #
    # else:
    #     gui_SendKeys(r"D:\opencv\username.jpg","15889752195")
    #     gui_SendKeys(r"D:\opencv\password.jpg","123456")
    #     gui_Click(r"D:\opencv\login.jpg")
    #     gui_Click(r"D:\opencv\xinxizhongxin-gb.jpg")


