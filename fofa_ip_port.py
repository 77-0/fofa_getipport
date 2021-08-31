# -*- coding: utf-8 -*-
import client
import json
import re
import base64
import requests


with open("config.txt","r+") as f:
    data = f.read()

config_data = json.loads(data)

email = config_data['fofa-user']['email']
key = config_data['fofa-user']['key']

query_str=[]

query_str.append(input('请输入查询信息:'))
    
page = ''
fields = "ip,port"
content = {"data": []}
output = {"ip": "", "port": [], "len": ""}

login = client.Client(email, key)

for quest in query_str:

    if page == "":
        datas = login.get_data(quest, fields=fields)
        if datas['size'] >= 10000:
            page = 100 + 1
        else:
            page = datas['size'] / 100 + 2

        for page in range(1, int(page)):
            datas = login.get_data(
                quest, fields="ip,port", page=page)  # 获取所有数据
            for data in datas["results"]:
                content['data'].append(data)
    else:
        for page in range(1, int(page)+1):
            datas = login.get_data(
                quest, fields="ip,port", page=page)
            for data in datas["results"]:
                content['data'].append(data)



if content["data"] == []:
    del content["data"]
    content["error"] = "not found"
    print(content["error"])
else:

    data_dict = {}

    for data in content["data"]:
        if data[0] in data_dict.keys():
            if data[1] not in data_dict[data[0]]:
                data_dict[data[0]].append(data[1])
        else:
            data_dict[data[0]] = [data[1]]
    num = 0

    del content["data"]

    for data in data_dict.keys():
        content["data" + str(num)] = {"ip": data,"port": data_dict[data], "len": data_dict[data].__len__()}
        num += 1

    print(content)

    with open('ip_port.txt' ,"w+") as f :
        f.write("")


    for key in content.keys():
        IP = content[key]["ip"]
        for port  in content[key]["port"]:
            with open('ip_port.txt' ,"a+") as f :
                f.write( str(IP) +":"+  str(port)  + "\n")
