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
config.read('settings.ini')

def sendMessage(token, user, message):
    print(token, user, message)


def getMessage():
    try:
        messageList =[]
        fileList = glob.glob("*.txt")
        for file in fileList:
            if "message" in file:
                messageList.append(file)

        f = open(random.choice(messageList), "rb")
        message = f.read()
        f.close()

    except Exception as e:
        if(len(messageList) == 0):
            print("\n")
            print("Создайте файл ''message1.txt'' и поместите в него текст сообщения, которое будет отправлять бот. Файлов с сообщениями можно создавать любое количество, бот будет выбирать их случайным образом. Сообщение может иметь любое название, но обязательно должно содержать ключевое слово ''message'' и иметь расширение ''.txt>''")
            print("\n")
        else:
            print("\n")
            print("Ошибка. Проверьте файлы с сообщениями на наличие подозрительных символов или присутствия нестандартной кодировки файла.")
            print("\n")
        f.close()
        pass

    return message

def getUser():
    with open("userlist.json", "r") as read_file:
        user = json.load(read_file)

    data = {"users":user['users'].remove(user['users'][0])}

    with open("userlist.json", "w") as write_file:
        json.dump(data, write_file)

    return user['users'][0]['id']

token = config.get("Settings", "token")
user = getUser()
message = getMessage()

sendMessage(token, user, message)
