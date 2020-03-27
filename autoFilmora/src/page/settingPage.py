#!/usr/bin/python
# -*- coding: UTF-8 -*-
from uiautomation import *
import time


def get_local(data):
    x = (int(data[0]) + int(data[2])) / 2
    y = (int(data[1]) + int(data[3])) / 2
    return (x, y)


class SettingPage():

    @staticmethod
    def get_videoValues():
        vals = [""]*8
        vals[0] = ComboBoxControl(searchDepth=3, foundIndex=1).CurrentValue()
        vals[1] = ComboBoxControl(searchDepth=3, foundIndex=2).CurrentValue()
        vals[2] = ComboBoxControl(searchDepth=3, foundIndex=3).CurrentValue()
        vals[3] = ComboBoxControl(searchDepth=3, foundIndex=4).CurrentValue()
        vals[4] = ComboBoxControl(searchDepth=3, foundIndex=5).CurrentValue()
        vals[5] = ComboBoxControl(searchDepth=3, foundIndex=6).CurrentValue()
        vals[6] = ComboBoxControl(searchDepth=3, foundIndex=7).CurrentValue()
        vals[7] = ComboBoxControl(searchDepth=3, foundIndex=8).CurrentValue()
        return vals

    @staticmethod
    def selectEncoder(encoder):
        encoderComboBox = ComboBoxControl(searchDepth=3, foundIndex=1)
        encoderComboBox.Select(encoder)

    @staticmethod
    def selectResolution(resolution):
        resolutionComboBox = ComboBoxControl(searchDepth=3, foundIndex=2)
        resolutionComboBox.Select(resolution)

    @staticmethod
    def selectFrameRate(frameRate):
        frameRateComboBox = ComboBoxControl(searchDepth=3, foundIndex=3)
        frameRateComboBox.Select(frameRate)

    @staticmethod
    def selectFrameRate2(frameRate):
        frameRateComboBox = ComboBoxControl(searchDepth=3, foundIndex=3)
        frameRateComboBox.Click()
        # print frameRateComboBox.BoundingRectangle
        ListItem = ListItemControl(searchFromControl=frameRateComboBox, foundIndex=2)
        # print ListItem.BoundingRectangle
        local = get_local(ListItem.BoundingRectangle)
        MoveTo(local[0], local[1])
        time.sleep(0.2)
        WheelDown(2)
        time.sleep(0.2)
        ListItemControl(searchFromControl=frameRateComboBox, Name=frameRate).Click()

    @staticmethod
    def selectVideoBitrate(videoBitrate):
        videoBitrateComboBox = ComboBoxControl(searchDepth=3, foundIndex=4)
        videoBitrateComboBox.Select(videoBitrate)

    @staticmethod
    def selectVideoBitrate2(videoBitrate):
        videoBitrateComboBox = ComboBoxControl(searchDepth=3, foundIndex=4)
        videoBitrateComboBox.Click()
        ListItem = ListItemControl(searchFromControl=videoBitrateComboBox, foundIndex=2)
        local = get_local(ListItem.BoundingRectangle)
        MoveTo(local[0], local[1])
        time.sleep(0.2)
        WheelDown(2)
        time.sleep(0.2)
        ListItemControl(searchFromControl=videoBitrateComboBox, Name=videoBitrate).Click()

    @staticmethod
    def selectAudioEncoder(audioEncoder):
        encoderComboBox = ComboBoxControl(searchDepth=3, foundIndex=5)
        encoderComboBox.Select(audioEncoder)

    @staticmethod
    def selectChannel(channel):
        resolutionComboBox = ComboBoxControl(searchDepth=3, foundIndex=6)
        resolutionComboBox.Select(channel)

    @staticmethod
    def selectSampleRate(sampleRate):
        frameRateComboBox = ComboBoxControl(searchDepth=3, foundIndex=7)
        frameRateComboBox.Select(sampleRate)

    @staticmethod
    def selectAudioBitrate(audioBitrate):
        audioBitrateComboBox = ComboBoxControl(searchDepth=3, foundIndex=8)
        audioBitrateComboBox.Select(audioBitrate)

    @staticmethod
    def clickDefault():
        defaultControl = ButtonControl(searchDepth=2, Name='DEFAULT Enter')
        defaultControl.Click()
        time.sleep(0.5)

    @staticmethod
    def clickOk():
        okControl = ButtonControl(searchDepth=2, Name='Ok'.upper())
        okControl.Click()

    @staticmethod
    def getPathValue():
        pathControl = EditControl(searchDepth=7, foundIndex=2)
        return pathControl.CurrentValue()

    @staticmethod
    def getFrameRateNum():
        ComboBoxControl(searchDepth=3, foundIndex=3).Click()
        num = len(ListControl(searchDepth=4, foundIndex=3).GetChildren())
        ComboBoxControl(searchDepth=3, foundIndex=3).Click()
        return num

    @staticmethod
    def getBitRateNum():
        ComboBoxControl(searchDepth=3, foundIndex=4).Click()
        num = len(ListControl(searchDepth=4, foundIndex=4).GetChildren())
        ComboBoxControl(searchDepth=3, foundIndex=4).Click()
        return num


if __name__ == '__main__':
    time.sleep(2)
    # c = RadioButtonControl(searchDepth=4, name="Better").GetLastChildControl()
    print [""]*8
    # print len(c)
    # for i in c:
    #     print i
