#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xlrd,xlwt
from xlutils.copy import copy
import os




# filePath=os.getcwd()+"\\Filmora.xls"
# print(filePath)
class MyExcelUtil(object):
    '''
    classdocs
    '''


    def __init__(self,path):
        '''
        Constructor
        '''
        self.filePath = path
        self.workbook = xlrd.open_workbook(path, formatting_info=True)
#         self.sheet=self.workbook.sheet_by_index(0)

    def get_sheet_names(self):
        return self.workbook.sheet_names()
        
    def get_row_num(self,index=0):
        return self.workbook.sheet_by_index(index).nrows

    def get_row_num2(self,name):
        return self.workbook.sheet_by_name(name).nrows

    def get_col_num(self,index=0):
        return self.workbook.sheet_by_index(index).ncols
    
    def get_rowCol_data(self,rowNum,colNum,index=0):
        return self.workbook.sheet_by_index(index).cell_value(rowNum,colNum)
    
    def get_Colnum_data(self,rowNum,data,index=0):
        cols = self.workbook.sheet_by_index(index).col_values(rowNum)
        for i in range(len(cols)):
            if cols[i] == data:
                return i
            
    
    def write_data(self,rowNum,colNum,P_F,style,index=0):
        """写入Excel"""
        wb = copy(self.workbook)
        s = wb.get_sheet(index)
        #设置样式
        s.write(rowNum, colNum,P_F,style)
        wb.save(self.filePath)
        return wb

    def write_rowNum_data(self,rowNum,colNum,style,index=0,*rowData):
        """写入Excel"""
        wb = copy(self.workbook)
        s = wb.get_sheet(index)
        #设置样式
        for row in rowData:
            s.write(rowNum,colNum,row,style)
            colNum=colNum+1
        wb.save(self.filePath)
        return wb

    def write_rowNum_data2(self,rowNum,colNum,style,index,rowData):
        """写入Excel"""
        wb = copy(self.workbook)
        s = wb.get_sheet(index)
        #设置样式
        for row in rowData:
            s.write(rowNum,colNum,row,style)
            colNum=colNum+1
        wb.save(self.filePath)
        return wb
    
    @staticmethod
    def set_style(color):
        """写入数据库的样式
        0.黑色
        1.白色
        2.红色
        3.绿色
        4.紫色
        5.黄色
        """

        font = xlwt.Font()
        font.name = "Times New Roman"
        font.colour_index = color
        style = xlwt.XFStyle()
        style.font = font
        return  style

    def get_sheet_row_data(self,colNum):
        data = []
        index = -1
        for name in self.workbook.sheet_names():
            index = index+1
            for i in range(1, self.workbook.sheet_by_index(index).nrows):
                rowVal = self.workbook.sheet_by_index(index).cell_value(i,colNum)
                if rowVal is not None and rowVal != "":
                    data.append(rowVal)
        return data
    
    
if __name__ == '__main__':
    pass
    exlPath = r"C:\Users\ws\Desktop\22.xls"
    m = MyExcelUtil(exlPath)
    for i in range(1, m.get_row_num(0)):
        print m.get_rowCol_data(i, 0)
        MyExcelUtil(exlPath).write_data(i, 0, m.get_rowCol_data(i, 0)+"_new",
                                        MyExcelUtil.set_style(2))
    # for i in MyExcelUtil(r"E:\work\python\UI-Project\req\fileup2.xls").get_sheet():
    #     print i

    
    
    