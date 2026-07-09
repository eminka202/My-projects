import telebot
from telebot import types
import requests

TOKEN = "8739590188:AAF8_euBoqCt-S2sOEqXNP_dGqGnDIuEDNE"

API_KEY = "41789d180a454e3c26de5bd8"

bot = telebot.TeleBot(TOKEN)

currencies = ["USD", "EUR", "RUB", "KZT", "GBP", "CNY", "JPY"]

user_data = {}

# тексты
texts = {
    "ru": {
        "choose_lang": "Выбери язык:",
        "from": "Выбери валюту ОТКУДА:",
        "to": "Выбери валюту КУДА:",
        "amount": "Теперь введи сумму:",
        "error": "Ошибка! Введи число"
    },
    "en": {
        "choose_lang": "Choose language:",
        "from": "Choose FROM currency:",
        "to": "Choose TO currency:",
        "amount": "Enter amount:",
        "error": "Error! Enter number"
    }
}

# /start
@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Русский", "English")

    bot.send_message(
        message.chat.id,
        "Выбери язык / Choose language",
        reply_markup=markup
    )

# выбор языка (кнопки)
@bot.message_handler(func=lambda message: message.text in ["Русский", "English"])
def set_language(message):

    chat_id = message.chat.id

    if message.text == "Русский":
        lang = "ru"
    else:
        lang = "en"

    user_data[chat_id] = {"lang": lang, "step": "from"}

    # кнопки валют
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for cur in currencies:
        markup.add(types.KeyboardButton(cur))

    bot.send_message(chat_id, texts[lang]["from"], reply_markup=markup)

# логика бота
@bot.message_handler(func=lambda message: True)
def handle(message):

    chat_id = message.chat.id

    if chat_id not in user_data:
        return

    lang = user_data[chat_id]["lang"]
    step = user_data[chat_id]["step"]
    text = message.text.upper()

    # FROM валюта
    if step == "from":
        if text in currencies:
            user_data[chat_id]["from"] = text
            user_data[chat_id]["step"] = "to"
            bot.send_message(chat_id, texts[lang]["to"])
        return

    # TO валюта
    if step == "to":
        if text in currencies:
            user_data[chat_id]["to"] = text
            user_data[chat_id]["step"] = "amount"
            bot.send_message(chat_id, texts[lang]["amount"])
        return

    # сумма
    if step == "amount":
        try:
            amount = float(text)

            from_cur = user_data[chat_id]["from"]
            to_cur = user_data[chat_id]["to"]

            url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_cur}"
            data = requests.get(url).json()

            rate = data["conversion_rates"][to_cur]
            result = amount * rate

            bot.send_message(
                chat_id,
                f"{amount} {from_cur} = {round(result, 2)} {to_cur}"
            )

            user_data.pop(chat_id)

        except ValueError:
            bot.send_message(chat_id, texts[lang]["error"])

bot.polling()