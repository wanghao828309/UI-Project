#!/usr/bin/python
# -*- coding: UTF-8 -*-
from uiautomation import *

paneControl = PaneControl(searchDepth=2, ClassName ='Qt5QWindowIcon')
fileControl = MenuItemControl(searchFromControl=paneControl ,searchDepth=4, Name='File')
proSetControl = MenuItemControl(Name='Project Settings')
exportControl = ButtonControl(Name='EXPORT')


def get_local(data):
    x = (int(data[0]) + int(data[2])) / 2
    y = (int(data[1]) + int(data[3])) / 2
    return (x, y)


class HomePage():

    @staticmethod
    def clickFile():
        fileControl.Click()

    @staticmethod
    def clickProSet():
        proSetControl.Click()

    @staticmethod
    def clickOk():
        okControl = ButtonControl(searchDepth=3, Name='OK Enter')
        okControl.Click()

    @staticmethod
    def clickEXPORT():
        exportControl.Click()

    @staticmethod
    def selectResolution(resolution):
        resolutionList = ComboBoxControl(searchDepth=5, foundIndex=1)
        resolutionList.Select(resolution)

    @staticmethod
    def selectResolution2(resolution):
        resolutionList = ComboBoxControl(searchDepth=5, foundIndex=1)
        resolutionList.Click()
        ListItem = ListItemControl(searchFromControl=resolutionList, foundIndex=2)
        local = get_local(ListItem.BoundingRectangle)
        MoveTo(local[0], local[1])
        time.sleep(0.2)
        WheelDown(2)
        time.sleep(0.2)
        ListItemControl(searchFromControl=resolutionList, Name=resolution).Click()

    @staticmethod
    def selectFrameRate(frameRate):
        frameRateList = ComboBoxControl(searchDepth=5, foundIndex=2)
        frameRateList.Select(frameRate)


if __name__ == '__main__':
    time.sleep(2)
    # HomePage.clickFile()
    # HomePage.clickProSet()
    # HomePage.selectFrameRate("24 fps")
    HomePage.clickOk()
    # HomePage.clickEXPORT()
