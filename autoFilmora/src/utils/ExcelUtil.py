#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xlrd,xlwt
from xlutils.copy import copy
import os


class MyGetPathUtil(object):
    @staticmethod
    def get_AppAuto_path():
        pwd = os.getcwd()
        # print(pwd)
        path = pwd.split("autoFilmora")[0] + "autoFilmora"
        return path

    @staticmethod
    def get_file_name(path):
        name = path.split("\\")[-1].split(".")[0]
        return name


class MyExcelUtil(object):
    '''
    classdocs
    '''

    def __init__(self, path):
        '''
        Constructor
        '''
        self.filePath = path
        self.workbook = xlrd.open_workbook(path, formatting_info=True)


    def get_sheet_names(self):
        return self.workbook.sheet_names()

    def get_row_num(self, index=0):
        return self.workbook.sheet_by_index(index).nrows

    def get_row_num2(self, name):
        return self.workbook.sheet_by_name(name).nrows

    def get_col_num(self, index=0):
        return self.workbook.sheet_by_index(index).ncols

    def get_rowCol_data(self, rowNum, colNum, index=0):
        return self.workbook.sheet_by_index(index).cell_value(rowNum, colNum)

    def get_Colnum_data(self, rowNum, data, index=0):
        cols = self.workbook.sheet_by_index(index).col_values(rowNum)
        for i in range(len(cols)):
            if cols[i] == data:
                return i

    def write_data(self, rowNum, colNum, P_F, style, index=0):
        """写入Excel"""
        wb = copy(self.workbook)
        s = wb.get_sheet(index)
        # 设置样式
        s.write(rowNum, colNum, P_F, style)
        wb.save(self.filePath)
        return wb

    def write_rowNum_data(self, rowNum, colNum, style, index=0, *rowData):
        """写入Excel"""
        wb = copy(self.workbook)
        s = wb.get_sheet(index)
        # 设置样式
        for row in rowData:
            s.write(rowNum, colNum, row, style)
            colNum = colNum + 1
        wb.save(self.filePath)
        return wb

    @staticmethod
    def set_style(color):
        """写入数据库的样式"""
        font = xlwt.Font()
        font.name = "Times New Roman"
        font.colour_index = color
        style = xlwt.XFStyle()
        style.font = font
        return style


if __name__ == '__main__':
    pass
    print (MyExcelUtil().get_rowCol_data(2,2))
    print (MyExcelUtil().get_row_num())
    m = MyExcelUtil()
    # for i in range(3,9):
    #     m.write_data(i, 12, "PASS", MyExcelUtil.set_style(3))
#     a=MyExcelUtil().get_Colnum_data(1,"test_registered_loginSucc")
#     MyExcelUtil().write_data(2,12,"FAIL", MyExcelUtil.set_style(2))
#     print MyExcelUtil().get_Colnum_data(1,"test_registered_loginSucc1")
#     max = (a if a is not None else 2)
#     print max
#     if a is None:
#         raise Exception("test_unregistered_loginSucc不在excel所在的列中")
    
    
    