from http.server import BaseHTTPRequestHandler
import json
import os
import requests

BOT_TOKEN = "8191155033:AAHXqDCDxZVfHOhQ16WjGMIvGweFwUueh6M"
CHANNEL_URL = "https://t.me/SH_Trading_academy"
PHOTO_URL = "https://ibb.co.com/0RCVWmyb"
RISK_PHOTO_URL = "https://img.icons8.com/clouds/1000/security-checked.png"

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
            
            if callback_data == 'risk_accepted':
                self.send_main_offer(chat_id)
                # Ответим на callback чтобы убрать "часики"
                self.answer_callback_query(update['callback_query']['id'])
            return
        
        # Обработка текстовых сообщений
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            text = update['message'].get('text', '')
            
            if text == '/start':
                self.send_risk_disclaimer(chat_id)
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

    def send_risk_disclaimer(self, chat_id):
        """Отправка риск-дисклеймера"""
        markup = {
            "inline_keyboard": [[
                {
                    "text": "✅ Я ОСОЗНАЮ РИСКИ И СОГЛАСЕН",
                    "callback_data": "risk_accepted"
                }
            ]]
        }
        
        self.send_telegram_message(chat_id,
            "🔐 *Важно: Осознание рисков трейдинга*\n\n"
            "📊 **Прежде чем начать, подтвердите что понимаете:**\n"
            "• Трейдинг связан с финансовыми рисками\n"
            "• Вы берете ответственность за свои решения\n"
            "• Риск-менеджмент — основа успеха\n"
            "• Убыточные сделки — часть процесса\n\n"
            "Нажмите кнопку ниже для подтверждения",
            reply_markup=markup)

    def send_main_offer(self, chat_id):
        """Основное предложение после согласия"""
        markup = {
            "inline_keyboard": [[
                {
                    "text": "📲 Присоединиться к каналу",
                    "url": CHANNEL_URL
                }
            ]]
        }
        
        self.send_telegram_photo(chat_id,
            "🚀 *Добро пожаловать в SH. Trading Academy!*\n\n"
            "💎 **Что вы получаете:**\n"
            "• Реальные сделки от профессионалов\n"
            "• Обучение риск-менеджменту\n" 
            "• Поддержку сообщества\n"
            "• 15-летний опыт в вашем распоряжении\n\n"
            "📈 *Начните свой путь к финансовой свободе!*",
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
