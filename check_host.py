#!/usr/bin/python
import socket
import requests
import time
import datetime
import json
# -*- coding:utf-8 -*-

def checkhost(host,port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(4)
        client.connect((host, port)) 
        #client.send(data) 
        response = client.recv(1024) 
        client.close()
        return response
    except socket.error as e:
        return False

def sendMessageToDiscord(url,messages):
    try:
        payload = {'content': messages}
        r = requests.post(url, payload)
        return r
    except socket.error as e:
        return False
def readchecklist():
    try:
        f = open('check_config.json', 'r')
        json_data = json.load(f)
        f.close()
        return json_data
    except:
        return {}

config_a = readchecklist()
discord_webhook = config_a['webhook']
checklist_a = config_a['targets']
targets_dic = {}

for key in checklist_a:
    host_a = key.split(':')
    host = host_a[0]
    port = int(host_a[1])

    dt_now = datetime.datetime.now()
    now_str = (dt_now.strftime('%Y-%m-%d %H:%M:%S'))+": "
    ret = checkhost(host,port)
    if ret==False:
        #Host is down
        targets_dic[key] = str(int(checklist_a[key]) + 1)
        if int(checklist_a[key]) == 2:
            #Host was up before
            sendMessageToDiscord(discord_webhook,now_str+"Host Down " + key)
    else:
        #Host is up
        targets_dic[key] = "0"
        if int(checklist_a[key]) >= 2:
            #Host was down before
            sendMessageToDiscord(discord_webhook,now_str+"Host Up " + key)
out_json_a={'targets':targets_dic}
out_json_a.update({'webhook':discord_webhook})
f = open('check_config.json','w')
json.dump(out_json_a,f,indent=4)
f.close()
