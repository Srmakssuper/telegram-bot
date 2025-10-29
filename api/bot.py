import telebot
from flask import Flask, request

# 🔑 Укажи здесь токен твоего бота
BOT_TOKEN = "8191155033:AAHXqDCDxZVfHOhQ16WjGMIvGweFwUueh6M"

# 🔗 Ссылка на твой Telegram-канал
CHANNEL_URL = "https://t.me/SH_Trading_academy"

# 📷 Фото для отправки (должно быть в интернете)
PHOTO_URL = "https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/", methods=["GET"])
def index():
    return {"ok": True, "message": "Bot is running!"}, 200


@bot.message_handler(commands=["start"])
def send_welcome(message):
    text = (
        "📈 *SH. Trading Academy* — команда профессионалов с 15-летним опытом торговли 💪\n"
        "Следите за нашими входами, учитесь и растите вместе с нами!"
    )
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("📲 Присоединиться", url=CHANNEL_URL)
    markup.add(btn)
    bot.send_photo(message.chat.id, PHOTO_URL, caption=text, parse_mode="Markdown", reply_markup=markup)


# 📢 Сообщение, которое видно сразу при входе в бота
@bot.message_handler(func=lambda message: True, content_types=['text'])
def welcome_text(message):
    start_text = (
        "🤖 *Что умеет этот бот?*\n\n"
        "💰 Делимся реальными сделками бесплатно, в которые входим сами, "
        "и помогаем нашим подписчикам зарабатывать вместе с нами 👇\n\n"
    )
    bot.reply_to(message, start_text, parse_mode="Markdown")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
