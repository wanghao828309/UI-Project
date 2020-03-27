#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest, platform
import time
# import HTMLTestRunner
from autoFilmora.src.utils import ExcelUtil
from autoFilmora.src.utils import mediaInfoUtil
from autoFilmora.src.case import filmora
from uiautomation import *


def decorator(func):
    def wrapper(*args, **kw):
        for i in range(3):
            try:
                Logger.ColorfulWrite("<Color=Cyan>" + str(i) + "</Color>  times again")
                r = func(*args, **kw)
                return r
            except Exception as err:
                Logger.ColorfulWrite('The one case fail by :%s' % err)
        raise Exception

    return wrapper


def get_AppAuto_path():
    pwd = os.getcwd()
    # print(pwd)
    path = pwd.split("autoFilmora")[0] + "autoFilmora"
    return path


XLS_WIN7_PATH = get_AppAuto_path() + "\\config\\autoCase_win7.xls"
XLS_WIN10_PATH = get_AppAuto_path() + "\\config\\autoCase_win10.xls"
PATH = ""


class Runner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        time.sleep(5)
        global PATH
        #         "Hook method for setting up class fixture before running tests in the class."
        #         thisWindow = GetConsoleWindow()
        Logger.ColorfulWrite('\nbegin <Color=Cyan>case</Color>\n')
        if platform.release() == "7":
            PATH = XLS_WIN7_PATH
        else:
            PATH = XLS_WIN10_PATH
        pass

    @classmethod
    def tearDownClass(cls):
        #         "Hook method for deconstructing the class fixture after running all tests in the class."
        Logger.ColorfulWrite("\n\n---------------------------------------end----------------------------------------")
        pass

    def setUp(self):
        Logger.ColorfulWrite("\n-------------setUp------------\n")
        pass

    def tearDown(self):
        pass

    def test_exportVideo(self):
        # time.sleep(0.1)
        Logger.ColorfulWrite("\n-------------test_exportVideo------------\n")
        excelUtil = ExcelUtil.MyExcelUtil(PATH)
        sheetName = excelUtil.get_sheet_names()
        j = -1
        for name in (sheetName):
            j = j + 1
            # val = mediaInfoUtil.conver_frame(name)
            # filmora.FilmoraRun().setFrameRate(val[0], val[1])
            if name not in ("GIF", "MP3"):
                for i in range(1, excelUtil.get_row_num(j)):
                    Logger.ColorfulWrite("-------------run:<Color=Cyan>" + str(i - 1) + "</Color>------------\n")
                    runmode = excelUtil.get_rowCol_data(i, 11, j)
                    try:
                        if (runmode.upper() == 'YES' or runmode.upper() == 'Y'):
                            filmora.FilmoraRun().exportCase(i, excelUtil.get_rowCol_data(i, 1, j),
                                                            excelUtil.get_rowCol_data(i, 2, j),
                                                            excelUtil.get_rowCol_data(i, 3, j),
                                                            excelUtil.get_rowCol_data(i, 4, j),
                                                            excelUtil.get_rowCol_data(i, 5, j),
                                                            excelUtil.get_rowCol_data(i, 6, j),
                                                            excelUtil.get_rowCol_data(i, 7, j),
                                                            excelUtil.get_rowCol_data(i, 8, j),
                                                            excelUtil.get_rowCol_data(i, 9, j),
                                                            excelUtil.get_rowCol_data(i, 10, j), j, PATH)
                            ExcelUtil.MyExcelUtil(PATH).write_rowNum_data(i, 11, ExcelUtil.MyExcelUtil.set_style(3), j,
                                                                          "N", "PASS")
                    except Exception as err:
                        Logger.ColorfulWrite('The one case fail by :%s' % err)
                        ExcelUtil.MyExcelUtil(PATH).write_data(i, 12, "FAIL:  %s" % err,
                                                               ExcelUtil.MyExcelUtil.set_style(2), j)

    # def test_exportGif(self):
    #     Logger.ColorfulWrite("\n-------------test_exportGif------------\n")
    #     excelUtil = ExcelUtil.MyExcelUtil(PATH)
    #     sheetName = excelUtil.get_sheet_names()
    #     j = -1
    #     for name in (sheetName):
    #         j = j + 1
    #         val = mediaInfoUtil.conver_frame(name)
    #         if name == "GIF":
    #             filmora.FilmoraRun().setFrameRate(val[0], val[1])
    #             for i in range(2, excelUtil.get_row_num(j)):
    #                 Logger.ColorfulWrite("-------------run:<Color=Cyan>" + str(i - 1) + "</Color>------------\n")
    #                 runmode = excelUtil.get_rowCol_data(i, 7, j)
    #                 try:
    #                     if (runmode.upper() == 'YES' or runmode.upper() == 'Y'):
    #                         filmora.FilmoraRun().exportGif(i, excelUtil.get_rowCol_data(i, 1, j),
    #                                                        excelUtil.get_rowCol_data(i, 2, j),
    #                                                        excelUtil.get_rowCol_data(i, 3, j),
    #                                                        excelUtil.get_rowCol_data(i, 4, j),
    #                                                        excelUtil.get_rowCol_data(i, 5, j),
    #                                                        excelUtil.get_rowCol_data(i, 6, j), j)
    #                         ExcelUtil.MyExcelUtil(PATH).write_rowNum_data(i, 7, ExcelUtil.MyExcelUtil.set_style(3), j,
    #                                                                       "N", "PASS")
    #                 except Exception as err:
    #                     Logger.ColorfulWrite('The one case fail by :%s' % err)
    #                     ExcelUtil.MyExcelUtil(PATH).write_data(i, 8, "FAIL:  %s" % err,
    #                                                            ExcelUtil.MyExcelUtil.set_style(2), j)
    #
    # def test_exportMP3(self):
    #     Logger.ColorfulWrite("\n-------------test_exportMP3------------\n")
    #     excelUtil = ExcelUtil.MyExcelUtil(PATH)
    #     sheetName = excelUtil.get_sheet_names()
    #     j = -1
    #     for name in (sheetName):
    #         j = j + 1
    #         val = mediaInfoUtil.conver_frame(name)
    #         if name == "MP3":
    #             filmora.FilmoraRun().setFrameRate(val[0], val[1])
    #             for i in range(2, excelUtil.get_row_num(j)):
    #                 Logger.ColorfulWrite("-------------run:<Color=Cyan>" + str(i - 1) + "</Color>------------\n")
    #                 runmode = excelUtil.get_rowCol_data(i, 7, j)
    #                 try:
    #                     if (runmode.upper() == 'YES' or runmode.upper() == 'Y'):
    #                         filmora.FilmoraRun().exportMP3(i, excelUtil.get_rowCol_data(i, 1, j),
    #                                                        excelUtil.get_rowCol_data(i, 2, j),
    #                                                        excelUtil.get_rowCol_data(i, 3, j),
    #                                                        excelUtil.get_rowCol_data(i, 4, j),
    #                                                        excelUtil.get_rowCol_data(i, 5, j),
    #                                                        excelUtil.get_rowCol_data(i, 6, j), j)
    #                         ExcelUtil.MyExcelUtil(PATH).write_rowNum_data(i, 7, ExcelUtil.MyExcelUtil.set_style(3), j,
    #                                                                       "N", "PASS")
    #                 except Exception as err:
    #                     Logger.ColorfulWrite('The one case fail by :%s' % err)
    #                     ExcelUtil.MyExcelUtil(PATH).write_data(i, 8, "FAIL:  %s" % err,
    #                                                            ExcelUtil.MyExcelUtil.set_style(2), j)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    Test=[]
    Test.append("test_exportVideo")
    for i in Test:
        print(i)
        suite.addTest(Runner(i))
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
