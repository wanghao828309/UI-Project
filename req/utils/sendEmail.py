#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from email.mime.multipart import MIMEMultipart


def send_mail(mess):
    # 第三方 SMTP 服务
    # mail_host = "smtp.qq.com"  # 设置服务器
    # mail_user = "770834094@qq.com"  # 用户名
    # mail_pass = "lmaxcmjvoeydbbjj"  # 口令

    mail_host = "smtp.wondershare.cn"  # 设置服务器
    mail_user = "wanghao@wondershare.cn"  # 用户名
    mail_pass = "Hello789"  # 口令

    sender = '770834094@qq.com'
    receivers = ["wanghao@rd.wondershare.cn"]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(mess, 'plain', 'utf-8')
    message = MIMEMultipart()
    message['From'] = 'lizhongliang@wondershare.cn'
    message['To'] = 'wanghao@rd.wondershare.cn'

    subject = '接口报错自动发送的邮件'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText('Python 邮件发送测试……', 'plain', 'utf-8'))
    # 构造附件1，传送当前目录下的 test.txt 文件
    # att1 = MIMEText(open(r'C:\Users\ws\Desktop\11.txt', 'rb').read(), 'base64', 'utf-8')
    # att1["Content-Type"] = 'application/octet-stream'
    # # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    # att1["Content-Disposition"] = 'attachment; filename="11.txt"'
    # message.attach(att1)

    # try:
    #     # smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    #     smtpObj = smtplib.SMTP(mail_host, 25)
    #     smtpObj.login(mail_user, mail_pass)
    #     smtpObj.sendmail(sender, receivers, message.as_string())
    #     print "邮件发送成功"
    # except smtplib.SMTPException:
    #     print "Error: 无法发送邮件"

    smtpObj = smtplib.SMTP(mail_host, 25)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print "邮件发送成功"

send_mail("autoTest")
