import threading #Лаба для интервалов и корутин
import requests #Для запросов на биток
import json #Преобразование ответа сервера в словарь питона
import time #Задержки для запросов
import re #Лаба для работы с паттернами строк
import datetime #Для работы с датой
import pickle

its_okey = True
 
#Функция для отправки запросов
def GetResponse(url, headers):
  response_func = requests.request("GET", url, headers=headers)
  # Преобразование объекта Response в строку.
  response_str = response_func.text
  try:
    response_dict = json.loads(response_str)
  except (JSONDecodeError, json.JSONDecodeError):
    response_dict = {}

  return response_dict


def ChecUnix():
    global its_okey

    currentUnix = int(time.time())
    
    savedUnixArr = GetResponse("https://66cea2c0901aab24841f06e7.mockapi.io/BotsUnix/", {
        "Content-Type": "application/json",
        "User-Agent": "insomnia/9.3.2"
    })
    
    
    for x in savedUnixArr:
        savedUnix = int(x["Unix"])
        print(f"currentUnix: {currentUnix} \nsavedUnix: {savedUnix}")

        if ((currentUnix - savedUnix) >= 1800):
            SendToChat = GetResponse("https://api.telegram.org/bot6471375015:AAGrXnRtslswCg6E1pzCzjkWGqnbjBWXBpc/sendMessage?chat_id=-4178861179&text=" + x["StartText"]+str(int((currentUnix - savedUnix)/60))+x["ClousedText"], {
                "Content-Type": "application/json",
                "User-Agent": "insomnia/8.5.1"
            })
            print(x["StartText"]+str(int((currentUnix - savedUnix)/60))+x["ClousedText"])
            its_okey = False
        else:
            print(f"Все работает, последняя активность: {savedUnix} !")
            if its_okey == False:
                SendToChat = GetResponse("https://api.telegram.org/bot7615326954:AAHqHflEsE23bwfLZqYuBWNhgs6iaLxjfIA/sendMessage?chat_id=1395354115&text=" + x["OkeyText"], {
                    "Content-Type": "application/json",
                    "User-Agent": "insomnia/8.5.1"
                })
                its_okey = True
                print(x["OkeyText"])
        

#Вызываю основные функции в интерале 10мин (600сек)
def printit():
  print("")
  current_datetime = datetime.datetime.now()
  print("Начал: ", current_datetime)
  print("")

  ChecUnix()
  threading.Timer(600, printit).start()

printit()