# -*-coding:utf-8-*-s
from req.utils.sqldb import Database
from req.utils.ExcelUtil import MyExcelUtil

if __name__ == '__main__':
    mydb = Database('192.168.11.83', 3306, 'root', 'root', 'Wang_Test')
    m = MyExcelUtil(r"E:\work\python\UI-Project\req\upload\file\language.xls")
    for i in range(1, m.get_row_num()):
        en, de, es, fr, it, jp, pt = m.get_rowCol_data(i, 0).strip(), m.get_rowCol_data(i,
                                                                                        5).strip(), m.get_rowCol_data(i,
                                                                                                                      3).strip(), m.get_rowCol_data(
            i, 2).strip(), m.get_rowCol_data(i, 4).strip(), m.get_rowCol_data(i, 1).strip(), m.get_rowCol_data(i,
                                                                                                               6).strip()
        print en, de, es, fr, it, jp, pt
        sql = 'INSERT INTO pack9_multi_language(en, de, es, fr, it, jp, pt) VALUES("{}","{}","{}","{}","{}","{}","{}")'.format(
            en, de, es, fr, it, jp, pt)
        print sql
        mydb.execNoQuery(sql)

    # rows = mydb.execQuery(
    #     "SELECT name,SUM(testsRun),SUM(successes),SUM(failures),SUM(errors),date_format(create_time, '%Y%m%d') AS day  from webinterface_Reports where date_format(create_time, '%Y%m%d') = date_format(NOW(), '%Y%m%d') GROUP BY NAME ORDER BY name")
