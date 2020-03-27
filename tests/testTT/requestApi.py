# coding=utf-8


import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from time import sleep

GATEWAY_HOST = 'dev.dachentech.com'




def decorator(func):  
    def wrapper(*args, **kw):  
        for i in range(4): 
            try:  
                if i >0:
                    print("第 " + str(i) + " 次重试")
                r = func(*args, **kw)  
                return r  
            except Exception as err:  
                sleep(3)
                if i >2:
                    _send_mail(str(err))
                    print( 'The one case fail by :%s' % err  )
        raise Exception  

    return wrapper  


def _send_mail(mess):
        # 第三方 SMTP 服务
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="770834094@qq.com"    #用户名
    mail_pass="lmaxcmjvoeydbbjj"   #口令 
      
      
    sender = '770834094@qq.com'
    receivers = ['wanghao@dachentech.com.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
      
    message = MIMEText(mess, 'plain', 'utf-8')
    message['From'] = '770834094@qq.com'
    message['To'] =  'wanghao@dachentech.com.cn'
      
    subject = '接口报错自动发送的邮件'
    message['Subject'] = Header(subject, 'utf-8')
      
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"
        
        
def _register(phone, password):
    return requests.post('http://{}/health/user/register'.format(GATEWAY_HOST), data={
        'telephone': phone,
        'password': password,
        'userType': "3",
    }, timeout=10)

# 用户登录接口
@decorator
def _login(phone, password):
    try:
        r =  requests.post('http://{}/health/user/login'.format(GATEWAY_HOST), data={
        'telephone': phone,
        'password': password,
        'userType': '3'
        }, timeout=5)
    except requests.exceptions.ConnectTimeout:
        raise RuntimeError("接口请求超时Timeout>5 [error] http://{}/health/user/login".format(GATEWAY_HOST))
    except Exception:
        raise RuntimeError("Exception [error] http://{}/health/user/login".format(GATEWAY_HOST))
    
    if r is None:
        raise RuntimeError("接口返回值为空 [error] http://{}/health/user/login".format(GATEWAY_HOST))
    elif r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{}/health/user/login".format(GATEWAY_HOST))
    return r
    
# 获取token接口
# @decorator 
def _get_access_token(telnum,password):
    payload = {'telephone':telnum,
               'password':password,
               'userType':'3'
               }
    url = "http://{}/health/user/login".format(GATEWAY_HOST)
    r = requests.post(url,data=payload, timeout=5)
    if r.json().get('resultCode') != 1:
        print("LBSLocateCity API Error resultCode=" + str(r.json().get('resultCode')))
    else:
        access_token = r.json()['data']['access_token']
        print("access_token为：" + str(access_token))
        return access_token
    
# 查看圈子详情接口
@decorator 
def _search_circle(phone, password):
    access_token=_get_access_token(phone, password)
    r = requests.post("http://{0}/circle/index/{1}?access_token={2}".format(GATEWAY_HOST,"422716257922560000",access_token),headers = {
        'Content-Type' : 'application/json'
    }, timeout=5) 
#     print r.json()
    if r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}//circle/index/{1}?access_token={2}".format(GATEWAY_HOST,"422716257922560000",access_token))
    return r

# 关闭直播接口
@decorator 
def _close_live(phone, password):
    access_token=_get_access_token(phone, password)
    r = requests.post("http://{0}/live/living/app/openLive/{1}/{2}?access_token={3}".format(GATEWAY_HOST,"422716257922560000","0",access_token), timeout=5)  
#     print r.json()
    if r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}/live/living/app/openLive/{1}/{2}?access_token={3}".format(GATEWAY_HOST,"422716257922560000","0",access_token))
    return r

# 关闭诊疗路径接口
@decorator 
def _close_treatPath(phone, password):
    access_token=_get_access_token(phone, password)
    r = requests.post("http://{0}/disgnosis-path/disgnosisOps/openOrCloseApp/{1}/{2}?access_token={3}".format(GATEWAY_HOST,"422716257922560000","0",access_token), timeout=5)  
#     print r.json()
    if r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}/disgnosis-path/disgnosisOps/openOrCloseApp/{1}/{2}?access_token={3}".format(GATEWAY_HOST,"422716257922560000","0",access_token))
    return r

# 获取验证码接口
@decorator 
def _verification_code(phone, password):
    access_token=_get_access_token(phone, password)
    r = requests.post("http://{0}/smsService/sms/find?access_token={1}".format(GATEWAY_HOST,access_token), data={
        'status': '2',
        'pageIndex': '0',
        'pageSize': '1'
    }, timeout=5)
#     print r.json()
    if r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}/smsService/sms/find?access_token={1}".format(GATEWAY_HOST,access_token))
    return r


# 拉取知识库
@decorator 
def _knowledge_base(phone, password):
    access_token=_get_access_token(phone, password)
    r = requests.get("http://{0}/literature/wanfang/knowledgeDase?access_token={1}".format(GATEWAY_HOST,access_token), timeout=5)
#     print r.json()
    if r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}/literature/wanfang/knowledgeDase?access_token={1}".format(GATEWAY_HOST,access_token))
    return r

# 拉取视频讲座
@decorator 
def _video_lecture(phone, password):
    access_token=_get_access_token(phone, password)
    r = requests.get("http://{0}/drugorg/doctorFriend/getEnterpriseList?access_token={1}&pageSize={2}".format(GATEWAY_HOST,access_token,"2"), timeout=5)
#     print r.json().get('resultCode')
    if r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}/drugorg/doctorFriend/getEnterpriseList?access_token={1}&pageSize={2}".format(GATEWAY_HOST,access_token,"2" ))
    return r

# 拉取会议管理
@decorator 
def _management_meeting(phone, password):
    access_token=_get_access_token(phone, password)
    r = requests.get("http://{0}/activity/meeting/app/findMeetingActivityList?access_token={1}&pageIndex=0&pageSize=5&type=YSQ&userID=1720299".format(GATEWAY_HOST,access_token), timeout=5)
#     print r.json().get('resultCode')
    if r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}/activity/meeting/app/findMeetingActivityList?access_token={1}&pageIndex=0&pageSize=5&type=YSQ&userID=1720299".format(GATEWAY_HOST,access_token))
    return r

# 获取消息动态接口
@decorator 
def _message_dynamics(phone, password):
    access_token=_get_access_token(phone, password)
    r = requests.post("http://{0}/im/msg/msgList.action?access_token={1}".format(GATEWAY_HOST,access_token), data={
        'groupId': 'GROUP_007',
        'msgId': '66df13d6d3814570bb1e7fdd3ef67b6a',
        'cnt': '20',
        'type': '0'
    }, timeout=5)
#     print r.json()
    if r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}/im/msg/msgList.action?access_token={1}".format(GATEWAY_HOST,access_token))
    return r

# 获取提问未解决接口
@decorator 
def _ask_question(phone, password):
    access_token=_get_access_token(phone, password)
    r = requests.post("http://{0}/faq/question/unsolvedCount?access_token={1}".format(GATEWAY_HOST,access_token), timeout=5)
#     print r.json()
    if r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}/faq/question/unsolvedCount?access_token={1}".format(GATEWAY_HOST,access_token))
    return r

# 获取学币接口
@decorator 
def _me_coin(phone, password):
    access_token=_get_access_token(phone, password)
    r = requests.get("http://{0}/credit/user/balance?access_token={1}&userID=1720299".format(GATEWAY_HOST,access_token), timeout=5)
#     print r.json().get('resultCode')
    if r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}/credit/user/balance?access_token={1}&userID=1720299".format(GATEWAY_HOST,access_token))
    return r

# 获取卡券接口
@decorator 
def _me_card(phone, password):
    access_token=_get_access_token(phone, password)
    r = requests.get("http://{0}/xgcard/cardsuser/cardsList?access_token={1}".format(GATEWAY_HOST,access_token), timeout=5)
#     print r.json().get('resultCode')
    if r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}/xgcard/cardsuser/cardsList?access_token={1}".format(GATEWAY_HOST,access_token))
    return r

# 获取我的收入接口
@decorator 
def _me_income(phone, password):
    access_token=_get_access_token(phone, password)
    r = requests.get("http://{0}/circle-atm/income/my/income/detail?access_token={1}&incomeTime=2018-03&pageIndex=1".format(GATEWAY_HOST,access_token), timeout=5)
#     print r.json().get('resultCode')
    if r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}/circle-atm/income/my/income/detail?access_token={1}&incomeTime=2018-03&pageIndex=1".format(GATEWAY_HOST,access_token))
    return r

# 获取我的学堂接口
@decorator 
def _me_school(phone, password):
    access_token=_get_access_token(phone, password)
    r = requests.get("http://{0}/micro-school/class/getMyClassRoom/1?access_token={1}".format(GATEWAY_HOST,access_token), timeout=5)
#     print r.json().get('resultCode')
    if r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}/micro-school/class/getMyClassRoom/1?access_token={1}".format(GATEWAY_HOST,access_token))
    return r

# 获取圈子学堂接口
@decorator 
def _circle_school(phone, password):
    access_token=_get_access_token(phone, password)
    try:
        r = requests.get("http://{0}/circle-school/user/info/1720299?access_token={1}".format(GATEWAY_HOST,access_token), timeout=5)
    except requests.exceptions.ConnectTimeout:
        raise RuntimeError("接口请求超时Timeout>5 [error] http://{}/health/user/login".format(GATEWAY_HOST))
    except Exception:
        raise RuntimeError("Exception [error] http://{}/health/user/login".format(GATEWAY_HOST))
    
    if r is None:
        raise RuntimeError("resultCode is not 1 [error] http://{0}/circle-school/user/info/1720299?access_token={1}".format(GATEWAY_HOST,access_token))
    elif r.json().get('resultCode') != 1:
        raise AssertionError("resultCode is not 1 [error] http://{0}/circle-school/user/info/1720299?access_token={1}".format(GATEWAY_HOST,access_token))
    return r


def _tt(phone, password):
    access_token=_get_access_token(phone, password)
    try:
        r = requests.get("http://{0}/circle/findFriendCircle?access_token={1}&pageIndex=1&pageSize=20".format(GATEWAY_HOST,access_token), timeout=5)
    except requests.exceptions.ConnectTimeout:
        raise RuntimeError("接口请求超时Timeout>5 [error] http://{}/health/user/login".format(GATEWAY_HOST))
    except Exception:
        raise RuntimeError("Exception [error] http://{}/health/user/login".format(GATEWAY_HOST))
    if(r is not None):
        print r.json()
    else:
        raise RuntimeError("接口返回值为空 [error] http://{}/health/user/login".format(GATEWAY_HOST))
    
    

if __name__ == '__main__':
    json_obj = _login("13575102002","123456")
#     print json_obj.json()
    count = 1
    while (count < 1):
        try:
            print "-------------begin-------------"
            print '_login'
            json_obj = _login("13575102002","123456")
            sleep(1)
            json_obj = _search_circle("13575102002","123456")
            print '_search_circle'
            sleep(1)
            json_obj = _close_live("13575102002","123456")
            print '_close_live'
            sleep(1)
            json_obj = _close_treatPath("13575102002","123456")
            print '_close_treatPath'
            sleep(1)
            json_obj = _verification_code("13575102002","123456")
            print '_verification_code'
            sleep(1)
            json_obj = _knowledge_base("13575102002","123456")
            print '_knowledge_base'
            sleep(1)
            json_obj = _video_lecture("13575102002","123456")
            print '_video_lecture'
            sleep(1)
            json_obj = _management_meeting("13575102002","123456")
            print '_management_meeting'
            sleep(1)
            json_obj = _message_dynamics("13575102002","123456")
            print '_message_dynamics'
            sleep(1)
            json_obj = _ask_question("13575102002","123456")
            print '_ask_question'
            sleep(1)
            json_obj = _me_coin("13575102002","123456")
            print '_me_coin'
            sleep(1)
            json_obj = _me_card("13575102002","123456")
            print '_me_card'
            sleep(1)
            json_obj = _me_income("13575102002","123456")
            print '_me_income'
            sleep(1)
            json_obj = _me_school("13575102002","123456")
            print '_me_school'
            sleep(1)
            json_obj = _circle_school("13575102002","123456")
            print '_circle_school'
            count = 0
            sleep(10)
            print "\t\n------------------------------------------------------\t\n"
        except:
            break
    
    pass
