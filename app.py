import requests
import random
import glob
import json
import time
import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

config = configparser.ConfigParser()
config.read('app_settings.ini')


def checkUserFile():
    with open("userlist.json", "r") as read_file:
        user = json.load(read_file)
    if len(user['users']) <= 10:
        os.system("python3 userloader.py 1")
        time.sleep(3)

def sendMessage(token, user, message):
    pass
    #print(token, user, message)
    print("--------------------------------------------------")
    print(message + " to " + user)
    print("--------------------------------------------------")

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
    try:
        with open("userlist.json", "r") as read_file:
            user = json.load(read_file)
        #print(type(user['users']))

        del user['users'][0]
        #data = {"users":user['users'].remove(user['users'][0])}
        data = {"users":user['users']}
        print(data)
        with open("userlist.json", "w") as write_file:
            json.dump(data, write_file)
    except:
        os.system("python3 userloader.py 1")
        time.sleep(3)
        if(len(user['users']) == 0):
            print('\n')
            print('Ошибка в работе подгрузчика пользователей. Файл с пользователями пуст.')
            print('\n')
        else:
            print('\n')
            print('Не удалось найти идентификатор получателя сообщения в файле. Убедитесь в наличии и правильном формате файла "userlist.json"')
            print('\n')
    return str(user['users'][0]['id'])

def program():
    try:
        tokens = config.get("Settings", "token").split(',')
        checkUserFile()
        for token in tokens:
            #print("|"+token+"|")
            user = str(getUser())
            message = str(getMessage())

            sendMessage(token.replace(" ", ""), user, message)
    except:
        print("Цикл рассылки завершен с ошибкой, просим ознакомиться с деталями.")
    else:
        pass
        print("Цикл рассылки завершен успешно.")
        print("________/\___________/\_________")
    finally:
        time.sleep(3)
        program()
program()
