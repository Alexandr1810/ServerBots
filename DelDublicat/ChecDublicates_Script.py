import threading #Лаба для интервалов и корутин
import requests #Для запросов на биток
import json #Преобразование ответа сервера в словарь питона
import time #Задержки для запросов
import re #Лаба для работы с паттернами строк
import datetime #Для работы с датой

#Переменные
Deals_For_Check = []
Not_Sort_Deals_Array = []
DealId_To_Send = ''

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
  global Not_Sort_Deals_Array
  #1. Получаем все ID Новых заявок
  try:
    Deals_For_Check.clear()
    Not_Sort_Deals_Array.clear()
    DealId_To_Send = ''
    print("Deals_For_Check: ", Deals_For_Check)
    print("Not_Sort_Deals_Array: ", Not_Sort_Deals_Array)
    print("DealId_To_Send: ", DealId_To_Send)
    respose = SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.list", {
          "filter": {"STAGE_ID": "NEW"},
          "start": "0",
          "select": ["ID"]
      }, {
          "cookie": "qmb=0.",
          "Content-Type": "application/json",
          "User-Agent": "insomnia/8.5.1"
      })
    
    print('REST (Новые):', respose['result'])
    
    print()

    for i in range(len(respose['result'])):
      Deals_For_Check.append(respose['result'][i]['ID'])


    if respose['total'] > 49:
      try:
        respose = SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.list", {
          "filter": {"STAGE_ID": "NEW"},
          "start": "50",
          "select": ["ID"]
        }, {
            "cookie": "qmb=0.",
            "Content-Type": "application/json",
            "User-Agent": "insomnia/8.5.1"
        })
      except requests.exceptions.Timeout:
        print("Timeout occurred")
      for i in range(len(respose['result'])):
        Deals_For_Check.append(respose['result'][i]['ID'])

      print('Deals_For_Check (Новые)', Deals_For_Check)
      print()
      Get_InWork_Deals();

    else:
      print('Deals_For_Check (Новые)', Deals_For_Check)
      print()
      Get_InWork_Deals();

  except KeyError as e:
    print('I got a KeyError - reason "%s"' % str(e))
  except IndexError as e:
    print('I got an IndexError - reason "%s"' % str(e))

def Get_InWork_Deals():
  global Not_Sort_Deals_Array
  #2. Получаем все ID заявок в работе
  try:
    respose = SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.list", {
          "filter": {"STAGE_ID": "PREPARATION"},
          "start": "0",
          "select": ["ID"]
      }, {
          "cookie": "qmb=0.",
          "Content-Type": "application/json",
          "User-Agent": "insomnia/8.5.1"
      })
    
    
    print('REST (в работе):', respose['result'])
    
    print()
    for i in range(len(respose['result'])):
      Deals_For_Check.append(respose['result'][i]['ID'])

    print('Deals_For_Check (Новые, В работе)', Deals_For_Check)
    print()
    Get_Nedozvon_Deals()

  except KeyError as e:
    print('I got a KeyError - reason "%s"' % str(e))
  except IndexError as e:
    print('I got an IndexError - reason "%s"' % str(e))

def Get_Nedozvon_Deals():
  global Not_Sort_Deals_Array
  #3. Получаем все ID Недозвонов
  try:
    respose = SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.list", {
          "filter": {"STAGE_ID": "UC_0SAOJL"},
          "start": "0",
          "select": ["ID"]
      }, {
          "cookie": "qmb=0.",
          "Content-Type": "application/json",
          "User-Agent": "insomnia/8.5.1"
      })
    

    try:
      print('REST (Недозвоны):', respose['result'])
    except KeyError as e:
      print('I got a KeyError - reason "%s"' % str(e))
    except IndexError as e:
      print('I got an IndexError - reason "%s"' % str(e))
    print()
    for i in range(len(respose['result'])):
      Deals_For_Check.append(respose['result'][i]['ID'])


    if respose['total'] > 49:
      try:
        respose = SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.list", {
          "filter": {"STAGE_ID": "UC_0SAOJL"},
          "start": "50",
          "select": ["ID"]
        }, {
            "cookie": "qmb=0.",
            "Content-Type": "application/json",
            "User-Agent": "insomnia/8.5.1"
        })
      except requests.exceptions.Timeout:
        print("Timeout occurred")
      for i in range(len(respose['result'])):
        Deals_For_Check.append(respose['result'][i]['ID'])

      print('Deals_For_Check (Новые, В работе, Недозвоны)', Deals_For_Check)
      print()
      time.sleep(1) 
      Get_Deals_Data()

    else:
      print('Deals_For_Check (Новые, В работе, Недозвоны)', Deals_For_Check)
      print()
      time.sleep(1) 
      Get_Deals_Data()
    
  except KeyError as e:
    print('I got a KeyError - reason "%s"' % str(e))
  except IndexError as e:
    print('I got an IndexError - reason "%s"' % str(e))

def Get_Deals_Data():
  #4. Получаем необходимые данные по сделке (Номер и Местрику)
  global Not_Sort_Deals_Array
  print(len(Deals_For_Check))
  for i in range(len(Deals_For_Check)):
    respose = SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.get", {"id": Deals_For_Check[i]}, {
          "cookie": "qmb=0.",
          "Content-Type": "application/json",
          "User-Agent": "insomnia/8.5.1"
      })
    
    print()
    print('------- Сделка', i, ' из ', len(Deals_For_Check))
    print()
    print('REST (Данные по сделке):', respose)
    try:
      if respose['result']['UF_CRM_1604651268'] != '111':
        Not_Sort_Deals_Array.append([respose['result']['ID'], respose['result']['UTM_SOURCE'], respose['result']['UF_CRM_1604651268'], respose['result']['STAGE_ID']])
      else:
        print()
        print("Встретил исключение '111', пропускаю")
        print()
    except KeyError as e:
      print('I got a KeyError - reason "%s"' % str(e))
    except IndexError as e:
      print('I got an IndexError - reason "%s"' % str(e))
        
    #Добавил задержку в 200мс, что-бы не частить запросами
    time.sleep(0.2)
    #Not_Sort_Deals_Array += []

  print()
  print("Все запросы завершены: ", Not_Sort_Deals_Array)
  Replace_Numbers_To_Pattern()


def Replace_Numbers_To_Pattern():
  #5. Получаем необходимые данные по сделке (Номер и Местрику)
  global Not_Sort_Deals_Array
  
  for i in range(len(Not_Sort_Deals_Array)):
    Not_Sort_Deals_Array[i][0] = re.sub(r'[^0-9]', '', Not_Sort_Deals_Array[i][0])
    if Not_Sort_Deals_Array[i][0][0] == '7':
      Not_Sort_Deals_Array[i][0] = Not_Sort_Deals_Array[i][0].replace("7", "")

    elif Not_Sort_Deals_Array[i][0][0] == '8':
      Not_Sort_Deals_Array[i][0] = Not_Sort_Deals_Array[i][0].replace("8", "")

  print()
  print("Все номера приведены к паттерну: ", Not_Sort_Deals_Array)
  Sort_Matrix()

def Sort_Matrix():
  '''
  6. Имея матрицу:
  Not_Sort_Deals_Array =  [
    ['12345', 'per-set', '79233024909', 'NEW'],
    ['12349', 'per-set', '79233024909', 'PREPARATION'],
    ['12346', 'dom.ru', '79012064151', 'PREPARATION'],
    ['12347', 'per-set', '79012064151', 'NEW'],
    ['12348', 'SpeedInet', '79029592377', 'NEW'],
    ['12350', 'SpeedInet', '79029592377', 'UC_0SAOJL'],
    ['12350', 'Izet', '79239414565', 'UC_0SAOJL']
  ]
  Сортируем ее так, что бы получить только заявки с повторяющимися номерами и разной метрикой
  [
    ['12345', 'per-set', '79233024909', 'NEW'],
    ['12349', 'per-set', '79233024909', 'PREPARATION'],
    ['12348', 'SpeedInet', '79029592377', 'NEW'],
    ['12350', 'SpeedInet', '79029592377', 'UC_0SAOJL']
  ]
*/
  /*
  var Not_Sort_Deals_Array =  [
    ['12345', 'per-set', '79233024909', 'NEW'],
    ['12349', 'per-set', '79233024909', 'PREPARATION'],
    ['12346', 'dom.ru', '79012064151', 'PREPARATION'],
    ['12347', 'per-set', '79012064151', 'NEW'],
    ['12348', 'SpeedInet', '79029592377', 'NEW'],
    ['12350', 'SpeedInet', '79029592377', 'UC_0SAOJL'],
    ['12351', 'Izet', '79239414565', 'UC_0SAOJL']
  ]
  '''
  global Not_Sort_Deals_Array
  global DublicateMatrix

  repeatedRequests = []
  DublicateMatrix = []
  InArrayIndicator = False

  for i in range(len(Not_Sort_Deals_Array)):
    for j in range(len(Not_Sort_Deals_Array)):
      if Not_Sort_Deals_Array[i][2] == Not_Sort_Deals_Array[j][2] and Not_Sort_Deals_Array[i][1] == Not_Sort_Deals_Array[j][1] and Not_Sort_Deals_Array[i][0] != Not_Sort_Deals_Array[j][0]:
        print("Сделки совпали")
        for k in range(len(repeatedRequests)):
          #print("Сравниваю", repeatedRequests[i], "и", Not_Sort_Deals_Array[i])
          if repeatedRequests[k][0] == Not_Sort_Deals_Array[i][0]:
            print("совпалость")
            InArrayIndicator = True
          
        
        if InArrayIndicator == False:

          repeatedRequests.append(Not_Sort_Deals_Array[i])
        
        else:
          InArrayIndicator = False;
        
  # Словарь для группировки по номеру телефона
  grouped_data = {}
  for row in repeatedRequests:
      phone = row[2]  # Получаем номер телефона
      if phone not in grouped_data:
          grouped_data[phone] = []
      grouped_data[phone].append(row)

  # Преобразуем словарь в список списков
  DublicateMatrix = list(grouped_data.values())


  print("Дубликаты с одной метрикой: ", repeatedRequests);
  print("Дубликаты с одной метрикой после сортировки: ", DublicateMatrix);
  Delete_Dublicates()

def Delete_Dublicates():
  #7. Через API кидаем все заявки из второй матрицы на удаление с признаком "Дубликат"

  global Not_Sort_Deals_Array
  global DublicateMatrix
  global DealId_To_Send

  for deals in DublicateMatrix:
    # Проверяем, есть ли больше одной сделки
    print("deals", deals)
    for deal in deals[:-1]:
      print("deal", deal)
      id_deal = deal[0]
      phone = deal[2]
      stage_id = deal[3]
      print(f"Я удалил сделку {id_deal} с номером {phone} из стадии {stage_id}")

      SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.update", {"id": id_deal,"fields": {"UF_CRM_1694601072": "5586","STAGE_ID": "UC_93XIL7"}}, {"cookie": "qmb=0.", "Content-Type": "application/json","User-Agent": "insomnia/8.6.0"})

      SendResponse("https://api.telegram.org/bot6881870667:AAEtWo3EkLw6HqsjdLxbY0eJwt1Y_Uqr8io/sendMessage", 
      {
        "chat_id": "1395354115",
        "text": "Заявка "+id_deal+" с номером "+phone+" удалена как Дубликат роботом из стадии"+stage_id
      }, {"Content-Type": "application/json","User-Agent": "insomnia/8.5.1"})


  print("")
  print("Завершил работу, очищаю данные.")

  Deals_For_Check.clear()
  Not_Sort_Deals_Array.clear()
  DealId_To_Send = ''

  print("Deals_For_Check: ", Deals_For_Check)
  print("Not_Sort_Deals_Array: ", Not_Sort_Deals_Array)
  print("DealId_To_Send: ", DealId_To_Send)

  print("Очистил данные, Жду следующего цикла")
  current_datetime = datetime.datetime.now()
  print("Закончил: ", current_datetime)





#Вызываю основные функции в интерале 2мин (120сек)
def printit():
  current_datetime = datetime.datetime.now()
  print("Начал: ", current_datetime)


  Get_New_Deals()
  threading.Timer(180, printit).start()

printit()