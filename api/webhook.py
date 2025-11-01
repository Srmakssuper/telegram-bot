from http.server import BaseHTTPRequestHandler
import json
import os
import requests

BOT_TOKEN = "8191155033:AAHXqDCDxZVfHOhQ16WjGMIvGweFwUueh6M"
CHANNEL_URL = "https://t.me/SH_Trading_academy"
PHOTO_URL = "https://ibb.co.com/0RCVWmyb"
RISK_PHOTO_URL = "https://img.icons8.com/clouds/1000/security-checked.png"
MANAGEMENT_PHOTO_URL = "https://img.icons8.com/clouds/1000/money-bag.png"
LOSSES_PHOTO_URL = "https://img.icons8.com/clouds/1000/chart.png"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data)
            
            self.handle_update(update)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Bot is running!')
        else:
            self.send_response(404)
            self.end_headers()

    def handle_update(self, update):
        # Обработка нажатия на инлайн-кнопки
        if 'callback_query' in update:
            chat_id = update['callback_query']['message']['chat']['id']
            callback_data = update['callback_query']['data']
            
            if callback_data == 'understand_trading':
                self.send_trading_understanding(chat_id)
            elif callback_data == 'understand_management':
                self.send_management_understanding(chat_id)
            elif callback_data == 'understand_losses':
                self.send_losses_understanding(chat_id)
            elif callback_data == 'risk_accepted':
                self.send_main_offer(chat_id)
            
            # Ответим на callback чтобы убрать "часики"
            self.answer_callback_query(update['callback_query']['id'])
            return
        
        # Обработка текстовых сообщений
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            text = update['message'].get('text', '')
            
            if text == '/start':
                self.send_welcome_disclaimer(chat_id)
            elif text in ['/help', '/info']:
                self.send_telegram_message(chat_id,
                    "🤖 *Что умеет этот бот?*\n\n"
                    "💰 Делимся реальными сделками бесплатно, в которые входим сами, "
                    "и помогаем нашим подписчикам зарабатывать вместе с нами 👇\n\n"
                    "Нажми /start, чтобы увидеть подробности!")
            else:
                self.send_telegram_message(chat_id,
                    "👋 Я бот *SH. Trading Academy*.\n\n"
                    "Чтобы узнать, что я умею — напиши /help.\n"
                    "Чтобы начать — нажми /start 🚀")

    def answer_callback_query(self, callback_query_id):
        """Отвечаем на callback query чтобы убрать часики"""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
        data = {'callback_query_id': callback_query_id}
        try:
            requests.post(url, json=data, timeout=5)
        except Exception as e:
            print(f"Error answering callback: {e}")

    def send_welcome_disclaimer(self, chat_id):
        """Приветственное сообщение с основным дисклеймером"""
        markup = {
            "inline_keyboard": [[
                {
                    "text": "📚 ПОНЯТЬ ОСНОВЫ ТРЕЙДИНГА",
                    "callback_data": "understand_trading"
                }
            ]]
        }
        
        self.send_telegram_photo(chat_id,
            "🎯 *Добро пожаловать в мир осознанного трейдинга!*\n\n"
            "💎 **SH. Trading Academy** — это не просто сигналы, а профессиональное обучение\n\n"
            "📊 *Прежде чем начать, важно понять основные принципы:*\n"
            "• Что такое трейдинг и какие риски он несёт\n"
            "• Как управлять капиталом\n"
            "• Как принимать убыточные сделки\n\n"
            "Нажмите кнопку ниже для продолжения 👇",
            photo_url=RISK_PHOTO_URL,
            reply_markup=markup)

    def send_trading_understanding(self, chat_id):
        """Раздел 1: Понимание трейдинга и рисков"""
        markup = {
            "inline_keyboard": [[
                {
                    "text": "💼 ПЕРЕЙТИ К УПРАВЛЕНИЮ КАПИТАЛОМ",
                    "callback_data": "understand_management"
                }
            ]]
        }
        
        self.send_telegram_photo(chat_id,
            "📈 *Раздел 1: Понимание трейдинга и рисков*\n\n"
            "🔍 **Трейдинг — это профессиональная деятельность,** где:\n\n"
            "✅ *Вы получаете:*\n"
            "• Возможность финансовой свободы\n"
            "• Гибкий график работы\n"
            "• Неограниченный потенциал дохода\n\n"
            "⚡️ *Вы принимаете на себя:*\n"
            "• Полную ответственность за решения\n"
            "• Финансовые риски рынка\n"
            "• Эмоциональную нагрузку\n\n"
            "💡 *Осознанный подход = уверенность в действиях*",
            photo_url=RISK_PHOTO_URL,
            reply_markup=markup)

    def send_management_understanding(self, chat_id):
        """Раздел 2: Мани-менеджмент и риск-менеджмент"""
        markup = {
            "inline_keyboard": [[
                {
                    "text": "📉 ПЕРЕЙТИ К ТЕМЕ УБЫТКОВ",
                    "callback_data": "understand_losses"
                }
            ]]
        }
        
        self.send_telegram_photo(chat_id,
            "💰 *Раздел 2: Управление капиталом и рисками*\n\n"
            "🎯 **Мани-менеджмент — основа долгосрочного успеха:**\n\n"
            "🛡️ *Золотые правила:*\n"
            "• **1-2% риска** от депозита на сделку\n"
            "• **Диверсификация** — не все яйца в одной корзине\n"
            "• **Стоп-лосс** — автоматическая защита\n\n"
            "📊 *Риск-менеджмент — ваша броня:*\n"
            "• Соотношение риск/прибыль 1:2+\n"
            "• Расчет размера позиции ДО входа\n"
            "• Психологическая готовность к риску\n\n"
            "⚖️ *Правила сохраняют капитал, когда интуиция подводит*",
            photo_url=MANAGEMENT_PHOTO_URL,
            reply_markup=markup)

    def send_losses_understanding(self, chat_id):
        """Раздел 3: Принятие убыточных сделок"""
        markup = {
            "inline_keyboard": [[
                {
                    "text": "✅ Я ПОНИМАЮ ВСЕ РИСКИ И СОГЛАСЕН",
                    "callback_data": "risk_accepted"
                }
            ]]
        }
        
        self.send_telegram_photo(chat_id,
            "📉 *Раздел 3: Убыточные сделки — часть процесса*\n\n"
            "🌊 **Реальность рынка:**\n"
            "• Никто не торгует без убытков\n"
            "• Даже лучшие трейдеры ошибаются\n"
            "• Убытки — плата за опыт\n\n"
            "💪 **Правильное отношение:**\n"
            "• Убыток ≠ провал, убыток = урок\n"
            "• Анализ ошибок = рост мастерства\n"
            "• Эмоциональный контроль = стабильность\n\n"
            "🎯 **Наша философия:**\n"
            "Мы учим не избегать убытков, а управлять ими так,\n"
            "чтобы они не мешали достижению целей!\n\n"
            "*Готовы начать осознанный путь?*",
            photo_url=LOSSES_PHOTO_URL,
            reply_markup=markup)

    def send_main_offer(self, chat_id):
        """Основное предложение после согласия со всеми рисками"""
        markup = {
            "inline_keyboard": [[
                {
                    "text": "📲 ПРИСОЕДИНИТЬСЯ К КАНАЛУ",
                    "url": CHANNEL_URL
                }
            ]]
        }
        
        self.send_telegram_photo(chat_id,
            "🚀 *Поздравляем! Вы прошли основы осознанного трейдинга!*\n\n"
            "💎 **Теперь вы готовы к реальной работе с SH. Trading Academy:**\n\n"
            "📈 *Что вас ждет:*\n"
            "• Реальные сделки с нашим входом\n"
            "• Профессиональный риск-менеджмент\n"
            "• Поддержка опытной команды\n"
            "• Постоянное обучение и рост\n\n"
            "🎯 *Наша миссия:*\n"
            "Сделать из вас самостоятельного трейдера,\n"
            "а не зависимого от сигналов!\n\n"
            "👇 *Присоединяйтесь к нашему сообществу:*",
            photo_url=PHOTO_URL,
            reply_markup=markup)

    def send_telegram_photo(self, chat_id, caption, photo_url=None, reply_markup=None):
        """Отправка фото с подписью"""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        
        data = {
            'chat_id': chat_id,
            'photo': photo_url or PHOTO_URL,
            'caption': caption,
            'parse_mode': 'Markdown',
        }
        
        if reply_markup:
            data['reply_markup'] = json.dumps(reply_markup)
        
        try:
            requests.post(url, json=data, timeout=10)
        except Exception as e:
            print(f"Error sending photo: {e}")

    def send_telegram_message(self, chat_id, text, reply_markup=None):
        """Отправка обычного текстового сообщения"""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown',
        }
        
        if reply_markup:
            data['reply_markup'] = json.dumps(reply_markup)
        
        try:
            requests.post(url, json=data, timeout=10)
        except Exception as e:
            print(f"Error: {e}")

def main(request, response):
    handler = Handler(request, response, {})
    handler.handle()
