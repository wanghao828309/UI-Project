#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from email.mime.multipart import MIMEMultipart


def send_mail(mess):
    # 第三方 SMTP 服务
    mail_host = "mail.wondershare.cn"  # 设置服务器
    mail_user = "vp_system_notice@wondershare.cn"  # 用户名
    mail_pass = "Hello789"  # 口令

    sender = 'vp_system_notice@wondershare.cn'
    receivers = ["wanghao@wondershare.cn"]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    mail_msg = """
    <p>自动化执行报告...</p>
    <table border="1">
    <tr>
        <th>操作名称</th>
        <th>filmora版本</th>
        <th>win系统版本</th>
        <th>显卡</th>
        <th>消耗时长</th>
        <th>执行时间</th>
    </tr>
    <tr>
        <th>{}</th>
    </tr>
    </table>
    <br />
    <hr />
    <p><a href="http://www.runoob.com">这是一个链接</a></p>
    """.format(1)
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header(sender, 'utf-8')
    message['To'] = Header(str(receivers), 'utf-8')

    subject = '接口报错自动发送的邮件'
    message['Subject'] = Header(subject, 'utf-8')

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
    send_mail("test")
