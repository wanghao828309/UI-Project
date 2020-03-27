# coding=utf-8


import requests
import argparse, os, shutil
from requests.exceptions import ConnectTimeout,ConnectionError
import pymysql.cursors


class MysqldbHelper(object):
    """
                            操作mysql数据库，基本方法
    """

    def __init__(self, host="localhost", user="root", password="root", port=3306, db="test", charset='utf8mb4',
                 cursorclass=pymysql.cursors.DictCursor):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.charset = charset
        self.cursorclass = cursorclass
        self.con = None
        self.cur = None
        try:
            self.con = pymysql.connect(host=self.host, user=self.user, passwd=self.password, port=self.port, db=self.db,
                                       charset=charset, cursorclass=cursorclass)
            # 所有的查询，都在连接 con 的一个模块 cursor 上面运行的
            self.cur = self.con.cursor()
        except:
            raise Exception("DataBase doesn't connect,close connectiong error;please check the db config.")

    def close(self):
        """关闭数据库连接

        """
        if self.con:
            self.cur.close()
            self.con.close()

    def executeCommentSql(self, sql=''):
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
        finally:
            self.cur.close()
            self.con.close()

    def executeSqlOne(self, sql=''):
        """执行sql语句，针对读操作返回结果集

            args：
                sql  ：sql语句
        """
        try:
            self.cur.execute(sql)
            records = self.cur.fetchone()
            return records
        except pymysql.Error, e:
            error = 'MySQL execute failed! ERROR (%s): %s' % (e.args[0], e.args[1])
            print error


# GATEWAY_HOST = 'automagic.wondershare.cn:8100'
GATEWAY_HOST = '192.168.11.83:9000'


def repeatTime(arg):
    """
    装饰器：用于对方法的装饰，包括（1.捕获方法的异常输出的html报告 2.控制方法出错重复执行）
    :param arg: int（出错重复执行的次数）
    :return:
    """

    def decorator(func):
        def wrapper(*args, **kw):
            for i in range(int(arg)):
                try:
                    if i > 0:
                        print ("第 " + str(i) + " 次重试")
                        #删除重试之前webinterface_Reports表里的记录

                        mydb = MysqldbHelper(host='192.168.11.83', port=3306, user='root', password='root',
                                             db='autoplat')
                        print args[0]
                        select_sql = 'select status from webinterface_Reports where `name` = (SELECT name FROM webinterface_Suite where id = "{}") ORDER BY id Desc LIMIT 1'.format(args[0])
                        res = mydb.executeSqlOne(select_sql)
                        if not res["status"]:
                            sql = 'UPDATE webinterface_Reports set delStatus=1 where `name` = (SELECT name FROM webinterface_Suite where id = "{}") ORDER BY id Desc LIMIT 1'.format(args[0])
                            mydb.executeCommentSql(sql)

                    r = func(*args, **kw)
                    return r
                except ConnectionError as c_err:
                    import time
                    time.sleep(5)
                    print('【Exception】 The one case fail by :%s' % c_err.message)
            # raise c_err

        return wrapper

    return decorator


def mkdir(dirPath):
    if os.path.isdir(dirPath):
        shutil.rmtree(dirPath)
        import time as t
        t.sleep(1)
    os.makedirs(dirPath)


def copyfile(sourceSrcfile, dstSrcfile):
    """
    复制文件
    :param sourceSrcfile:
    :param dstSrcfile:
    """
    shutil.copyfile(sourceSrcfile, dstSrcfile)


def get_args():
    '''
    解析命令行参数
    :return: 命令行参数命名空间
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='suite_id', type=str, help='Suite ID')
    parser.add_argument('-e', action='store', dest='env_name', type=str, help='Env Name')
    parser.add_argument('-t', action='store', dest='time', type=str, help='Time')
    rst = parser.parse_args()
    return rst


@repeatTime(5)
def _runSuite(ids, env_name):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        id_list = []
        for id in ids.split(","):
            if len(id) > 0:
                id_list.append(id)

        r = requests.post('http://{}/api/webinterface/suite/run'.format(GATEWAY_HOST), data={
            'index': "{}".format(id_list),
            'env_name': env_name,
            'is_async': "False",
        }, headers=headers, timeout=600)
    except ConnectTimeout as ct:
        print "/api/webinterface/suite/run接口请求报错 ConnectTimeout: {}".format(ct.message)
        raise ct
    except ConnectionError as c_err:
        print "/api/webinterface/suite/run接口请求报错 ConnectionError: {}".format(c_err.message)
        raise c_err
    except Exception as err:
        print "/api/webinterface/suite/run接口请求报错 Exception: {}".format(err.message)
        if "Connection reset by peer" in err.message:
            raise ConnectionError('Connection aborted. Connection reset by peer')
        else:
            raise err
    if r is None:
        raise ConnectionError("接口返回值为空 [error] http://{}/api/webinterface/suite/run".format(GATEWAY_HOST))
    elif r.status_code != 200:
        raise ConnectionError("接口返回码为：{} [error] http://{}/api/webinterface/suite/run".format(r.status_code, GATEWAY_HOST))
    print "运行结果："
    print r.content
    res = r.json()
    return res


def _ftp_report(res, time):
    if res.has_key("report_url"):
        report = res.get('report_url')
        sourceSrc = "/data/www/html/automagic/webinterface/"
        sourceSrcfile = sourceSrc + report.split("/")[-1]
        dstSrc = "/data/www/html/automagic/report/{}/".format(time)
        dstSrcfile = dstSrc + "index.html"
        mkdir(dstSrc)
        copyfile(sourceSrcfile, dstSrcfile)
        status = res.get('report_status')
        if not status:
            raise Exception("运行报告状态为：Fail")


if __name__ == '__main__':
    suite_id = get_args().suite_id
    env_name = get_args().env_name
    time = get_args().time
    res = _runSuite(suite_id, env_name)
    if res is not None:
        _ftp_report(res, time)
