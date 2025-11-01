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
                self.send_complete_disclaimer(chat_id)
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

    def send_complete_disclaimer(self, chat_id):
        """Все три пункта в одном красивом сообщении"""
        markup = {
            "inline_keyboard": [[
                {
                    "text": "✅ Я ПОНИМАЮ И ПРИНИМАЮ ВСЕ УСЛОВИЯ",
                    "callback_data": "risk_accepted"
                }
            ]]
        }
        
        self.send_telegram_photo(chat_id,
            "🔐 *Осознанный трейдинг — основа успеха*\n\n"
            
            "📊 **1. Понимание трейдинга и ответственности**\n"
            "• Я осознаю, что трейдинг — профессиональная деятельность\n"
            "• Принимаю полную ответственность за свои торговые решения\n"
            "• Понимаю все финансовые риски, связанные с рынком\n\n"
            
            "💰 **2. Согласие с риск-менеджментом**\n"  
            "• Обязуюсь соблюдать правила управления капиталом\n"
            "• Буду использовать стоп-лосс для ограничения убытков\n"
            "• Приму принципы мани-менеджмента (1-2% риска на сделку)\n\n"
            
            "📉 **3. Принятие убыточных сделок**\n"
            "• Понимаю, что убытки — неотъемлемая часть трейдинга\n"
            "• Готов к психологической нагрузке от просадок\n"
            "• Рассматриваю убытки как опыт для совершенствования\n\n"
            
            "💎 *Только осознанный подход приводит к стабильным результатам!*\n\n"
            "Нажмите кнопку подтверждения ниже 👇",
            photo_url=RISK_PHOTO_URL,
            reply_markup=markup)

    def send_main_offer(self, chat_id):
        """Основное предложение после согласия"""
        markup = {
            "inline_keyboard": [[
                {
                    "text": "📲 ПРИСОЕДИНИТЬСЯ К КАНАЛУ",
                    "url": CHANNEL_URL
                }
            ]]
        }
        
        self.send_telegram_photo(chat_id,
            "🚀 *Добро пожаловать в SH. Trading Academy!*\n\n"
            "💎 **Теперь вы готовы к осознанной торговле!**\n\n"
            "📈 **Что вас ждет:**\n"
            "• Реальные сделки от профессионалов с 15-летним опытом\n"
            "• Обучение риск-менеджменту на практике\n" 
            "• Поддержка сообщества трейдеров\n"
            "• Бесплатные сигналы и аналитика\n\n"
            "🎯 *Наша цель — сделать вас самостоятельным трейдером!*\n\n"
            "👇 Присоединяйтесь к нашему каналу:",
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
