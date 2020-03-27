#!/usr/bin/python
# -*- coding: UTF-8 -*-

from req.utils.ExcelUtil import MyExcelUtil
from req.utils.mysqldbUtil import MysqldbHelper



def conver_to_mysql(exlPath):
    mydb = MysqldbHelper(host='192.168.11.83', port=3306, user='root', password='root', db='Wang_Test')
    m = MyExcelUtil(exlPath)
    for j in range(0, 1):
        for i in range(1, m.get_row_num(j)):
            # categoryExcel = m.get_rowCol_data(i, 0, j)
            enExcel = m.get_rowCol_data(i, 0, j)
            # print enExcel
            # print unicode(enExcel, "utf8")
            jpExcel = m.get_rowCol_data(i, 1, j)
            deExcel = m.get_rowCol_data(i, 2, j)
            frExcel = m.get_rowCol_data(i, 3, j)
            ptExcel = m.get_rowCol_data(i, 4, j)
            esExcel = m.get_rowCol_data(i, 5, j)
            itExcel = m.get_rowCol_data(i, 6, j)
            # print enExcel, frExcel, deExcel, esExcel, itExcel, ptExcel, jpExcel
            sql = 'INSERT INTO pack9_multi_language(en,fr,de,es,it,pt,jp) VALUES (\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")'.format(
                    enExcel, frExcel, deExcel, esExcel, itExcel, ptExcel, jpExcel)
            print sql
            mydb.executeCommentSqlOnce(sql)


if __name__ == "__main__":

    conver_to_mysql(r"E:\work\python\UI-Project\req\upload\file\tran_language.xls")
