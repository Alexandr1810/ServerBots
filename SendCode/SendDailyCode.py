import threading #Лаба для интервалов и корутин
import requests #Для запросов на биток
import json #Преобразование ответа сервера в словарь питона
import time #Задержки для запросов
import re #Лаба для работы с паттернами строк
import datetime #Для работы с датой
import random

random_index1 = random.randint(0, 39)
random_index2 = random.randint(0, 39)
random_index3 = random.randint(0, 39)
random_index4 = random.randint(0, 39)
random_index5 = random.randint(0, 39)
random_index6 = random.randint(0, 39)
random_index7 = random.randint(0, 39)
random_index8 = random.randint(0, 39)
random_index9 = random.randint(0, 39)
random_index10 = random.randint(0, 39)
random_index11 = random.randint(0, 39)

random_int1 = random.randint(1000, 9999)
random_int2 = random.randint(100, 300)
random_int3 = random.randint(567, 867)

symbols_arr = ['f', 'd', 'rt', 'f', 'g', 'h', 'j', 't', '-', 'k', 'f', 'm', '&', 'df', '=', 'dy', '?', 'п', '3', 'а+', '+', 'р', 'л', 'в', 'ц', 'а', 'ь', '%', 'l', 'i', ',', 'g', ')', '(', 'b', 'c', 'z', '.', 'u', '*']

random_str = symbols_arr[random_index1] + symbols_arr[random_index2] + symbols_arr[random_index3] + str(random_int1) + symbols_arr[random_index4] + symbols_arr[random_index5] + symbols_arr[random_index6] + str(random_int2) + symbols_arr[random_index7] + symbols_arr[random_index8] + str(random_int3) + symbols_arr[random_index9] + symbols_arr[random_index10] + symbols_arr[random_index11]

print(random_str)

#Переменные
Deals_For_Check = []
Not_Sort_Deals_Array = []
DealId_To_Send = ''

#Функция для отправки запросов
def SendResponse(url, headers):
  response_func = requests.request("GET", url, headers=headers)
  # Преобразование объекта Response в строку.
  response_str = response_func.text

  # Загрузите ответ API в словарь Python.
  response_dict = json.loads(response_str)

  # Пример работы с JSON: print(response_dict['result'][0]['ID'])

  #Возвращаем словарь в переменную
  return response_dict

#Функция для отправки запросов
def SendKeyToBot(url, payload, headers):
  response_func = requests.request("POST", url, json=payload, headers=headers)
  # Преобразование объекта Response в строку.
  response_str = response_func.text

  # Загрузите ответ API в словарь Python.
  response_dict = json.loads(response_str)

  # Пример работы с JSON: print(response_dict['result'][0]['ID'])

  #Возвращаем словарь в переменную
  return response_dict

#Функция для отправки запросов
def PutDateInApi(url, payload, headers):
  response_func = requests.request("PUT", url, json=payload, headers=headers)
  # Преобразование объекта Response в строку.
  response_str = response_func.text

  # Загрузите ответ API в словарь Python.
  response_dict = json.loads(response_str)

  # Пример работы с JSON: print(response_dict['result'][0]['ID'])

  #Возвращаем словарь в переменную
  return response_dict

def CheckDay():

  #Получаю текущий день и месяц

  current_datetime = datetime.datetime.now()

  current_day = int(current_datetime.day)

  current_month = int(current_datetime.month)

  #Получаю день и месяц сохраненный в API
  respose = SendResponse("https://656de619bcc5618d3c242ec1.mockapi.io/MyPartners/EISSD_Pass/1", {
    "Content-Type": "application/json",
    "User-Agent": "insomnia/9.3.2"
  })
  ApiDay = int(respose["LoginDate"])
  ApiMonth = int(respose["LoginMounth"])


  print("День в API: ", ApiDay)
  print("Месяц в API: ", ApiMonth)
  print("Текущий день: ", current_day)
  print("Текущий Месяц: ", current_month)

  if ((ApiDay < current_day) and (current_month == ApiMonth)) or ((ApiDay > current_day) and (current_month != ApiMonth)):
    print("Отправляю код, меняю день и месяц")
    random_index1 = random.randint(0, 39)
    random_index2 = random.randint(0, 39)
    random_index3 = random.randint(0, 39)
    random_index4 = random.randint(0, 39)
    random_index5 = random.randint(0, 39)
    random_index6 = random.randint(0, 39)
    random_index7 = random.randint(0, 39)
    random_index8 = random.randint(0, 39)
    random_index9 = random.randint(0, 39)
    random_index10 = random.randint(0, 39)
    random_index11 = random.randint(0, 39)

    random_int1 = random.randint(1000, 9999)
    random_int2 = random.randint(100, 300)
    random_int3 = random.randint(567, 867)


    random_str = symbols_arr[random_index1] + symbols_arr[random_index2] + symbols_arr[random_index3] + str(random_int1) + symbols_arr[random_index4] + symbols_arr[random_index5] + symbols_arr[random_index6] + str(random_int2) + symbols_arr[random_index7] + symbols_arr[random_index8] + str(random_int3) + symbols_arr[random_index9] + symbols_arr[random_index10] + symbols_arr[random_index11]

    print(random_str)

    SendKeyToBot("https://api.telegram.org/bot6772388598:AAGgg0BDIwVE7jAbzxi4WjL7dw_aL8kgnaU/sendMessage", 
      {
        "chat_id": "-1002064816512",
        "text": "Код на сегодня: `"+random_str+"`",
        "parse_mode": "MARKDOWN"
      }, {"Content-Type": "application/json","User-Agent": "insomnia/8.5.1"})

    PutDateInApi("https://656de619bcc5618d3c242ec1.mockapi.io/MyPartners/EISSD_Pass/1", {
      "LoginDate": current_day,
      "LoginMounth": current_month,
      "LoginCode": random_str

    }, {
      "Content-Type": "application/json",
      "User-Agent": "insomnia/9.3.2"
    })

  else:
    print("Ничего не делаю")
  
  current_datetime = datetime.datetime.now()
  print("Закончил: ", current_datetime)



#Вызываю основные функции в интерале 2мин (120сек)
def printit():
  print("Начинаю Шаманить!")
  current_datetime = datetime.datetime.now()
  print("Начал: ", current_datetime)

  CheckDay()
  threading.Timer(1800, printit).start()

printit()