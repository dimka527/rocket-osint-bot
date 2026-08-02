import telebot
from telebot import types
import random
import string
from datetime import datetime
import os
bot.set_webhook()  # Сброс вебхука
API_TOKEN = "8828985447:AAGFB6g3X9gfgP7yPWVbShMFinCo6BhNZMk"
bot = telebot.TeleBot(API_TOKEN)

# Фейковая база данных
OSINT_DB = {}

import requests

# Новая функция для реального поиска по VK
def search_vk_real(query):
    # Вставь сюда свой реальный токен (после того, как получишь его)
    access_token = "ТВОЙ_ТОКЕН_ИЗ_VK" 
    api_version = "5.131"
    url = "https://api.vk.com/method/users.get"
    
    params = {
        "user_ids": query,
        "fields": "photo_200, city, bdate, status, followers_count, country",
        "access_token": access_token,
        "v": api_version
    }
    
    try:
        response = requests.get(url, params=params).json()
        return response
    except Exception as e:
        return {"error": str(e)}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📱 Пробив по номеру"),
        types.KeyboardButton("✈️ Пробив по Telegram"),
        types.KeyboardButton("🌐 Пробив по VK"),
        types.KeyboardButton("🎯 FACE TRAP"),
        types.KeyboardButton("📸 Фото"),
        types.KeyboardButton("ℹ️ Помощь")
    )
    bot.send_message(message.chat.id, "🛰️ *ROCKET OSINT BOT v3.7*\n\nВыберите действие:", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handler(message):
    chat_id = message.chat.id
    text = message.text
    if text == "📱 Пробив по номеру":
        msg = bot.send_message(chat_id, "Введите номер:")
        bot.register_next_step_handler(msg, search_phone)
    elif text == "✈️ Пробив по Telegram":
        msg = bot.send_message(chat_id, "Введите @username или ID:")
        bot.register_next_step_handler(msg, search_tg)
    elif text == "🌐 Пробив по VK":
        msg = bot.send_message(chat_id, "Введите ссылку VK или ID:")
        bot.register_next_step_handler(msg, search_vk)
    elif text == "ℹ️ Помощь":
        bot.send_message(chat_id, "ROCKET OSINT v3.7 | Rocket Way | 20.05.2026")
    elif text == "📸 Фото":
        bot.send_message(chat_id, "Функция фото временно отключена для стабильности")

def search_phone(message):
    query = message.text.strip()
    data = OSINT_DB.get(query, generate_data(query))
    send_result(message.chat.id, data)

def search_tg(message):
    query = message.text.strip()
    data = generate_data(query)
    send_result(message.chat.id, data)

def search_vk(message):
    query = message.text.strip()
    data = search_vk_real(query)
    
    # Обработка ответа от VK
    if "error" in data:
        bot.send_message(message.chat.id, f"❌ Ошибка: {data['error']}")
        return
    
    user = data.get("response", [{}])[0]
    
    # Формируем красивый ответ
    result = f"""
🟢 *РЕАЛЬНЫЙ РЕЗУЛЬТАТ ПО VK*
👤 Имя: {user.get('first_name', 'Не указано')} {user.get('last_name', 'Не указано')}
📅 ДР: {user.get('bdate', 'Не указано')}
📍 Город: {user.get('city', {}).get('title', 'Не указано')}
🌐 Страна: {user.get('country', {}).get('title', 'Не указано')}
📸 Фото: {user.get('photo_200', 'Нет фото')}
📊 Подписчики: {user.get('followers_count', '0')}
📝 Статус: {user.get('status', 'Нет статуса')}
"""
    bot.send_message(message.chat.id, result, parse_mode="Markdown")

def send_result(chat_id, data):
    text = f"""
🟢 *РЕЗУЛЬТАТ*
👤 {data['name']}
📅 {data['dob']}
📍 {data['address']}
📧 {data['email']}
✈️ {data['telegram']}
🌐 {data['vk']}
📡 {data['operator']}
📋 Паспорт: {data['passport']}
🚗 {data['car']}
"""
    bot.send_message(chat_id, text, parse_mode="Markdown")

# Запуск в режиме polling (без веб-сервера)
if __name__ == '__main__':
    print("Бот запущен в режиме polling...")
    bot.polling(non_stop=True)
