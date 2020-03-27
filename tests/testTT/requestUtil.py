#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from time import sleep
from src.utils import LogUtil
from src.utils import mysqldbUtil
from src.utils import mongodbUtil
from src.utils import FileParserUtil
from src.utils import GetPathUtil

logger=LogUtil.Logger( logger="MyrequestUtil_log").getlog()
class MyrequestUtil(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
#     @staticmethod
    def get_verification_code(self,telnum):
#         access_token=MyrequestUtil.get_access_token(telnum, password)
        testHost = FileParserUtil.MyFileParserUtil(GetPathUtil.MyGetPathUtil().get_AppAuto_path()+"\\config\\Medical.ini").get_fileValue("Basic_Data", "host")
        headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
        payload = {'status':'2',
                   'pageIndex':'0',
                   'pageSize':'1'
                   }
        data=None
        content = None
        for i in range(0,5):
            sleep(2)
            url = "http://"+testHost+"/smsService/sms/find"
            r = requests.post(url,headers=headers,data=payload)
            #r.encoding = 'utf-8'
            data=r.json()
            logger.debug("重新发送请求: "+str(i)+" 次")
            if r.status_code!=200:
                logger.error("LBSLocateCity API Error " + str(r.status_code))
            else:
                toPhone = data['data']['pageData'][0]['toPhone']
                logger.debug("注册的手机号码为：" + str(toPhone))
                if toPhone == telnum:
                    content = data['data']['pageData'][0]['content']
                    logger.debug(content)
                    break
                else:
                    logger.error("获取的手机号错误")
                    
                
#         content = data['data']['pageData'][0]['content']
        mycode=content.split("|")[2]
        logger.debug(mycode) 
        return mycode[7:11]
#         print json.dumps(data,indent=1,sort_keys=True,ensure_ascii=False) #树形打印json，ensure_ascii必须设为False否则中文会显示为unicode

    @staticmethod
    def get_access_token(telnum,password):
        payload = {'telephone':telnum,
                   'password':password,
                   'userType':'3'
                   }
        data=None
        for i in range(0,3):
            sleep(2)
            ip = FileParserUtil.MyFileParserUtil(GetPathUtil.MyGetPathUtil().get_AppAuto_path()+"\\config\\Medical.ini").get_fileValue("Basic_Data", "host")
            url = "http://"+ip+"/health/user/login"
            r = requests.post(url,data=payload)
            #r.encoding = 'utf-8'
            data=r.json()
            logger.debug("重新发送请求: "+str(i)+" 次")
            if r.status_code!=200:
                logger.error("LBSLocateCity API Error " + str(r.status_code))
            else:
                
                access_token = data['data']['access_token']
                logger.debug("access_token为：" + str(access_token))
                return access_token
            
    @staticmethod        
    def del_my_circle(telnum,password,name):
        try:
            ip = FileParserUtil.MyFileParserUtil(GetPathUtil.MyGetPathUtil().get_AppAuto_path()+"\\config\\Medical.ini").get_fileValue("Basic_Data", "ip")
            testHost = FileParserUtil.MyFileParserUtil(GetPathUtil.MyGetPathUtil().get_AppAuto_path()+"\\config\\Medical.ini").get_fileValue("Basic_Data", "host")
            mydb = mysqldbUtil.MysqldbHelper(host=ip, port=3306, user='root', password='123456', db='circle')
            sql= 'SELECT count(*)  from circle where  `name` = "'+name+'" and flag =1 '
            count = mydb.executeSqlOne(sql)['count(*)']
            logger.debug(name+" 名称的圈子记录数为为：" + str(count))
            if count > 0:
                access_token=MyrequestUtil.get_access_token(telnum, password)
                sql2= 'SELECT id from circle where  `name` = "'+name+'" and flag =1 '
                result = mydb.executeSqlOne(sql2)
                id = result['id']
                headers = {'Content-Type' : 'application/x-www-form-urlencoded','access-token' : access_token}
                data=None
                for i in range(0,3):
                    sleep(2)
                    url = "http://"+testHost+"/circle/dissolution/"
                    r = requests.post(url+str(id),headers=headers)
                    #r.encoding = 'utf-8' 
                    data=r.json()
                    logger.debug("重新发送请求: "+str(i)+" 次")
                    if r.status_code!=200:
                        logger.error("LBSLocateCity API Error " + str(r.status_code))
                    else:
                        resultCode = data['resultCode']
                        logger.debug("resultCode为：" + str(resultCode))
                        return resultCode
        finally:  
            mydb.close()
            
            
    @staticmethod        
    def del_circle_member(telnum,circleName):
        ip = FileParserUtil.MyFileParserUtil(GetPathUtil.MyGetPathUtil().get_AppAuto_path()+"\\config\\Medical.ini").get_fileValue("Basic_Data", "ip")
        userid = mongodbUtil.MyMongdb().get_userId(telnum)
        mydb = mysqldbUtil.MysqldbHelper(host=ip, port=3306, user='root', password='123456', db='circle')
        sql = 'DELETE FROM circle_member WHERE circleId = (SELECT id from circle WHERE `name`="'+circleName+'") and userId ='+str(userid)
        logger.debug("sql: "+sql)
        mydb.executeCommentSql(sql)
        
        
    @staticmethod        
    def del_friends(tel,pwd,friendTel):
        testHost = FileParserUtil.MyFileParserUtil(GetPathUtil.MyGetPathUtil().get_AppAuto_path()+"\\config\\Medical.ini").get_fileValue("Basic_Data", "host")
        userid = mongodbUtil.MyMongdb().get_userId(friendTel)
        access_token=MyrequestUtil.get_access_token(tel,pwd)
        url = "http://"+testHost+"/health/friends/delete?access_token="+access_token+"&toUserId="+str(userid)
        logger.debug("删除通讯录好友的url: "+url)
        requests.get(url)
        
    '''
                      关闭直播
    '''      
    @staticmethod       
    def close_live(tel,pwd,circleName): 
        ip = FileParserUtil.MyFileParserUtil(GetPathUtil.MyGetPathUtil().get_AppAuto_path()+"\\config\\Medical.ini").get_fileValue("Basic_Data", "ip")
        testHost = FileParserUtil.MyFileParserUtil(GetPathUtil.MyGetPathUtil().get_AppAuto_path()+"\\config\\Medical.ini").get_fileValue("Basic_Data", "host")
        access_token=MyrequestUtil.get_access_token(tel,pwd)    
        mydb = mysqldbUtil.MysqldbHelper(host=ip, port=3306, user='root', password='123456', db='circle')
        sql = 'SELECT id from circle WHERE `name`="'+circleName+'"'
        id = mydb.executeSqlOne(sql)["id"]  
        requests.post("http://"+testHost+"/live/living/app/openLive/"+str(id)+"/0?access_token="+str(access_token))  
        
    '''
                      关闭诊疗路径
    '''             
    @staticmethod        
    def close_treatPath(tel,pwd,circleName,openId=0): 
        testHost = FileParserUtil.MyFileParserUtil(GetPathUtil.MyGetPathUtil().get_AppAuto_path()+"\\config\\Medical.ini").get_fileValue("Basic_Data", "host")
        ip = FileParserUtil.MyFileParserUtil(GetPathUtil.MyGetPathUtil().get_AppAuto_path()+"\\config\\Medical.ini").get_fileValue("Basic_Data", "ip")
        access_token=MyrequestUtil.get_access_token(tel,pwd)    
        mydb = mysqldbUtil.MysqldbHelper(host=ip, port=3306, user='root', password='123456', db='circle')
        sql = 'SELECT id from circle WHERE `name`="'+circleName+'"'
        id = mydb.executeSqlOne(sql)["id"]  
        requests.post("http://"+testHost+"/disgnosis-path/disgnosisOps/openOrCloseApp/"+str(id)+"/"+str(openId)+"?access_token="+str(access_token))  
        
    '''
                      病例讨论推荐至首页
    '''             
    @staticmethod        
    def caseDiss_recommendation(tel,pwd,id=0): 
        testHost = FileParserUtil.MyFileParserUtil(GetPathUtil.MyGetPathUtil().get_AppAuto_path()+"\\config\\Medical.ini").get_fileValue("Basic_Data", "host")
        access_token=MyrequestUtil.get_access_token(tel,pwd)    
        header = {'Content-Type' : 'application/json','access-token': access_token}
        payload = {"recommendId":"428934836581937152","recommendType":3,"recommendName":"推荐04","circleId":"428560513442615296","refereeId":"1719877"}
        if id==0:
            url = "http://"+testHost+"/recommend/recommend/mobile/cancelRecommend"
        else:
            url = "http://"+testHost+"/recommend/recommend/mobile/addRecommend"
        r = requests.post(url,headers=header,json=payload)
        
        
if __name__=='__main__':
    
    print MyrequestUtil().get_verification_code("13575901001")
    
#     print "【医生圈】, ext=7 | 您的验证码是1212，如非本人操作，请忽略本短信，请勿将验证码透露给他人。请于2分钟内输入".split("|")[1]
    pass
