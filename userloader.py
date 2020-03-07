import requests
import random
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

def getUsers(token, group):
    if(not "-" in group): "-"+group
    method = "method=groups.getMembers"
    group_id = "group_id="+group
    count = "count=2"
    fields = "fields=can_write_private_message,sex,bdate,city,last_seen"
    r = requests.post("https://api.vk.com/api.php?oauth=1&"+method+"&"+group_id+"&"+fields+"&"+count+"&v=5.67&access_token="+token)
    print(r.json())

getUsers(token, group)
