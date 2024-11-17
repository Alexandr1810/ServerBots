import threading #Лаба для интервалов и корутин
import requests #Для запросов на биток
import json #Преобразование ответа сервера в словарь питона
import time #Задержки для запросов
import re #Лаба для работы с паттернами строк
import datetime #Для работы с датой
import pickle
import pytz #Часовые пояса

update_id = 732199299
# Получаем
with open('data_1.sav', 'rb') as f:
  update_id = pickle.load(f)
print("update_id", update_id)

# Определяем московский часовой пояс
moscow_tz = pytz.timezone("Europe/Moscow")


#Функция для отправки запросов
def GetResponse(url, headers):
  response_func = requests.request("GET", url, headers=headers)
  # Преобразование объекта Response в строку.
  response_str = response_func.text
  try:
    response_dict = json.loads(response_str)
  except (JSONDecodeError, json.JSONDecodeError):
    response_dict = {}
  # Загрузите ответ API в словарь Python.
  

  # Пример работы с JSON: print(response_dict['result'][0]['ID'])

  #Возвращаем словарь в переменную
  return response_dict

#Функция для отправки запросов
def PutResponse(url, payload, headers):
  response_func = requests.request("PUT", url, json=payload, headers=headers)
  # Преобразование объекта Response в строку.
  response_str = response_func.text
  try:
    response_dict = json.loads(response_str)
  except (JSONDecodeError, json.JSONDecodeError):
    response_dict = {}
  # Загрузите ответ API в словарь Python.
  

  # Пример работы с JSON: print(response_dict['result'][0]['ID'])

  #Возвращаем словарь в переменную
  return response_dict

#Функция для отправки запросов
def PostResponse(url, payload, headers):
  response_func = requests.request("POST", url, json=payload, headers=headers)
  # Преобразование объекта Response в строку.
  response_str = response_func.text
  try:
    response_dict = json.loads(response_str)
  except (JSONDecodeError, json.JSONDecodeError):
    response_dict = {}
  # Загрузите ответ API в словарь Python.
  

  # Пример работы с JSON: print(response_dict['result'][0]['ID'])

  #Возвращаем словарь в переменную
  return response_dict

#Функция для отправки запросов
def DeleteResponse(url, headers):
  response_func = requests.request("DELETE", url, headers=headers)
  # Преобразование объекта Response в строку.
  response_str = response_func.text
  try:
    response_dict = json.loads(response_str)
  except (JSONDecodeError, json.JSONDecodeError):
    response_dict = {}
  # Загрузите ответ API в словарь Python.
  

  # Пример работы с JSON: print(response_dict['result'][0]['ID'])

  #Возвращаем словарь в переменную
  return response_dict



def Get_Api_Data():
	global update_id
	Current_Unix = time.time()
	print("Current_Unix", Current_Unix)
	print()
	
	#Получаю данные по рабочему времени из чата MOCK API
	respose = GetResponse("https://668253b204acc3545a090ff2.mockapi.io/SpeedInetBase/NoWork_Agents", {
	    "Content-Type": "application/json",
	    "User-Agent": "insomnia/9.3.2"
	})

	print("respose", respose)
	print()

	#Получаю сообщения из чата Ежедневный Отчет
	ChatItems = GetResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/getUpdates?offset="+str(update_id+1), {
	    "Content-Type": "application/json",
	    "User-Agent": "insomnia/8.6.1"
	})


	for i in ChatItems["result"]:
		try:
			print(i["message"]["text"])
			print()
			for k in respose:
				if k["user"] in i["message"]["text"]:
					print('Это отчет ', k["user"], 'id:', k["id"], 'BT_Id:', k["BT_Id"])
					print()
					print()

					PostResponse("https://speedinet.bitrix24.ru/rest/25550/92yb1mz0rkt5e2cl/timeman.close",
					{
						"user_id": k["BT_Id"]
					},
					{
				    "cookie": "qmb=0.",
				    "Content-Type": "application/json",
				    "User-Agent": "insomnia/10.1.1"
					})
		 			
					PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
						"chat_id": "-4548879553",
						"text": "Автоматически закрыл смену у Агента "+k["user"]+", Причина: Агент отправил Ежедневный отчет"
					}, {
						"Content-Type": "application/json",
						"User-Agent": "insomnia/8.5.1"
					})
		 			
					PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
						"chat_id": "-4548879553",
						"text": "Автоматически закрыл смену у Агента "+k["user"]+", Причина: Агент отправил Ежедневный отчет"
					}, {
						"Content-Type": "application/json",
						"User-Agent": "insomnia/8.5.1"
					})

					PutResponse("https://668253b204acc3545a090ff2.mockapi.io/SpeedInetBase/NoWork_Agents/"+k["id"], {"Online": False}, {
					   "Content-Type": "application/json",
					   "User-Agent": "insomnia/9.3.2"
					})

			update_id = i["update_id"]
			print('i["update_id"]: ', i["update_id"])
			

		except KeyError as e:
			print('I got a KeyError - reason ')
			print()
		except IndexError as e:
			print('I got an IndexError - reason ')
			print()


	#сохраняем
	with open('data_1.sav', 'wb') as f:
		pickle.dump(update_id, f)

	respose = GetResponse("https://668253b204acc3545a090ff2.mockapi.io/SpeedInetBase/NoWork_Agents", {
	    "Content-Type": "application/json",
	    "User-Agent": "insomnia/9.3.2"
	})

	print("respose", respose)
	print()

	for x in respose:
		if  Current_Unix - x["LastBeryClick"] >= 1200:
			Agent_Status = PostResponse("https://speedinet.bitrix24.ru/rest/25550/92yb1mz0rkt5e2cl/timeman.status",
				{
					"user_id": x["BT_Id"]
				},
				{
			    "cookie": "qmb=0.",
			    "Content-Type": "application/json",
			    "User-Agent": "insomnia/10.1.1"
			})
			Agent_Status=Agent_Status["result"]["STATUS"]

			if Agent_Status != "CLOSED" and Agent_Status != "EXPIRED":

				print(x)
				print("Сравниваю: ", Current_Unix, "и", x["LastBeryClick"], "Разница:", (Current_Unix - x["LastBeryClick"])/60/60, "часа", "Агент: ", x["Online"])
				
				if Current_Unix - x["LastBeryClick"] < 1200 and x["InIgnoreList"] == True:
					PutResponse("https://668253b204acc3545a090ff2.mockapi.io/SpeedInetBase/NoWork_Agents/"+x["id"], {"InIgnoreList": False}, {
					   "Content-Type": "application/json",
					   "User-Agent": "insomnia/9.3.2"
					})
					PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
						"chat_id": "-4548879553",
						"text": "Агент "+x["user"]+" вернулся в работу!"
					}, {
						"Content-Type": "application/json",
						"User-Agent": "insomnia/8.5.1"
					})

					print("Агент "+x["user"]+" вернулся в работу!")

				elif Current_Unix - x["LastBeryClick"] >= 1200 and Current_Unix - x["LastBeryClick"] < 3600 and Agent_Status != "PAUSED":
					"""
					PostResponse("https://speedinet.bitrix24.ru/rest/25550/92yb1mz0rkt5e2cl/timeman.pause",
						{
							"user_id": x["BT_Id"]
						},
						{
					    "cookie": "qmb=0.",
					    "Content-Type": "application/json",
					    "User-Agent": "insomnia/10.1.1"
					})

					

					PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
						"chat_id": "-1001903941079",
						"text": "Автоматически приостановил смену у Агента "+x["user"]+", Причина: Не проявляет активности более 20мин"
					}, {
						"Content-Type": "application/json",
						"User-Agent": "insomnia/8.5.1"
					})

					PutResponse("https://668253b204acc3545a090ff2.mockapi.io/SpeedInetBase/NoWork_Agents/"+x["id"], {"Online": False}, {
					   "Content-Type": "application/json",
					   "User-Agent": "insomnia/9.3.2"
					})
					"""

					PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
						"chat_id": "-4548879553",
						"text": "Автоматически приостановил смену у Агента "+x["user"]+", Причина: Не проявляет активности более 20мин"
					}, {
						"Content-Type": "application/json",
						"User-Agent": "insomnia/8.5.1"
					})

					print("Автоматически приостановил смену у Агента "+x["user"]+", Причина: Не проявляет активности более 20мин")


				elif Current_Unix - x["LastBeryClick"] >= 3600 and Current_Unix - x["LastBeryClick"] < 43200:
					# Получаем текущее время в московском часовом поясе
					moscow_time = datetime.now(moscow_tz)

					if int(moscow_time.strftime("%H")) >= 4 and int(moscow_time.strftime("%H")) <= 18:
						if x["InIgnoreList"] == True:
							if Current_Unix - x["IgnoreUnix"] >= 3600:
								PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
									"chat_id": "-4548879553",
									"text": "@Супер1, @Супер2, @Cegth3, @РОП.\nАгент "+x["user"]+" все еще не берет заявки, проверьте агента и отпишите о результате в этот чат.\n Или закройте смену командой: /StopWorkTime"+x["id"]+" если агент уже завершил смену."
								}, {
									"Content-Type": "application/json",
									"User-Agent": "insomnia/8.5.1"
								})
								PutResponse("https://668253b204acc3545a090ff2.mockapi.io/SpeedInetBase/NoWork_Agents/"+x["id"], {"InIgnoreList": True,"IgnoreUnix":Current_Unix}, {
								  "Content-Type": "application/json",
								  "User-Agent": "insomnia/9.3.2"
								})

						else:
							PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
									"chat_id": "-4548879553",
									"text": "@Супер1, @Супер2, @Cegth3, @РОП.\nАгент "+x["user"]+" не берет заявки 1ч, проверьте агента и отпишите о результате в этот чат.\n Или закройте смену командой: /StopWorkTime"+x["id"]+" если агент уже завершил смену."
								}, {
									"Content-Type": "application/json",
									"User-Agent": "insomnia/8.5.1"
								})
							PutResponse("https://668253b204acc3545a090ff2.mockapi.io/SpeedInetBase/NoWork_Agents/"+x["id"], {"InIgnoreList": True,"IgnoreUnix":Current_Unix}, {
							  "Content-Type": "application/json",
							  "User-Agent": "insomnia/9.3.2"
							})




					PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
						"chat_id": "-4548879553",
						"text": "Автоматически закрыл смену у Агента "+x["user"]+", Причина: Не проявляет активности более 1ч"
					}, {
						"Content-Type": "application/json",
						"User-Agent": "insomnia/8.5.1"
					})


					print("Автоматически закрыл смену у Агента "+x["user"]+", Причина: Не проявляет активности более 1ч")

				elif Current_Unix - x["LastBeryClick"] >= 43200 and Current_Unix - x["LastBeryClick"] < 2592000:
					
					a = PostResponse("https://speedinet.bitrix24.ru/rest/25550/92yb1mz0rkt5e2cl/timeman.close",
						{
							"user_id": x["BT_Id"]
						},
						{
					    "cookie": "qmb=0.",
					    "Content-Type": "application/json",
					    "User-Agent": "insomnia/10.1.1"
					})
					print(a)

					"""
					PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
						"chat_id": "-1001903941079",
						"text": "Автоматически закрыл смену у Агента "+x["user"]+", Причина: Не проявляет активности более 12ч"
					}, {
						"Content-Type": "application/json",
						"User-Agent": "insomnia/8.5.1"
					})
                                        """
					PutResponse("https://668253b204acc3545a090ff2.mockapi.io/SpeedInetBase/NoWork_Agents/"+x["id"], {"Online": False}, {
					   "Content-Type": "application/json",
					   "User-Agent": "insomnia/9.3.2"
					})
					

					PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
						"chat_id": "-4548879553",
						"text": "Автоматически закрыл смену у Агента "+x["user"]+", Причина: Не проявляет активности более 12ч"
					}, {
						"Content-Type": "application/json",
						"User-Agent": "insomnia/8.5.1"
					})

					print("Автоматически закрыл смену у Агента "+x["user"]+", Причина: Не проявляет активности более 12ч")

				elif Current_Unix - x["LastBeryClick"] >= 2592000:
					
					DeleteResponse("https://668253b204acc3545a090ff2.mockapi.io/SpeedInetBase/NoWork_Agents/"+x["id"], {
				    "Content-Type": "application/json",
				    "User-Agent": "insomnia/9.3.3"
					})

					PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
						"chat_id": "-4548879553",
						"text": "Убрал учетную запись Агента "+x["user"]+" из API, Причина: Не проявляет активности более 30дн"
					}, {
						"Content-Type": "application/json",
						"User-Agent": "insomnia/8.5.1"
					})

					print("Убрал учетную запись Агента "+x["user"]+" из API, Причина: Не проявляет активности более 30дн")
				
			

	current_datetime = datetime.datetime.now()
	print("Закончил: ", current_datetime)
		

#Вызываю основные функции в интерале 10мин (600сек)
def printit():
  current_datetime = datetime.datetime.now()
  print("Начал: ", current_datetime)


  Get_Api_Data()
  threading.Timer(600, printit).start()

printit()
