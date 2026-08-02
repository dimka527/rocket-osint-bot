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

def generate_data(query):
    names = ["Козлов Дмитрий", "Смирнова Ольга", "Новиков Артем"]
    return {
        "name": random.choice(names),
        "dob": f"{random.randint(1985,2000)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
        "address": f"г. Москва, ул. Ленина, д. {random.randint(1,100)}",
        "email": f"user{random.randint(1000,9999)}@mail.ru",
        "telegram": f"@user_{random.randint(10000,99999)}",
        "telegram_id": str(random.randint(100000000,999999999)),
        "vk": f"https://vk.com/id{random.randint(100000000,999999999)}",
        "operator": random.choice(["МТС","Билайн","МегаФон"]),
        "region": random.choice(["Москва","СПб","Казань"]),
        "passport": f"{random.randint(4000,5000)} {random.randint(100000,999999)}",
        "car": f"{random.choice(['Toyota','Kia','BMW'])} {random.randint(2018,2024)}"
    }

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
    data = generate_data(query)
    send_result(message.chat.id, data)

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
