# coding:utf-8
# Copyright (c) 2020 YBM.eli0t All rights reserved.
# Power by Eli0t
# 目前需要填写：
#   编号
#   amap_key（获取位置和经纬度） 高德地图 API 的 key 使用API前您需先申请Key。若无高德地图API账号需要先申请账号。
#   whoami_value(可以通过编号计算出，目前仅支持 1872 中队)
#   X-CSRF-Token 变化情况未知
#   cookie 一般不变化

import requests
import json
import time
import logging
import ast
import sys
import yaml


logging.getLogger().setLevel(logging.INFO)

with open('config.yaml', 'r') as config:
    information = yaml.load(config.read(), Loader=yaml.FullLoader)
    number = information['number']
    amap_key = information['amap_key']
    Cookie = information['Cookie']
    X_CSRF_Token = information['X_CSRF_Token']
    Province_GPS = information['Province_GPS']
    City_GPS = information['City_GPS']
    District_GPS = information['District_GPS']
    Detail_GPS = information['Detail_GPS']
    health = information['health']

name = ''
time_ = int(str(int(time.time())).ljust(13,'0'))
format_date = time.strftime( "%Y-%m-%d", time.localtime()) 
ts = time.strptime(format_date, "%Y-%m-%d")
date_ = int(str(int(time.mktime(ts))).ljust(13, '0'))
Class = number[:3]
whoami_value = str(hex(0x5e565f3eb897e100066ca24a + int(number[-2:])))[2:]
telephone = ''
null = ''
t = round(time.time() * 1000)
# 13 位详细时间戳


# 通过 IP 获取位置，返回一个包含 省份、城市、经度、纬度 的列表
def IP_get_addr_and_itude():
    logging.info("\033[1;32m ** 位置通过 IP 获取开始 ** \033[0m")
    get_IP_url = 'https://api.ipify.org/?format=json'
    IP = ast.literal_eval(requests.get(get_IP_url).text)['ip']
    print(" 当前 IP ：" + IP)
    amap_API_url_get_addr = 'http://restapi.amap.com/v3/ip?ip={}&key=38731f296471c055b5ac30f079df1473'.format(IP, amap_key)
    addr_IP_get = requests.get(amap_API_url_get_addr).text
    addr_IP_get = ast.literal_eval(addr_IP_get)
    City_IP_GPS = addr_IP_get['city']
    print(" 当前城市（通过 IP 获取）：" + City_IP_GPS)
    Province_IP_GPS = addr_IP_get['province']
    print(" 当前省份（通过 IP 获取）：" + Province_IP_GPS)
    Longitude_IP_GPS = addr_IP_get['rectangle'].split(';')[0].split(',')[0]
    Latitude_IP_GPS = addr_IP_get['rectangle'].split(';')[0].split(',')[1]
    print(" 当前经度（通过 IP 获取）：" + Longitude_IP_GPS)
    print(" 当前纬度（通过 IP 获取）：" + Latitude_IP_GPS)
    IP_get_addr_and_itude = []
    IP_get_addr_and_itude.append(Province_IP_GPS)
    IP_get_addr_and_itude.append(City_IP_GPS)
    IP_get_addr_and_itude.append(Longitude_IP_GPS)
    IP_get_addr_and_itude.append(Latitude_IP_GPS)
    return IP_get_addr_and_itude

# 通过详细位置获取经纬度，返回一个包含 经度、纬度 的列表
def location_get_itude(Province_GPS, City_GPS, District_GPS, Detail_GPS, amap_key):
    logging.info("\033[1;32m ** 详细位置获取经纬度开始 ** \033[0m")
    amap_API_url_get_L = 'https://restapi.amap.com/v3/geocode/geo?address={}&key={}'.format(Province_GPS + City_GPS + District_GPS + Detail_GPS, amap_key)
    GPS = requests.get(amap_API_url_get_L)
    GPS = str(ast.literal_eval(GPS.text)['geocodes'])[1:-1]
    # str => dict
    GPS = ast.literal_eval(GPS)['location'].split(",")
    Longitude = GPS[0].ljust(17, '0') + '1'
    print(" 当前经度（通过详细地址获取）：" + Longitude)
    Latitude = GPS[1].ljust(17, '0') + '1'
    print(" 当前纬度（通过详细地址获取）：" + Latitude)
    location_get_itude = []
    location_get_itude.append(Longitude)
    location_get_itude.append(Latitude)
    return location_get_itude

push_data = time.strftime(number + "%Y%m%d", time.localtime()) 
logging.info("\033[1;32m ** Get ready ** \033[0m")

session = requests.Session()

# 未开发完全
'''
url_get_Cookie_1 = 'https://wxwork.jiandaoyun.com/wxwork/ww0f8c29c5c7b53b53/dashboard'
header_get_Cookie_1 = {
    'Host': 'wxwork.jiandaoyun.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-cn',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 wxwork/3.0.25 MicroMessenger/7.0.1 Language/zh'
}
re = session.get(url_get_Cookie_1, headers = header_get_Cookie_1, timeout = 20)
print(re.text)
print(re.cookies)
input()

url_get_Cookie_2 = 'https://wxwork.jiandaoyun.com/wxwork/ww0f8c29c5c7b53b53/dashboard?code=jJJCuqSe2mRLKIVzaqz9XuvrvdaDbQDkPVojLaSgCSA&state=5fd23bf5fdf61734d1dcb73'
header_get_Cookie_2 = {
    'Host': 'wxwork.jiandaoyun.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 wxwork/3.0.25 MicroMessenger/7.0.1 Language/zh',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': "JDY_SID=s%3AtMXH2b4RlXPSCg1CFgpp_Lr4BKHT0kiQ.ls1J9cw2K90%2BpcGlYBtrtquA625DqQOwSd8QDGqimrM; _csrf=s%3AFZPR-zsYhX9xBkcReVSfNNji.WlSihcpP4JXGyzh32aO5AEL%2Bcms%2BfhiYdIxBqraUoNM"
}
re = session.get(url_get_Cookie_2, headers = header_get_Cookie_2, timeout = 20)
print(re.text)
input()
'''

url_start_ready_1 = 'https://wxwork.jiandaoyun.com/wxwork/ww0f8c29c5c7b53b53/dashboard'
header_start_ready_1 = {
    'Host': 'wxwork.jiandaoyun.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'If-None-Match': 'W/"1aa4-cm7T6S4W9E82aHiZK14XgeRHHqg"',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 wxwork/3.0.25 MicroMessenger/7.0.1 Language/zh',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cookie': Cookie
}

url_start_ready_2 = 'https://wxwork.jiandaoyun.com/dashboard/apps'
header_start_ready_2 = {
    'Host': 'wxwork.jiandaoyun.com',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type' : 'application/json;charset=UTF-8',
    'X-JDY-Ver': 'undefined',
    'Origin' : 'https://wxwork.jiandaoyun.com',
    'Referer': 'https://wxwork.jiandaoyun.com/wxwork/ww0f8c29c5c7b53b53/dashboard',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 wxwork/3.0.25 MicroMessenger/7.0.1 Language/zh',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-CSRF-Token': X_CSRF_Token,
    'Cookie' : Cookie
}
data_start_ready_2 = {
    'corpId': 'ww0f8c29c5c7b53b53'
}

url_start_ready_3 = 'https://wxwork.jiandaoyun.com/dashboard/workflow/todo_count'
header_start_ready_3 = header_start_ready_2
data_start_ready_3 = data_start_ready_2

url_start_ready_4 = 'https://track.jiandaoyun.com/log?e=custom_app_post_m&t={}&u=ww0f8c29c5c7b53b53-{}&c=ww0f8c29c5c7b53b53'.format(t, number)
header_start_ready_4 = {
    'Host': 'track.jiandaoyun.com',
    'Accept': 'image/webp,image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 wxwork/3.0.25 MicroMessenger/7.0.1 Language/zh',
    'Accept-Language': 'zh-cn',
    'Referer': 'https://wxwork.jiandaoyun.com/wxwork/ww0f8c29c5c7b53b53/dashboard',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-CSRF-Token': X_CSRF_Token
}

url_ready_1 = "https://track.jiandaoyun.com/log?e=app_visit_from_mobile&t={}&u=ww0f8c29c5c7b53b53-{}&c=ww0f8c29c5c7b53b53".format(t, number)
header_ready_1 = header_start_ready_4
# 2020-07-12T07:03:15.045Z

url_ready_2 = 'https://wxwork.jiandaoyun.com/_/app/5e3abc6eb2603a0006585067'
header_ready_2 = {
    'Host': 'wxwork.jiandaoyun.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 wxwork/3.0.25 MicroMessenger/7.0.1 Language/zh',
    'Referer': 'https://wxwork.jiandaoyun.com/wxwork/ww0f8c29c5c7b53b53/dashboard',
    'Accept': '*/*',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json;charset=UTF-8',
    'X-JDY-Ver': 'undefined',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://wxwork.jiandaoyun.com',
    'Connection': 'keep-alive',
    'X-CSRF-Token': X_CSRF_Token,
    'Cookie': Cookie
}
data_ready_2 = {
    'appId': '5e3abc6eb2603a0006585067'
    # 这个应该是整的学校都是一样的
}
# 2020-07-12T07:03:15.052Z

url_ready_3 = 'https://wxwork.jiandaoyun.com/_/app/5e3abc6eb2603a0006585067/workflow/query_data_count'
header_ready_3 = header_ready_2
data_ready_3 = {
    'type': 'todo'
}
# 2020-07-12T07:03:15.296Z

url_1 = 'https://wxwork.jiandaoyun.com/_/app/5e3abc6eb2603a0006585067/form/5e329f810cc34e0006b9706b'
header = {
    'Host': 'wxwork.jiandaoyun.com',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 wxwork/3.0.25 MicroMessenger/7.0.1 Language/zh',
    'Referer': 'https://wxwork.jiandaoyun.com/wxwork/ww0f8c29c5c7b53b53/dashboard',
    'Accept': '*/*',
    'Accept-Language': 'zh-cn',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json;charset=UTF-8',
    'X-CSRF-Token': X_CSRF_Token,
    'X-JDY-Ver': 'undefined',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://wxwork.jiandaoyun.com',
    'Connection': 'keep-alive',
    'Cookie': Cookie,
    'TE': 'Trailers'
}

data_1 = {
    "appId": "5e3abc6eb2603a0006585067",
    "entryId": "5e329f810cc34e0006b9706b"
}
# "text" : "{\"appId\":\"5e3abc6eb2603a0006585067\",\"entryId\":\"5e329f810cc34e0006b9706b\"}"
# 1619  2020-07-12T07:03:17.821Z

url_middle = 'https://wxwork.jiandaoyun.com/_/app/5e3abc6eb2603a0006585067/get_vip_pack'
header_middle = header_ready_2
data_middle = data_1

data_2_1 = {
  "formId" : "5e351e41041a5f0006de5b66",
  "appId" : "5e3abc6eb2603a0006585067",
  "entryId" : "5e329f810cc34e0006b9706b",
  "dataId" : '',
  "filter" : {
    "rel" : "and",
    "cond" : [
      {
        "entryId" : "5e351e41041a5f0006de5b66",
        "value" : [
          whoami_value ],
        "method" : "in",
        "type" : "user",
        "field" : "_widget_1582792744211"
      }
    ]
  },
  "field" : "_widget_1580539457795"
}
# get number

url_all = 'https://wxwork.jiandaoyun.com/_/data/link'
data_2 = {
  "formId" : "5e351e41041a5f0006de5b66",
  "appId" : "5e3abc6eb2603a0006585067",
  "entryId" : "5e329f810cc34e0006b9706b",
  "dataId" : '',
  "filter" : {
    "rel" : "and",
    "cond" : [
      {
        "entryId" : "5e351e41041a5f0006de5b66",
        "value" : [
          number
        ],
        "method" : "in",
        "type" : "text",
        "field" : "_widget_1580539457795"
      },
      {
        "entryId" : "5e351e41041a5f0006de5b66",
        "value" : [
          whoami_value
        ],
        "method" : "in",
        "type" : "user",
        "field" : "_widget_1582792744211"
      }
    ]
  },
  "field" : "_widget_1580539457756"
}
# get name 1
# 2460 2020-07-12T07:03:18.697Z

data_2_2 = {
  "formId" : "5e351e41041a5f0006de5b66",
  "appId" : "5e3abc6eb2603a0006585067",
  "entryId" : "5e329f810cc34e0006b9706b",
  "dataId" : '',
  "filter" : {
    "rel" : "and",
    "cond" : [
      {
        "entryId" : "5e351e41041a5f0006de5b66",
        "value" : [
          whoami_value
        ],
        "method" : "in",
        "type" : "user",
        "field" : "_widget_1582792744211"
      }
    ]
  },
  "field" : "_widget_1580539457756"
}
# get name 2

data_3 = {
    "field":"_widget_1581313193925",
    "formId":"5e351e41041a5f0006de5b66",
    "appId":"5e3abc6eb2603a0006585067",
    "entryId":"5e329f810cc34e0006b9706b",
    "dataId": "",
    "filter":{
        "cond":[
            {"type":"user",
            "field":"_widget_1582792744211",
            "method":"in",
            "value":[whoami_value],
            "entryId":"5e351e41041a5f0006de5b66"}
        ],
        "rel":"and"}
}
# 2630 2020-07-12T07:03:18.715Z



data_5 = {
    "field":"_widget_1581313193966",
    "formId":"5e351e41041a5f0006de5b66",
    "appId":"5e3abc6eb2603a0006585067",
    "entryId":"5e329f810cc34e0006b9706b",
    "dataId": "",
    "filter":{
        "cond":[
            {"type":"user",
            "field":"_widget_1582792744211",
            "method":"in",
            "value":[whoami_value],
            "entryId":"5e351e41041a5f0006de5b66"}
        ],
        "rel":"and"}
}

data_6 = {
    "field":"_widget_1581313194033",
    "formId":"5e351e41041a5f0006de5b66",
    "appId":"5e3abc6eb2603a0006585067",
    "entryId":"5e329f810cc34e0006b9706b",
    "dataId": "",
    "filter":{
        "cond":[
            {"type":"user",
            "field":"_widget_1582792744211",
            "method":"in",
            "value":[whoami_value],
            "entryId":"5e351e41041a5f0006de5b66"}
        ],
        "rel":"and"}
}
# 2020-07-12T07:03:19.023Z


data_8 = {
    "field":"_widget_1580372529999",
    "formId":"5e4212ae1ce79100064f49bd",
    "appId":"5e3abc6eb2603a0006585067",
    "entryId":"5e329f810cc34e0006b9706b",
    "dataId": "",
    "filter":{
        "cond":[
            {"type":"text",
            "field":"_widget_1581486714569",
            "method":"in",
            "value":[number+name],
            "entryId":"5e4212ae1ce79100064f49bd"}
        ],
        "rel":"and"}
}
# 3869 _widget_1580372529999
# 2020-07-12T07:03:19.196Z

data_9 = {
    "field":"_widget_1580372530349",
    "formId":"5e4212ae1ce79100064f49bd",
    "appId":"5e3abc6eb2603a0006585067",
    "entryId":"5e329f810cc34e0006b9706b",
    "dataId": "",
    "filter":{
        "cond":[
            {"type":"text",
            "field":"_widget_1581486714569",
            "method":"in",
            "value":[number+name],
            "entryId":"5e4212ae1ce79100064f49bd"}
        ],
        "rel":"and"}
}
# 533 _widget_1580372530349
# 2020-07-12T07:03:19.364Z

url_push = 'https://wxwork.jiandaoyun.com/_/data/create'

if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '-i':
            list_ip = IP_get_addr_and_itude()
            Detail_GPS_push = ''
            Province_GPS_push = list_ip[0]
            City_GPS_push = list_ip[1]
            Longitude_push = list_ip[2]
            Latitude_push = list_ip[3]
        elif sys.argv[i] == '-c':
            Detail_GPS_push = Detail_GPS
            Province_GPS_push = Province_GPS
            City_GPS_push = City_GPS
            list_itude = location_get_itude(Province_GPS, City_GPS, District_GPS, Detail_GPS, amap_key)
            Longitude_push = list_itude[0]
            Latitude_push = list_itude[1]
    # 读取位置参数

    time.sleep(1)
    re = session.get(url_start_ready_1, headers = header_start_ready_1, timeout = 20)
    print(re.status_code)
    re = session.post(url_start_ready_2, headers = header_start_ready_2, data = json.dumps(data_start_ready_2), timeout = 20)
    print(re.status_code)
    re = session.post(url_start_ready_3, headers = header_start_ready_3, data = json.dumps(data_start_ready_3), timeout = 20)
    print(re.status_code)
    re = session.get(url_start_ready_4, headers = header_start_ready_4, timeout = 20)
    print(re.status_code)
    re = session.get(url_ready_1, headers = header_ready_1, timeout = 20)
    print(re.status_code)
    re = session.post(url_ready_2, headers = header_ready_2, data = json.dumps(data_ready_2), timeout = 20)
    print(re.status_code)
    re = session.post(url_ready_3, headers = header_ready_3, data = json.dumps(data_ready_2), timeout = 20)
    print(re.status_code)
    re = session.post(url_1, headers = header, data = json.dumps(data_1), timeout = 20)
    print(' get if seccess ' + str(re.status_code))
    re = session.post(url_middle, headers = header_middle, data = json.dumps(data_middle), timeout = 20)
    print(str(re.status_code))
    logging.info("\033[1;32m all ready to start ! \033[0m")
    re = session.post(url_all, headers = header, data = json.dumps(data_2_1), timeout = 20)
    number = ast.literal_eval(re.text)['value']
    print(' get number ' + number)
    re = session.post(url_all, headers = header, data = json.dumps(data_2), timeout = 20)
    name = ast.literal_eval(re.text)['value']
    print(' get name ' + name)
    re = session.post(url_all, headers = header, data = json.dumps(data_2_2), timeout = 20)
    name_2 = ast.literal_eval(re.text)['value']
    print(' get name 2 ' + name_2)
    re = session.post(url_all, headers = header, data = json.dumps(data_3), timeout = 20)
    sex = ast.literal_eval(re.text)['value']
    print(' get sex ' + sex)
    # attention
    data_4 = {
        "field":"_widget_1580282769605",
        "formId":"5e4212ae1ce79100064f49bd",
        "appId":"5e3abc6eb2603a0006585067",
        "entryId":"5e329f810cc34e0006b9706b",
        "dataId": "",
        "filter":{
            "cond":[
                {"type":"text",
                "field":"_widget_1581486714569",
                "method":"in",
                "value":[number+name],
                "entryId":"5e4212ae1ce79100064f49bd"}
            ],
            "rel":"and"}
    }
    # old type
    re = session.post(url_all, headers = header, data = json.dumps(data_4), timeout = 20)
    telephone = ast.literal_eval(re.text)['value']
    print(' get telephone ' + telephone)
    re = session.post(url_all, headers = header, data = json.dumps(data_5), timeout = 20)
    sdept = ast.literal_eval(re.text)['value']
    print(' get sdept ' + sdept)
    re = session.post(url_all, headers = header, data = json.dumps(data_6), timeout = 20)
    specialty = ast.literal_eval(re.text)['value']
    print(' get specialty ' + specialty)
    # attention
    data_6_2 = {
      "formId" : "5e351e41041a5f0006de5b66",
      "appId" : "5e3abc6eb2603a0006585067",
      "entryId" : "5e329f810cc34e0006b9706b",
      "dataId" : '',
      "filter" : {
        "rel" : "and",
        "cond" : [
          {
            "entryId" : "5e351e41041a5f0006de5b66",
            "value" : [
              number+name
            ],
            "method" : "in",
            "type" : "text",
            "field" : "_widget_1581486490214"
          }
        ]
      },
      "field" : "_widget_1581313194061"
    }
    # get class
    re = session.post(url_all, headers = header, data = json.dumps(data_6_2), timeout = 20)
    Class = ast.literal_eval(re.text)['value']
    print(' get class ' + Class)

    data_7 = {
        "field":"_widget_1581318550297",
        "formId":"5e4212ae1ce79100064f49bd",
        "appId":"5e3abc6eb2603a0006585067",
        "entryId":"5e329f810cc34e0006b9706b",
        "dataId": "",
        "filter":{
            "cond":[
                {"type":"text",
                "field":"_widget_1581486714569",
                "method":"in",
                "value":[number+name],
                "entryId":"5e4212ae1ce79100064f49bd"}
            ],
            "rel":"and"}
    }
    # 2020-07-12T07:03:19.187Z
    re = session.post(url_all, headers = header, data = json.dumps(data_7), timeout = 20)
    Province = ast.literal_eval(re.text)['value']['province']
    City = ast.literal_eval(re.text)['value']['city']
    District = ast.literal_eval(re.text)['value']['district']
    Detail = ast.literal_eval(re.text)['value']['detail']
    print(' get address ' + Province + City + District + Detail)
    re = session.post(url_all, headers = header, data = json.dumps(data_8), timeout = 20)
    a = re.status_code
    re = session.post(url_all, headers = header, data = json.dumps(data_9), timeout = 20)
    b = re.status_code
    if a == 200 and b == 200:
            logging.info("\033[1;32m 信息全部获取完毕 \033[0m")
    # start push data
    logging.info("\033[1;32m ** Wait five seconds ** \033[0m")
    time.sleep(5)
    data_push = {
      "values" : {
        "_widget_1587197651534" : {
          "visible" : 'false',
          "data" : null
        },
        "_widget_1583383208396" : {
          "visible" : 'true',
          "data" : whoami_value
        },
        "_widget_1581314208236" : {
          "visible" : 'true',
          "data" : sex
        },
        "_widget_1585056350799" : {
          "visible" : 'true',
          "data" : ""
        },
        "_widget_1581470866567" : {
          "visible" : 'false',
          "data" : name
        },
        "_widget_1580372529030" : {
          "visible" : 'true',
          "data" : {
            "district" : District_GPS,
            "lnglatXY" : [
              Longitude_push,
              Latitude_push
            ],
            "detail" : Detail_GPS_push,
            "province" : Province_GPS_push,
            "city" : City_GPS_push
          }
        },
        "_widget_1581309340517" : {
          "visible" : 'true',
          "data" : Class
        },
        "_widget_1581318550297" : {
          "visible" : 'true',
          "data" : {
            "district" : District,
            "detail" : Detail,
            "province" : Province,
            "city" : City
          }
        },
        "_widget_1585383950352" : {
          "visible" : 'true',
          "data" : health
        },
        "_widget_1586768128186" : {
          "visible" : 'true',
          "data" : "否"
        },
        "_widget_1587197651716" : {
          "visible" : 'true',
          "data" : "否"
        },
        "_widget_1581655457136" : {
          "visible" : 'true',
          "data" : 37
        },
        "_widget_1580372529999" : {
          "visible" : 'true',
          "data" : ""
        },
        "_widget_1581486852689" : {
          "visible" : 'false',
          "data" : number+name
        },
        "_widget_1583397430927" : {
          "visible" : 'true',
          "data" : "为响应党中央号召，坚决打赢新冠疫情防控人民战争、总体战、阻击战，我郑重承诺：所填疫情防控信息真实准确并自行承担纪律责任、法律责任。"
        },
        "_widget_1581559576367" : {
          "visible" : 'true',
          "data" : push_data
        },
        "_widget_1581307558927" : {
          "visible" : 'true',
          "data" : number
        },
        "_widget_1586768127924" : {
          "visible" : 'true',
          "data" : "是"
        },
        "_widget_1587197651732" : {
          "visible" : 'false',
          "data" : null
        },
        "_widget_1585383950396" : {
          "visible" : 'true',
          "data" : "否"
        },
        "_widget_1581314208382" : {
          "visible" : 'true',
          "data" : specialty
        },
        "_widget_1585383950412" : {
          "visible" : 'true',
          "data" : "否"
        },
        "_widget_1580372530169" : {
          "visible" : 'true',
          "data" : time_
          # 精确时间戳
        },
        "_widget_1586768127940" : {
          "visible" : 'true',
          "data" : "否"
        },
        "_widget_1580282769605" : {
          "visible" : 'true',
          "data" : telephone
        },
        "_widget_1580282769590" : {
          "visible" : 'false',
          "data" : name
        },
        "_widget_1581308432036" : {
          "visible" : 'true',
          "data" : sdept
        },
        "_widget_1585374358624" : {
          "visible" : 'false',
          "data" : date_
          # 日期时间戳
        },
        "_widget_1580372530349" : {
          "visible" : 'true',
          "data" : ""
        }
      },
      "formId" : "5e329f810cc34e0006b9706b",
      "dataId" : null,
      "hasResult" : 'true',
      "authGroupId" : -1,
      "appId" : "5e3abc6eb2603a0006585067",
      "entryId" : "5e329f810cc34e0006b9706b",
      "flowAction" : null
    }
    # 2020-07-12T07:03:29.371Z"
    re = session.post(url_push, headers = header, data = json.dumps(data_push), timeout = 20)
    print(' push data ' + str(re.text))