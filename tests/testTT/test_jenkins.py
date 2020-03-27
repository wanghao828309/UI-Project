import jenkins,time

def duration_change(num):
    if num == 0:
        x = 0
    elif int(num) < 1000:
        return '1s'
    else:
        x = str(num)[:-3]
    if int(x) <= 60:
        return str(x)+'s'
    elif int(x) < 3600:
        y = float(x)/60
        z = str(y).split('.')
        return z[0]+'min:'+ str(int(z[1])*6)[:2]+'s'
    else:
        y = divmod(int(x), 3600)
        z = float(y[1])/60
        m = str(z).split('.')
        return str(y[0])+'h:'+m[0]+'min:'+ str(int(m[1])*6)[:2]+'s'

def timeStamp(timastamp):
    timastamp = str(timastamp)[:10]
    timeArray = time.localtime(int(timastamp))
    chartime = time.strftime('%Y-%m-%d %H:%M:%S',timeArray)
    return chartime

def testreport(path):
    path = path[7:]
    return path

server = jenkins.Jenkins("http://192.168.11.83:8080/", "wanghao", "123456")
p={'TrunId': '0', 'TaskId': '1'}
res = server.build_job("test",parameters=p)

jenkinsjob = server.get_job_info("test")
num = jenkinsjob['lastBuild']['number']
print num
time.sleep(15)
while True:
    print server.get_build_info("test", num+1)
    building = server.get_build_info("test", num+1)['building']
    print building
    if not building:
        # print building
        break


# jenkinsjob = server.get_job_info("filmora")


# # print server.ge
# print jenkinsjob
# for i in jenkinsjob['builds'][:40]:
#     bi = server.get_build_info("filmora", i['number'])
#     # print bi
#     th = {}
#     th['starttime'] = timeStamp(bi['timestamp'])
#     th['build_name'] = bi['fullDisplayName']
#     # th['exectime'] = duration_change(bi['duration'])
#     th['result'] = bi['result']
#     # th['user'] = bi['actions'][0]['causes'][0]['shortDescription']
#     th['consoleurl'] = bi['url'] + 'console'
#     # if len(bi["changeSet"]["items"]):
#     #     print bi["changeSet"]["items"][0]["paths"][15]["file"]
#     # print testreport(bi['artifacts'][0]['relativePath'])
#     # print i["url"].split("test")[0]+"test"
#
# print th


# print  'http://10.10.0.70:8080/job/test'+r"/ws/keyword/result/2018-09-21/2018-09-21-09_14_36_result.html"
# print "2018-09-25 09:38:17".split(" ")[0]