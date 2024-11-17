import threading #Лаба для интервалов и корутин
import requests #Для запросов на биток
import json #Преобразование ответа сервера в словарь питона
import time #Задержки для запросов
import re #Лаба для работы с паттернами строк
import datetime #Для работы с датой
import pickle

update_id = 732199299
# Получаем
with open('data.sav', 'rb') as f:
  update_id = pickle.load(f)
print("update_id", update_id)




#Функция для отправки запросов
def SendResponse(url, headers):
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



def Get_Api_Data():
	global update_id
	Current_Unix = time.time()
	print("Current_Unix", Current_Unix)
	print()
	

	respose = SendResponse("https://668253b204acc3545a090ff2.mockapi.io/SpeedInetBase/NoWork_Agents", {
	    "Content-Type": "application/json",
	    "User-Agent": "insomnia/9.3.2"
	})

	print("respose", respose)
	print()

	ChatItems = SendResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/getUpdates?offset="+str(update_id+1), {
	    "Content-Type": "application/json",
	    "User-Agent": "insomnia/8.6.1"
	})

	for i in ChatItems["result"]:
		try:
			print(i["message"]["text"])
			print()
			for k in respose:
				if k["user"] in i["message"]["text"]:
					print('Это отчет ', k["user"], 'id:', k["id"])
					print()
					print()
					ChatItems = PutResponse("https://668253b204acc3545a090ff2.mockapi.io/SpeedInetBase/NoWork_Agents/"+k["id"], {
						"Online": False
					}, 
					{
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
	with open('data.sav', 'wb') as f:
		pickle.dump(update_id, f)

	respose = SendResponse("https://668253b204acc3545a090ff2.mockapi.io/SpeedInetBase/NoWork_Agents", {
	    "Content-Type": "application/json",
	    "User-Agent": "insomnia/9.3.2"
	})

	print("respose", respose)
	print()

	for x in respose:
		print(x)
		print("Сравниваю: ", Current_Unix, "и", x["LastBeryClick"], "Разница:", (Current_Unix - x["LastBeryClick"])/60/60, "часа", "Агент: ", x["Online"])
		if Current_Unix - x["LastBeryClick"] > 3600 and x["Online"] == True:
			
			AgentDeportament = PostResponse("https://speedinet.bitrix24.ru/rest/26/48qmdec3obtu7b6w/user.get", {"id": x["BT_Id"]}, {
				"cookie": "qmb=0.",
				"Content-Type": "application/json",
				"User-Agent": "insomnia/9.3.2"
			})
			print(AgentDeportament)
			SendText = ''
			if len(AgentDeportament["result"][0]["UF_DEPARTMENT"]) > 1:
				SendText = "Агент " + x["user"] + " из департамента " + str(AgentDeportament["result"][0]["UF_DEPARTMENT"][1]) + " не жмет на кнопку уже " + str(int((Current_Unix - x["LastBeryClick"])/60/60)) + " часов" 
			else:
				SendText = "Агент " + x["user"] + " из департамента " + str(AgentDeportament["result"][0]["UF_DEPARTMENT"][0]) + " не жмет на кнопку уже " + str(int((Current_Unix - x["LastBeryClick"])/60/60)) + " часов"

			print(SendText)

			if x["user"] != "Илья Золототрубов" and x["user"] != "Никита Колганов" and x["user"] != "Алесандр Шатохин":
				if len(AgentDeportament["result"][0]["UF_DEPARTMENT"]) > 1:
					if AgentDeportament["result"][0]["UF_DEPARTMENT"][1] == 30 or AgentDeportament["result"][0]["UF_DEPARTMENT"][0] == 30:
						print("Пишу в команду Никиты")
						PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
						    "chat_id": "-1002122366332",
						    "text": SendText
						}, {
						    "Content-Type": "application/json",
						    "User-Agent": "insomnia/8.5.1"
						})
					elif AgentDeportament["result"][0]["UF_DEPARTMENT"][1] == 32 or AgentDeportament["result"][0]["UF_DEPARTMENT"][0] == 32:
						print("Пишу в команду Ильи")
						PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
						    "chat_id": "-1001885125208",
						    "text": SendText
						}, {
						    "Content-Type": "application/json",
						    "User-Agent": "insomnia/8.5.1"
						})
				else:
					if AgentDeportament["result"][0]["UF_DEPARTMENT"][0] == 30:
						print("Пишу в команду Никиты")
						PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
						    "chat_id": "-1002122366332",
						    "text": SendText
						}, {
						    "Content-Type": "application/json",
						    "User-Agent": "insomnia/8.5.1"
						})
					elif AgentDeportament["result"][0]["UF_DEPARTMENT"][0] == 32:
						print("Пишу в команду Ильи")
						PostResponse("https://api.telegram.org/bot7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs/sendMessage", {
						    "chat_id": "-1001885125208",
						    "text": SendText
						}, {
						    "Content-Type": "application/json",
						    "User-Agent": "insomnia/8.5.1"
						})
		print()
	current_datetime = datetime.datetime.now()
	print("Закончил: ", current_datetime)
		

#Вызываю основные функции в интерале 30мин (1800сек)
def printit():
  current_datetime = datetime.datetime.now()
  print("Начал: ", current_datetime)


  Get_Api_Data()
  threading.Timer(1800, printit).start()

printit()