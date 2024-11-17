import telebot
import requests

# Создаем экземпляр бота
bot = telebot.TeleBot("6970838783:AAEn9KDsJWDh6kKCIEJPYu9beFLOOTlQQn0")

# Обработчик команды /ReservBery_on
@bot.message_handler(commands=["ReservBery_on"])
def reserv_bery_on(message):
    response = requests.request("PUT", "https://656de619bcc5618d3c242ec1.mockapi.io/MyPartners/EISSD_Pass/1", json={"ReservButtonOn": True}, headers={"Content-Type": "application/json","User-Agent": "insomnia/9.3.2"})
    bot.send_message(message.chat.id, "Резервная кнопка включена")

# Обработчик команды /ReservBery_off
@bot.message_handler(commands=["ReservBery_off"])
def reserv_bery_off(message):
    response = requests.request("PUT", "https://656de619bcc5618d3c242ec1.mockapi.io/MyPartners/EISSD_Pass/1", json={"ReservButtonOn": False}, headers={"Content-Type": "application/json","User-Agent": "insomnia/9.3.2"})
    bot.send_message(message.chat.id, "Резервная кнопка выключена")

# Запускаем бота
bot.polling()
