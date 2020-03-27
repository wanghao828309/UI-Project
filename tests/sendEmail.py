#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
import argparse
from email.mime.text import MIMEText
from email.header import Header
from sqldb import Database
import sys

reload(sys)
sys.setdefaultencoding("utf8")


def get_args():
    '''
    解析命令行参数
    :return: 命令行参数命名空间
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', action='store', dest='email', type=str, help='email')
    parser.add_argument('-t', action='store', dest='type', type=str, help='type')
    rst = parser.parse_args()
    return rst


def get_msg():
    tr_list = []
    mydb = Database('192.168.11.83', 3306, 'root', 'root', 'Wang_Test')
    sql = 'SELECT operation_name,operation_time,filmora_version,cpu_gpu,similar,win_version,graphics_card,cpu,memory_size,date_format(create_time, "%Y-%c-%d %H:%i:%S")AS day  FROM snapshotTable WHERE STATUS=1'
    res_tuple = mydb.execQuery(sql)
    print res_tuple
    if res_tuple is not None:
        for res in res_tuple:
            print res
            com_info=res[5]+"\n"+res[6]+"\n"+res[7]
            tr_msg = """
               <tr>
                   <th>{}</th>
                   <th>{}</th>
                   <th>{}</th>
                   <th>{}</th>
                   <th>{}</th>
                   <th>{}</th>
                   <th>{}</th>
               </tr>
            """.format(res[0], res[1], res[2], res[3], res[4], com_info, res[8])
            tr_list.append(tr_msg)


    tr = "".join(tr_list)
    mail_msg_head = '<p><font size="4">自动化执行报告...</font></p><hr /><table border="1"><tr><th>操作名称</th><th>比对时间</th><th>filmora版本</th><th>CPU或者GPU</th><th>电脑信息</th><th>执行时间</th></tr>'
    mail_msg_tail = '</table><br /><hr />'
    mail_msg = "{}{}{}".format(mail_msg_head, tr, mail_msg_tail)
    # print mail_msg
    return mail_msg



from email.mime.multipart import MIMEMultipart
import os, time
import jinja2, shutil

LOG_PATH = "C:\Program Files\Wondershare\Filmora9\log"


def send_mail_file():
    email = "wanghao@wondershare.cn"

    # 第三方 SMTP 服务
    mail_host = "mail.wondershare.cn"  # 设置服务器
    mail_user = "vp_system_notice@wondershare.cn"  # 用户名
    mail_pass = "Hello789"  # 口令

    sender = 'vp_system_notice@wondershare.cn'
    receivers = email  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEMultipart()
    message['From'] = Header(sender, 'utf-8')
    message['To'] = Header(email, 'utf-8')
    subject = '自动化执行发送的邮件'
    message['Subject'] = Header(subject, 'utf-8')
    # 邮件正文内容
    message.attach(MIMEText('测试带附件', 'plain', 'utf-8'))

    opencl_log = os.path.join(LOG_PATH, "opencl.log")
    NLELog_log = os.path.join(LOG_PATH, "NLELog.txt")
    log0_log = os.path.join(LOG_PATH, "log0.txt")
    app_log_log = os.path.join(LOG_PATH, "app_log_{}.txt".format(time.strftime("%Y-%m-%d", time.localtime())))

    # 构造附件1，opencl.log 文件
    att1 = MIMEText(open(opencl_log, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="opencl.log"'
    message.attach(att1)

    # 构造附件1，opencl.log 文件
    att2 = MIMEText(open(NLELog_log, 'rb').read(), 'base64', 'utf-8')
    att2["Content-Type"] = 'application/octet-stream'
    att2["Content-Disposition"] = 'attachment; filename="NLELog.txt"'
    message.attach(att2)

    # 构造附件1，opencl.log 文件
    att3 = MIMEText(open(log0_log, 'rb').read(), 'base64', 'utf-8')
    att3["Content-Type"] = 'application/octet-stream'
    att3["Content-Disposition"] = 'attachment; filename="log0.txt"'
    message.attach(att3)

    # 构造附件1，opencl.log 文件
    att4 = MIMEText(open(app_log_log, 'rb').read(), 'base64', 'utf-8')
    att4["Content-Type"] = 'application/octet-stream'
    att4["Content-Disposition"] = 'attachment; filename="app_log_{}.txt"'.format(
        time.strftime("%Y-%m-%d", time.localtime()))
    message.attach(att4)

    try:
        # smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj = smtplib.SMTP(mail_host, 25)
        # smtpObj.set_debuglevel(1)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"




if __name__ == '__main__':
    print get_msg()
    # print get_version()
