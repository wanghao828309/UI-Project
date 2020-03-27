#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql.cursors

class MysqldbHelper(object):
    """
                            操作mysql数据库，基本方法
    """
    def __init__(self , host="localhost", user="root", password="root", port=3306, db="test", charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.charset = charset
        self.cursorclass = cursorclass
        self.con = None
        self.cur = None
        # self.con = pymysql.connect(host=self.host, user=self.user, passwd=self.password, port=self.port, db=self.db,
        #                            charset=charset, cursorclass=cursorclass)
        try:
            self.con = pymysql.connect(host=self.host, user=self.user, passwd=self.password, port=self.port, db=self.db,charset = charset,cursorclass = cursorclass)
            # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
            self.cur = self.con.cursor()
        except:
            raise Exception("DataBase doesn't connect,close connectiong error;please check the db config.")

    def reConnect(self):
        try:
            self.con.ping()
        except:
            print "重新连接"
            self.con

    def close(self):
        """关闭数据库连接
 
        """
        if self.con:
            self.cur.close() 
            self.con.close()
         
    def executeSql(self,sql=''):
        """执行sql语句，针对读操作返回结果集
 
            args：
                sql  ：sql语句
        """
        try:
            self.cur.execute(sql)
            records = self.cur.fetchall()
            return records
        except pymysql.Error,e:
            error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print error
        finally:  
            self.cur.close()  
            self.con.close() 
 
    
    def executeSqlOne(self,sql=''):
        """执行sql语句，针对读操作返回结果集
 
            args：
                sql  ：sql语句
        """
        try:
            self.cur.execute(sql)
            records = self.cur.fetchone()
            return records
        except pymysql.Error,e:
            error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print error

    def executeCommentSqlOnce(self, sql=''):
        """执行sql语句，针对读操作返回结果集

            args：
                sql  ：sql语句
        """
        try:
            self.cur.execute(sql)
            self.cur.fetchone()
            self.con.commit()
        except pymysql.Error, e:
            self.con.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print error

    def executeCommentSql(self,sql=''):
        """执行sql语句，针对读操作返回结果集
 
            args：
                sql  ：sql语句
        """
        try:
            self.cur.execute(sql)
            self.cur.fetchone()
            self.con.commit()
        except pymysql.Error,e:
            self.con.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' %(e.args[0],e.args[1])
            print error
        finally:  
            self.cur.close()  
            self.con.close()
            
            
if __name__ == "__main__":
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    mydb = MysqldbHelper(host='192.168.11.83', port=3306, user='root', password='root',
                         db='autoplat')
    select_sql = 'select status from webinterface_Reports where `name` = (SELECT name FROM webinterface_Suite where id = "{}") ORDER BY id Desc LIMIT 1'.format(
        35)
    res = mydb.executeSqlOne(select_sql)
    print res["status"]
    if res["status"]:
        print 111

    # import json
    # mydb = MysqldbHelper(host='10.10.19.117', port=3306, user='root', password='root', db='filmora_es_admin')
    # # mydb = MysqldbHelper(host='127.0.0.1', port=3306, user='root', password='root', db='filmora')
    # result = mydb.executeSql('SELECT catname from wx_resource_category where catdir="sound_electronic" ')
    # for r in result:
    #     # mydb = MysqldbHelper(host='10.10.19.117', port=3306, user='root', password='root', db='filmora_es_admin')
    #     # print r["catname"]
    #     params = json.loads(r["catname"])
    #     # print params["en"]
    #     b = params["en"]
    #     params["en"] = params["en"].title()
    #     # print params["en"]
    #     # print params
    #     jsoninfo = json.dumps(params, ensure_ascii=False)
    #     # print jsoninfo
    #     # r["catname"] = jsoninfo
    #     # print str(r)
    #     # sql = "UPDATE wx_resource_category SET catname ='{\"en\":\"234234234\",\"fr\":\"\",\"de\":\"\",\"jp\":\"23423\",\"es\":\"\",\"it\":\"\",\"pt\":\"\"}' where catname LIKE '%\"234234234\"%'"
    #     sql = 'UPDATE wx_resource_category SET catname = {} where catname LIKE AAA\"%{}%\"BBB '.format(jsoninfo,b)
    #     print sql+";"
    #     # mydb.executeCommentSql(sql)
    #
    #

