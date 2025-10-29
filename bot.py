import telebot
from telebot import types

# 🔑 ВСТАВЬ СВОЙ ТОКЕН от BotFather
BOT_TOKEN = "8191155033:AAHXqDCDxZVfHOhQ16WjGMIvGweFwUueh6M"
CHANNEL_URL = "https://t.me/SH_Trading_academy"

bot = telebot.TeleBot(BOT_TOKEN)

# 💬 Сообщение, которое отображается при первом заходе в бота
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
    # Кнопка "Присоединиться"
    markup = types.InlineKeyboardMarkup()
    join_button = types.InlineKeyboardButton("📲 Присоединиться", url=CHANNEL_URL)
    markup.add(join_button)

    # Текст под фото
    caption = (
        "📈 *SH. Trading Academy* — команда профессионалов с 15-летним опытом торговли 💪\n"
        "Следите за нашими входами, учитесь и растите вместе с нами!"
    )

    # Отправка фото + подписи + кнопки
    with open("logo.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption=caption, parse_mode="Markdown", reply_markup=markup)

# 🧠 Обработка любого текста (по желанию)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = (
        "👋 Я бот *SH. Trading Academy*.\n\n"
        "Чтобы узнать, что я умею — напиши /help.\n"
        "Чтобы начать — нажми /start 🚀"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# 🔁 Запуск бота
print("✅ Бот запущен и работает...")
bot.polling(none_stop=True)
