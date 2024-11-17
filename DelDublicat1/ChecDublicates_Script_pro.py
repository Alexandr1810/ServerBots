import threading #Лаба для интервалов и корутин
import requests #Для запросов на биток
import json #Преобразование ответа сервера в словарь питона
import time #Задержки для запросов
import re #Лаба для работы с паттернами строк
import datetime #Для работы с датой

#Переменные
Contacts_In_New = []
Contacts_In_Work = []
Contacts_In_Nedozvons = []

All_Contacts = []

Sort_Contacts_Array = []


#Функция для отправки запросов
def SendResponse(url, payload, headers):
  global response_func
  try:
    response_func = requests.request("POST", url, json=payload, headers=headers)

    # Преобразование объекта Response в строку.
    response_str = response_func.text
    try:
      # Загрузите ответ API в словарь Python.
      response_dict = json.loads(response_str)
    except (JSONDecodeError, json.JSONDecodeError):
      response_dict = {}
    
  except requests.exceptions.RequestException:  # любая ошибка requests
    print('ConnectionError')
  

  # Пример работы с JSON: print(response_dict['result'][0]['ID'])

  #Возвращаем словарь в переменную
  return response_dict





def Get_New_Deals():
  global Contacts_In_New
  response = SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.list", {"filter": {"STAGE_ID": "NEW"},"select": ["CONTACT_ID", "STAGE_ID"],"start": "0"}, {"cookie": "qmb=0.","Content-Type": "application/json","User-Agent": "insomnia/8.5.1"})
  
  Contacts_In_New = response["result"]

  if response["total"] > 50:
    for i in range(51, response["total"], 50): 
      response = SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.list", {"filter": {"STAGE_ID": "UC_0SAOJL"},"select": ["CONTACT_ID", "STAGE_ID"],"start": str(i)}, {"cookie": "qmb=0.","Content-Type": "application/json","User-Agent": "insomnia/8.5.1"})
      Contacts_In_New = Contacts_In_New + response["result"]

  print("Новые:", Contacts_In_New)
  print("Длинна:", len(Contacts_In_New))
  print()
  Get_InWork_Deals()

def Get_InWork_Deals():
  global Contacts_In_Work
  response = SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.list", {"filter": {"STAGE_ID": "PREPARATION"},"select": ["CONTACT_ID", "STAGE_ID"],"start": "0"}, {"cookie": "qmb=0.","Content-Type": "application/json","User-Agent": "insomnia/8.5.1"})
  
  Contacts_In_Work = response["result"]

  print("В работе:", Contacts_In_Work)
  print("Длинна:", len(Contacts_In_Work))
  print()
  Get_Nedozvon_Deals()

def Get_Nedozvon_Deals():
  global Contacts_In_Nedozvons
  response = SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.list", {"filter": {"STAGE_ID": "UC_0SAOJL"},"select": ["CONTACT_ID", "STAGE_ID"],"start": "0"}, {"cookie": "qmb=0.","Content-Type": "application/json","User-Agent": "insomnia/8.5.1"})
  
  Contacts_In_Nedozvons = response["result"]

  if response["total"] > 50:
    for i in range(51, response["total"], 50): 
      response = SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.list", {"filter": {"STAGE_ID": "UC_0SAOJL"},"select": ["CONTACT_ID", "STAGE_ID"],"start": str(i)}, {"cookie": "qmb=0.","Content-Type": "application/json","User-Agent": "insomnia/8.5.1"})
      Contacts_In_Nedozvons = Contacts_In_Nedozvons + response["result"]

  print("Недозвоны:", Contacts_In_Nedozvons)
  print("Длинна:", len(Contacts_In_Nedozvons))
  print()
  UnificationArray()

def UnificationArray():
  global Contacts_In_New
  global Contacts_In_Work
  global Contacts_In_Nedozvons

  global All_Contacts

  All_Contacts = Contacts_In_New + Contacts_In_Work + Contacts_In_Nedozvons

  print("Все сделки:", All_Contacts)
  print("Длинна:", len(All_Contacts))
  print()
  Find_Duplicates()

def Find_Duplicates():
  global Contacts_In_New
  global Contacts_In_Work
  global Contacts_In_Nedozvons
  
  global All_Contacts

  global Sort_Contacts_Array


  # Словарь для группировки по CONTACT_ID
  grouped_contacts = {}

  # Группируем контакты
  for contact in All_Contacts:
      contact_id = contact['CONTACT_ID']
      if contact_id not in grouped_contacts:
          grouped_contacts[contact_id] = []
      grouped_contacts[contact_id].append(contact)

  # Отбираем только те группы, которые содержат дубликаты
  Sort_Contacts_Array = [contacts for contacts in grouped_contacts.values() if len(contacts) > 1]

  # Определяем порядок сортировки STAGE_ID
  stage_order = {'UC_0SAOJL': 0, 'NEW': 1, 'PREPARATION': 2}

  # Сортируем вложенные массивы по STAGE_ID
  for contacts in Sort_Contacts_Array:
      contacts.sort(key=lambda contact: stage_order[contact['STAGE_ID']])

  print("Сортированный массив из дубликатов: ", Sort_Contacts_Array)
  print("Длинна:", len(Sort_Contacts_Array))
  Delete_Dublicates(Sort_Contacts_Array)



def Delete_Dublicates(contacts_array):
  for contacts in contacts_array:
    # Проверяем, есть ли больше одной сделки
    if len(contacts) > 1:
      # Проходим по всем, кроме последней сделки
      for contact in contacts[:-1]:
        id_deal = contact['ID']
        stage_id = contact['STAGE_ID']
        print(f"Я удалил сделку {id_deal} из стадии {stage_id}")

        SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.update", {"id": id_deal,"fields": {"UF_CRM_1694601072": "5586","STAGE_ID": "UC_93XIL7"}}, {"cookie": "qmb=0.", "Content-Type": "application/json","User-Agent": "insomnia/8.6.0"})

        SendResponse("https://api.telegram.org/bot6881870667:AAEtWo3EkLw6HqsjdLxbY0eJwt1Y_Uqr8io/sendMessage", 
          {
            "chat_id": "1395354115",
            "text": "Заявка "+id_deal+" удалена как Дубликат роботом из стадии"+stage_id
          }, {"Content-Type": "application/json","User-Agent": "insomnia/8.5.1"})
  Final()

def Final():
  global Contacts_In_New
  global Contacts_In_Work
  global Contacts_In_Nedozvons
  
  global All_Contacts

  global Sort_Contacts_Array

  Contacts_In_New = []
  Contacts_In_Work = []
  Contacts_In_Nedozvons = []

  All_Contacts = []

  Sort_Contacts_Array = []
  print("Очистил данные, Жду следующего цикла")
  current_datetime = datetime.datetime.now()
  print("Закончил: ", current_datetime)





#Вызываю основные функции в интерале 5мин (180сек)

def printit():
  global Contacts_In_New
  global Contacts_In_Work
  global Contacts_In_Nedozvons
  
  global All_Contacts

  global Sort_Contacts_Array

  Contacts_In_New = []
  Contacts_In_Work = []
  Contacts_In_Nedozvons = []
  
  current_datetime = datetime.datetime.now()
  print("Начал: ", current_datetime)


  Get_New_Deals()
  threading.Timer(300, printit).start()
printit()