import telebot
from telebot import types
import requests
import random

API_TOKEN = "8828985447:AAGFB6g3X9gfgP7yPWVbShMFinCo6BhNZMk"
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📱 Пробив по номеру"),
        types.KeyboardButton("✈️ Пробив по Telegram"),
        types.KeyboardButton("🔍 Пробив по ВК")
    )
    bot.send_message(message.chat.id, "🔫 Бот готов к работе. Выбери режим.", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handler(message):
    if message.text == "📱 Пробив по номеру":
        bot.send_message(message.chat.id, "Введи номер в формате +7XXXXXXXXXX:")
    elif message.text == "✈️ Пробив по Telegram":
        bot.send_message(message.chat.id, "Введи @username:")
    elif message.text == "🔍 Пробив по ВК":
        bot.send_message(message.chat.id, "Введи ссылку на профиль VK:")

if __name__ == "__main__":
    bot.polling(non_stop=True)
