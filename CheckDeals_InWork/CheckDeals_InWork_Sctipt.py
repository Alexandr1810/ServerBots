import threading #Лаба для интервалов и корутин
import requests #Для запросов на биток
import json #Преобразование ответа сервера в словарь питона
import time #Задержки для запросов
import re #Лаба для работы с паттернами строк
import datetime #Для работы с датой


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


def Get_InWork_Deals():

	respose = SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.list", {
          "filter": {"STAGE_ID": "PREPARATION"},
          "start": "0"
      }, {
          "cookie": "qmb=0.",
          "Content-Type": "application/json",
          "User-Agent": "insomnia/8.5.1"
      })
    
	print('REST (В работе):', respose['result'])
	for x in respose['result']:
		print("----")
		print()
		print("Сделка:", x["ID"], "висит в работе на Агенте:", x["ASSIGNED_BY_ID"])
		print()

		AgentDeportament = SendResponse("https://speedinet.bitrix24.ru/rest/26/48qmdec3obtu7b6w/user.get", {"id": x["ASSIGNED_BY_ID"]}, {
			"cookie": "qmb=0.",
			"Content-Type": "application/json",
			"User-Agent": "insomnia/9.3.2"
		})

		print("Агент", x["ASSIGNED_BY_ID"], "состоит в депортаменте", AgentDeportament["result"][0]["UF_DEPARTMENT"][0])
		print()

		match AgentDeportament["result"][0]["UF_DEPARTMENT"][0]:
			case 30:
				print("Определен подходящий депортамент Команда Никиты")
				print()
			case 32:
				print("Определен подходящий депортамент Команда Ильи")
				print()
			case 3:
				print("Определен подходящий депортамент Call Центр")
				print()
			case 10:
				print("Определен подходящий депортамент Менеджеры")
				print()
			case _:
				print("Подходящий депортамент не найден!")
				print()
				print("Перевожу заявку", x["ID"], "в Новые!")
				print()
				SendToNew = SendResponse("https://speedinet.bitrix24.ru/rest/26/qzz79qlepr8oxwmk/crm.deal.update", {
					"id": x["ID"],
					"fields": {
						"STAGE_ID": "NEW"
					}
				}, {
					"cookie": "qmb=0.",
					"Content-Type": "application/json",
					"User-Agent": "insomnia/9.3.2"
				})
				print("Готово!")
	current_datetime = datetime.datetime.now()
	print("Закончил: ", current_datetime)


#Вызываю основные функции в интерале 3мин (180сек)
def printit():
	current_datetime = datetime.datetime.now()
	print("Начал: ", current_datetime)

	Get_InWork_Deals()
	threading.Timer(180, printit).start()

printit()