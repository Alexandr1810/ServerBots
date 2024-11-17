import telebot
import requests
import json #Преобразование ответа сервера в словарь питона
import re

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

  #Возвращаем словарь в переменную
  return response_dict

bot = telebot.TeleBot("7377332361:AAFr8FnibII4GPnfcsHrUjss5amE91GrzYs")
# Регулярное выражение для поиска команды и числа
pattern = r'/StopWorkTime(\d+)'

# Обработчик всех сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    match = re.search(pattern, message.text)
    if match:
        number = int(match.group(1))
        a = PostResponse("https://speedinet.bitrix24.ru/rest/25550/92yb1mz0rkt5e2cl/timeman.close",
        {
            "user_id": number
        },
        {
            "cookie": "qmb=0.",
            "Content-Type": "application/json",
            "User-Agent": "insomnia/10.1.1"
        })

        bot.reply_to(message, f'Завершил смену у Агента {number}')

    else:
        print('Неизвестная команда')

if __name__ == '__main__':
    bot.polling(none_stop=True)