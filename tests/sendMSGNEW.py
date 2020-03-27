import requests
import time
import hashlib
import operator
import json
import sys
import redis

#mobile = sys.argv[2]
#msg = sys.argv[1]
mobile = '18820969007'
msg = 'Problem: Zabbix agent on eus_filmora_back06 is unreachable for 5 minutes'
msg = 'Problem: Zabbix agent on eus_filmora_back06 is unreachable for 5'

print(mobile)
print(msg)

secret = '8d8d62f6411c024b31ca81160b7166f7'
app_key = '80d35a7ee5e9479819205f32ba13ede6'
api_url = 'https://account.wondershare.com/api/v2/resources'

# every_msg_send_num = 5
# r = redis.Redis(host='172.20.103.202', port=6379,db=0)
# md5_1 = hashlib.md5()
# md5_1.update(msg.encode('utf-8'))
# redis_key = mobile + ':' + time.strftime("%Y%m%d") + ':' + md5_1.hexdigest()
# num = r.incr(redis_key)
# r.expire(redis_key , 24*60*60)
# if num > every_msg_send_num :
#     sys.exit()

def func_send_sms(tel , content):
    params = {
        'operate_type': 'send_msg',
        'mobile': tel,
        'msg': content,
        'timestamp': int(time.time()),
        'app_key': app_key,
    }

    arr = sorted(params.items(), key=operator.itemgetter(0))
    sign = ''
    for i in range(len(arr)):
        sign += arr[i][0] + str(arr[i][1])

    sign = secret + sign + secret
    md5 = hashlib.md5()
    md5.update(sign.encode('utf-8'))
    sign = md5.hexdigest()
    params['sign'] = sign

    print(params)

    headers = {'content-type': "application/json"}
    response = requests.post(api_url, data=json.dumps(params), verify=False, headers=headers)

    print(response.text)
    print(response.status_code)

msg = msg.split()
print(msg)

tmp = ''
for i in range(len(msg)):
    tmp += str(msg[i]) + ' '
    if (len(tmp) > 50) :
        print(tmp)
        func_send_sms(mobile, "Problem: Zabbix agent on eus_filmora_back06 is unreachable")
        tmp = ''
        continue

# func_send_sms(mobile , tmp)
# print(tmp)

# func_send_sms(mobile , msg)
# func_send_sms(mobile , 'hey')