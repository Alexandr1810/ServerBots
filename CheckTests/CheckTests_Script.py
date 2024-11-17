import threading #Лаба для интервалов и корутин
import requests #Для запросов на биток
import json #Преобразование ответа сервера в словарь питона
import time #Задержки для запросов
import re #Лаба для работы с паттернами строк
import datetime #Для работы с датой
import os #для удаления файлов
import glob #Для поиска файлов
import random
import os
import subprocess

app_path = r"C:/Users/Максим Б/AppData/Local/Programs/Python/Launcher/py.exe"

with open('Html_Head.txt', 'r', encoding='utf-8') as file:
    # Читаем содержимое файла
    Html_Head = file.read()

with open('Html_Footer.txt', 'r', encoding='utf-8') as file:
    # Читаем содержимое файла
    Html_Footer = file.read()

folder_path = 'Itogs'

Html_Body = ''

def CheckUpdates():
  global Html_Body
  response = json.loads(requests.request("GET", "https://66cea2c0901aab24841f06e7.mockapi.io/Temp_Tests/", headers={
    "Content-Type": "application/json",
    "User-Agent": "insomnia/9.3.2"
  }).text)



  for Tests in response:
    html_content = ''
    Html_Body = ''
    print()
    print("Тест", Tests["TestTitle"])
    print("Агент", Tests["Agent"])

    print("Процент выполнения", Tests["Percent"])

    Html_Body += '<div class="TestHead"><h1>Тест <span>'+Tests["TestTitle"]+'</span></h1><hr><h1>Агент <span>'+Tests["Agent"]+'</span></h1></div>'

    for elems in range(len(Tests["TestBody"])):
      print("Вопрос:", Tests["TestBody"][elems]["Question"])
      print("Ответ:", Tests["TestBody"][elems]["Answer"])
      print("Итог:", Tests["TestBody"][elems]["Itog"])
      

      if Tests["TestBody"][elems]["Itog"] == "Верно":
        colorId = "Green"
      elif Tests["TestBody"][elems]["Itog"] == "Не Верно":
        colorId = "Red"
      elif Tests["TestBody"][elems]["Itog"] == "Требует Проверки":
        colorId = "Yellow"
      
      print("colorId: ", colorId)
      print()
      print("---")
      print()


      Html_Body += '<div class="TestBody"><div class="TestBody-block"><div class="TestBody-block-head"><h1 class="TestBody-Num">#'+str(elems+1)+'</h1><h1 class="TestBody-Itog" id="'+colorId+'">'+Tests["TestBody"][elems]["Itog"]+'</h1></div> '
      Html_Body += '<h1 class="TestBody-Question">Вопрос: <span>'+Tests["TestBody"][elems]["Question"]+'</span></h1><hr><h1 class="TestBody-Answer">Ответ: <span>'+Tests["TestBody"][elems]["Answer"]+'</span></h1></div>'
    print(Html_Body)

    filename = str(Tests["Percent"])+" Тест" + ' ' + Tests["TestTitle"] + ' ' + Tests["Agent"]

    html_content = Html_Head + Html_Body + Html_Footer
    # Открываем файл example.html в режиме записи
    with open('Itogs/'+filename+'.html', 'w', encoding='utf-8') as file:
        # Записываем строку в файл
        file.write(html_content)
    # Открываем файл example.html в режиме записи
    with open('AllItogs/'+filename+'.html', 'w', encoding='utf-8') as file:
        # Записываем строку в файл
        file.write(html_content)

    response1 = requests.request("DELETE", "https://66cea2c0901aab24841f06e7.mockapi.io/Temp_Tests/"+Tests["id"], headers={
      "Content-Type": "application/json",
      "User-Agent": "insomnia/9.3.3"
    })

    subprocess.Popen(["start", app_path, "Send_ToServer.py"], shell=True)

  

  current_datetime = datetime.datetime.now()
  print("Закончил: ", current_datetime)

#Вызываю основные функции в интерале 5мин (300сек)
def printit():
  print("Начинаю Шаманить!")
  html_files = glob.glob(os.path.join(folder_path, '*.html'))
  print(html_files)
  # Удаляем каждый файл
  for file in html_files:
    try:
        os.remove(file)
        print(f'Удалён файл: {file}')
    except Exception as e:
        print(f'Ошибка при удалении файла {file}: {e}')



  current_datetime = datetime.datetime.now()
  print("Начал: ", current_datetime)

  CheckUpdates()
  threading.Timer(30, printit).start()

printit()