import telebot
from telebot import types
import random
import os

API_TOKEN = "8828985447:AAGFB6g3X9gfgP7yPWVbShMFinCo6BhNZMk"
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📱 Пробив по номеру"),
        types.KeyboardButton("✈️ Пробив по Telegram"),
        types.KeyboardButton("🌐 Пробив по VK")
    )
    bot.send_message(
        message.chat.id, 
        "🛰️ *Бот заработал!*\n\nВыбери действие:", 
        parse_mode="Markdown", 
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: True)
def handler(message):
    bot.send_message(message.chat.id, "Функции временно отключены для стабильности.")

if __name__ == '__main__':
    bot.polling(non_stop=True)
