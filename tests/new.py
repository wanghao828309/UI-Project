#!/usr/bin/env python
# coding: utf-8
import cv2, time
from PIL import Image, ImageGrab
import numpy as np
from uiautomation import *


def test01():
    bbox = (100, 834, 1908 + 1, 940 + 1)
    im = ImageGrab.grab(bbox)
    # src = cv2.imread(im)
    arr = np.array(im)
    roi = arr[..., ::-1]
    # cv2.findNonZero()
    cv2.namedWindow("input", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("input", roi)
    """
    提取图中的红色部分
    """
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    low_hsv = np.array([78, 43, 46])
    high_hsv = np.array([99, 255, 255])
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
    # ret, thresh = cv2.threshold(hsv, 127, 255, 0)
    # print cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_val, max_val, min_indx, max_indx = cv2.minMaxLoc(hsv)
    print(min_val, max_val, min_indx, max_indx)
    cv2.imshow("test", mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test02(im):
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    low_hsv = np.array([78, 43, 46])
    high_hsv = np.array([99, 255, 255])
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
    min_val, max_val, min_indx, max_indx = cv2.minMaxLoc(mask)
    return (min_val, max_val, min_indx, max_indx)


def gui_findTga(tga):
    st = time.time()
    im = ImageGrab.grab()
    arr = np.array(im)
    temp = cv2.imread(tga)
    # x1 = 0
    # y1 = 0
    # x2 = 1920
    # y2 = 1080
    # arr = arr[y1:y2,x1:x2]
    roi = arr[..., ::-1]
    # roi=arr[200:270,1100:1350]

    temp_h, temp_w, _ = temp.shape
    print temp.shape
    match_score = cv2.matchTemplate(roi, temp, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(match_score)
    print max_loc
    x = max_loc[0] + int(temp_w / 2)
    y = max_loc[1] + int(temp_h / 2)
    print("match_score : %f" % max_val)
    print("Used time %f seconds\n" % (time.time() - st))
    print(x, y)
    assert isinstance(max_val, object)
    return (x, y, max_val)


def gui_Click(imgpath):
    """通过图标对比识别元素，并点击"""
    res = gui_findTga(imgpath)
    if res[2] > 0.9:
        p_x = res[0]
        p_y = res[1]
        MoveTo(p_x, p_y, 1.5)
    else:
        print("Can not find {}".format(imgpath))


from collections import OrderedDict


def extract_const_attributes(cls):
    """Return dict with constants attributes and values in the class(e.g. {'VAL1': 1, 'VAL2': 2})
    Args:
        cls (type): Class to be extracted constants
    Returns:
        OrderedDict: dict with constants attributes and values in the class
    """
    print vars(cls).items()
    return OrderedDict(
        [(attr, value) for attr, value in vars(cls).items() if not callable(getattr(cls, attr)) and attr.isupper()])


class b:
    TT = 123

    def test(self):
        print 11

+201
if __name__ == '__main__':
    # time.sleep(2)

    i ="0"
    if True:
        i=1
    else:
        i=2
    print i

