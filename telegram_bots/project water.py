import telebot
import time
import threading

TOKEN = "8739590188:AAF8_euBoqCt-S2sOEqXNP_dGqGnDIuEDNE"

bot = telebot.TeleBot(TOKEN)

water = 0
reminder = 1
chat_id = None  


@bot.message_handler(commands=['start'])
def start(message):
    global chat_id
    chat_id = message.chat.id 

    bot.send_message(chat_id,
                     "Привет\n"
                     "/setreminder 1 - напоминание каждый час\n"
                     "/drank 300 - добавить воду\n"
                     "/status - сколько выпито")


@bot.message_handler(commands=['setreminder'])
def setreminder(message):
    global reminder

    try:
        reminder = int(message.text.split()[1])
        bot.send_message(message.chat.id,
                         f"Напоминание каждые {reminder} час(а)")
    except:
        bot.send_message(message.chat.id,
                         "Напиши так: /setreminder 1")


@bot.message_handler(commands=['drank'])
def drank(message):
    global water

    try:
        ml = int(message.text.split()[1])
        water += ml

        bot.send_message(message.chat.id,
                         f"Ты выпил {water} мл воды")
    except:
        bot.send_message(message.chat.id,
                         "Напиши так: /drank 300")


@bot.message_handler(commands=['status'])
def status(message):
    left = 2000 - water

    if left > 0:
        bot.send_message(message.chat.id,
                         f"Осталось выпить {left} мл")
    else:
        bot.send_message(message.chat.id,
                         "Ты выпил достаточно воды")


# напоминания
def remind():
    global chat_id

    while True:
        time.sleep(reminder * 3600)

        if chat_id is not None:
            bot.send_message(chat_id,
                             "Не забывай пить воду")


threading.Thread(target=remind, daemon=True).start()

print("Бот работает")

bot.infinity_polling()