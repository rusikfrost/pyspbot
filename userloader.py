import requests
import random
from random import randrange
import glob
import json
import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

config = configparser.ConfigParser()
config.read('app_settings.ini')
token = config.get("Settings", "token")

config.read('userloader_settings.ini')
group = config.get("SettingsLoader", "group_for_unload_users")
count = config.get("SettingsLoader", "count")

sex = config.get("SettingsLoader", "sex")
bdateFrom = config.get("SettingsLoader", "bdateFrom")
bdateTo = config.get("SettingsLoader", "bdateTo")
city = config.get("SettingsLoader", "city")
last_seen = config.get("SettingsLoader", "last_seen")

def getGroup(token, group):
    group = group.replace("-", "")
    method = "method=groups.getById"
    group_id = "group_id="+group
    fields = "fields=members_count"
    print(group)
    r = requests.post("https://api.vk.com/api.php?oauth=1&"+method+"&"+group_id+"&"+fields+"&v=5.67&access_token="+token)
    print(r.json())
    members_count = r.json()['response'][0]['members_count']
    if(int(members_count) < 20000):
        print("Сообщество "+r.json()['response'][0]['members_count']+ " имеет небольшое количество подписчиков, рекомендуется повысить охват целевой аудитории.")
    #print(members_count)
    return members_count

def getUsers(token, group, members_count, count):
    group = group.replace("-", "")
    offset = "offset="+str(randrange(int(members_count)-int(count)))
    print(offset)
    method = "method=groups.getMembers"
    group_id = "group_id="+group
    count = "count="+count

    fields = "fields=can_write_private_message,sex,bdate,city,last_seen"
    r = requests.post("https://api.vk.com/api.php?oauth=1&"+method+"&"+group_id+"&"+offset+"&"+fields+"&"+count+"&v=5.67&access_token="+token)
    print(r.json())
    return r.json()['response']['items']

def checkUsers(members, sex, bdateFrom, bdateTo, city, last_seen):
    users = []
    for member in members:
        if(member['can_write_private_message'] == 1):

            if(sex != "" and sex != str(member['sex'])): continue
            if(city != "" and city != str(member['city']['title'])): continue

            users.append(member['id'])
            #if()
            #try: print(member['bdate'])
            #except: continue
    return users

def writeUsers(users):
    print(users)
    data = {"users":users}

    with open("userlist.json", "w") as write_file:
        json.dump(data, write_file)

members_count = getGroup(token, group)
members = getUsers(token, group, members_count, count)
ready_users = checkUsers(members, sex, bdateFrom, bdateTo, city, last_seen)
writeUsers(ready_users)
