from flask import Flask, request
import telebot
from telebot import types
import os

app = Flask(__name__)

# 🔑 Получаем токен из переменных окружения Vercel
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8191155033:AAHXqDCDxZVfHOhQ16WjGMIvGweFwUueh6M')
CHANNEL_URL = "https://t.me/SH_Trading_academy"

bot = telebot.TeleBot(BOT_TOKEN)

# 💬 Сообщение при первом заходе
@bot.message_handler(commands=['help', 'info'])
def info(message):
    text = (
        "🤖 *Что умеет этот бот?*\n\n"
        "💰 Делимся реальными сделками бесплатно, в которые входим сами, "
        "и помогаем нашим подписчикам зарабатывать вместе с нами 👇\n\n"
        "Нажми /start, чтобы увидеть подробности!"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# 🚀 Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    join_button = types.InlineKeyboardButton("📲 Присоединиться", url=CHANNEL_URL)
    markup.add(join_button)

    caption = (
        "📈 *SH. Trading Academy* — команда профессионалов с 15-летним опытом торговли 💪\n"
        "Следите за нашими входами, учитесь и растите вместе с нами!"
    )

    # Для Vercel лучше использовать URL фото, а не локальный файл
    photo_url = "https://images.unsplash.com/photo-1640340434855-6084b1f4901c?w=400"  # Замените на ваше фото
    bot.send_photo(message.chat.id, photo_url, caption=caption, parse_mode="Markdown", reply_markup=markup)

# 🧠 Обработка любого текста
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = (
        "👋 Я бот *SH. Trading Academy*.\n\n"
        "Чтобы узнать, что я умею — напиши /help.\n"
        "Чтобы начать — нажми /start 🚀"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# 🔁 Вебхук обработчик для Vercel
@app.route('/api/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 'Bad Request', 400

# 🏠 Главная страница
@app.route('/')
def home():
    return '🤖 Бот SH. Trading Academy работает!'

# 🛠️ Установка вебхука
@app.route('/set-webhook')
def set_webhook():
    webhook_url = f"https://{request.host}/api/webhook"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    return f'Webhook set to: {webhook_url}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
