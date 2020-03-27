#!/usr/bin/python
# -*- coding: UTF-8 -*-
from uiautomation import *

# nameControl = EditControl(searchDepth=8, Value='My Video')
# setControl = ButtonControl(searchDepth=8, Name='SETTINGS'.upper())
# exportControl = ButtonControl(searchDepth=8, Name='Export'.upper(), foundIndex=1)
completedControl = TextControl(searchDepth=4, SubName='Completed')
# closeControl = ButtonControl(searchDepth=4, Name='Close'.upper(), foundIndex=1)


class ExportPage():

    @staticmethod
    def inputName(name):
        nameControl = EditControl(searchDepth=7, Value='My Video',foundIndex=1)
        nameControl.Click()
        SendKeys('{ctrl}a')
        Win32API.PressKey(uiautomation.Keys.VK_BACK)
        nameControl.SendKeys(name)

    @staticmethod
    def clickFormat(format):
        ListItemControl(searchDepth=8, Name=format).Click()

    @staticmethod
    def clickSetting():
        setControl = ButtonControl(searchDepth=8, Name='SETTINGS'.upper())
        setControl.Click()

    @staticmethod
    def clickExport():
        exportControl = ButtonControl(searchDepth=8, Name='Export'.upper(), foundIndex=1)
        exportControl.Click()

    @staticmethod
    def v_completedText(time=50):
        closeControl = ButtonControl(searchDepth=4, Name='CLOSE', foundIndex=1)
        if uiautomation.WaitForExist(completedControl, time):
            print("Export:Completed")
            # closeControl = ButtonControl(searchDepth=8, Name='Close', foundIndex=1)
            closeControl.Click()
        else:
            print("Export:NO Completed")
            raise Exception("Export:NO Completed")

    @staticmethod
    def v_exportText(time=10):
        exportControl = PaneControl(searchDepth=2, Name='Export')
        if uiautomation.WaitForExist(exportControl, time):
            print("Export:exist")
            closeControl = ButtonControl(searchFromControl =exportControl ,searchDepth=5, foundIndex=1)
            closeControl.Click()
            return True
        else:
            print("Export:NO exist")
            return False
