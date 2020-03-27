import subprocess
from uiautomation import *

def test_start(t):
    filmoraWindow = PaneControl(searchDepth=1, ClassName='Qt5QWindowIcon')
    if not filmoraWindow.Exists(0, 0):
        subprocess.Popen('C:\Program Files\Wondershare\Filmora 9\Wondershare Filmora 9.exe')
    else:
        print "filmora is open"

    ButtonControl(Name="Wondershare Filmora 9").Click()

    filmoraWindow.SetFocus()
    if WaitForExist(filmoraWindow,20):
    # if filmoraWindow.Exists(0, 0):
        print "filmora is open"
        filmoraWindow.SetFocus()
        EditControl(searchFromControl=filmoraWindow, searchDepth=2, foundIndex=1).Click()
        SendKeys('2')
        # EditControl(searchFromControl=filmoraWindow, searchDepth=2, foundIndex=1).SetValue("2")
    #     ButtonControl(searchFromControl=filmoraWindow,searchDepth=2, foundIndex=4).Click()
    #     time.sleep(t)
    #     pan = PaneControl(searchDepth=2, ClassName='Qt5QWindowIcon')
    #     ButtonControl(searchFromControl=pan,searchDepth=4, foundIndex=4).Click()
    # else:
    #     print "filmoraWindow is not exist"


test_start(5)