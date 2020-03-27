# -*-coding:utf-8-*-s
# mysql和sqlserver的库
import pymysql
from DBUtils.PooledDB import PooledDB
import sys
reload(sys)
sys.setdefaultencoding("utf8")


class Database:
    def __init__(self, *db):
        if len(db) == 5:
            # mysql数据库
            self.host = db[0]
            self.port = int(db[1])
            self.user = db[2]
            self.pwd = db[3]
            self.db = db[4]
        self._CreatePool()

    def _CreatePool(self):
        if not self.db:
            raise NameError + "没有设置数据库信息"
        self.Pool = PooledDB(creator=pymysql, mincached=2, maxcached=5, maxshared=3, maxconnections=6, blocking=True,
                             host=self.host, port=self.port, \
                             user=self.user, password=self.pwd, database=self.db, charset="utf8")

    def _Getconnect(self):
        self.conn = self.Pool.connection()
        cur = self.conn.cursor()
        if not cur:
            raise ("数据库连接不上")
        else:
            return cur

    # 查询sql
    def execQuery(self, sql, count=0):
        cur = self._Getconnect()
        cur.execute(sql)
        if count == 1:
            res = cur.fetchone()
        else:
            res = cur.fetchall()
        cur.close()
        self.conn.close()
        return res

    # 非查询的sql
    def execNoQuery(self, sql):
        cur = self._Getconnect()
        try:
            cur.execute(sql)
            # self.cur.fetchone()
            self.conn.commit()
        except pymysql.Error, e:
            self.conn.rollback()
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print error
        finally:
            cur.close()
            self.conn.close()


if __name__ == '__main__':
    mydb = Database('192.168.11.83', 3306, 'root', 'root', 'autoplat')
    rows = mydb.execQuery(
        "SELECT name,SUM(testsRun),SUM(successes),SUM(failures),SUM(errors),date_format(create_time, '%Y%m%d') AS day  from webinterface_Reports where date_format(create_time, '%Y%m%d') = date_format(NOW(), '%Y%m%d') and LENGTH(`name`) >0 GROUP BY NAME ORDER BY name")
    with open('jenkins_env_data', 'w') as f:
        for i, row in enumerate(rows):
            print row
            if row[0] is not None:
                f.write("{}_day={}".format(i, row[5]))
                f.write('\n')
                f.write("{}_name={}".format(i, row[0]))
                f.write('\n')
                f.write("{}_testsRun={}".format(i, row[1]))
                f.write('\n')
                f.write("{}_successes={}".format(i, row[2]))
                f.write('\n')
                f.write("{}_failures={}".format(i, row[3]))
                f.write('\n')
                f.write("{}_errors={}".format(i, row[4]))
                f.write('\n')