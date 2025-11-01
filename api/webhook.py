from http.server import BaseHTTPRequestHandler
import json
import os
import requests

BOT_TOKEN = "8191155033:AAHXqDCDxZVfHOhQ16WjGMIvGweFwUueh6M"
CHANNEL_URL = "https://t.me/SH_Trading_academy"
PHOTO_URL = "https://ibb.co.com/0RCVWmyb"

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
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            text = update['message'].get('text', '')
            
            if text == '/start':
                # Сначала отправляем риск-дисклеймер
                self.send_risk_disclaimer(chat_id)
            elif text == '/agree':
                # Если пользователь написал /agree - отправляем основное предложение
                self.send_main_offer(chat_id)
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

    def send_risk_disclaimer(self, chat_id):
        """Отправка риск-дисклеймера (просто текст)"""
        risk_text = (
            "🔐 *Важно: Осознание рисков трейдинга*\n\n"
            "📊 **Прежде чем начать, подтвердите что понимаете:**\n\n"
            "1. *Понимание трейдинга и ответственности:*\n"
            "   • Трейдинг — профессиональная деятельность\n"
            "   • Вы принимаете полную ответственность за решения\n"
            "   • Финансовые риски — неотъемлемая часть\n\n"
            "2. *Согласие с риск-менеджментом:*\n"
            "   • Обязательное использование стоп-лосс\n"
            "   • Правило 1-2% риска от депозита\n"
            "   • Управление капиталом — основа успеха\n\n"
            "3. *Принятие убыточных сделок:*\n"
            "   • Убытки — часть торгового процесса\n"
            "   • Психологическая готовность к просадкам\n"
            "   • Ошибки — опыт для совершенствования\n\n"
            "💎 *Осознанный подход = уверенность в действиях*\n\n"
            "Если вы понимаете и принимаете эти условия,\n"
            "напишите команду /agree чтобы продолжить"
        )
        
        self.send_telegram_message(chat_id, risk_text)

    def send_main_offer(self, chat_id):
        """Основное предложение после согласия"""
        markup = {
            "inline_keyboard": [[
                {
                    "text": "📲 Присоединиться",
                    "url": CHANNEL_URL
                }
            ]]
        }
        
        self.send_telegram_photo(chat_id,
            "🚀 *Добро пожаловать в SH. Trading Academy!*\n\n"
            "💎 **Теперь вы готовы к осознанной торговле!**\n\n"
            "📈 **Что вы получаете:**\n"
            "• Реальные сделки от профессионалов\n"
            "• Обучение риск-менеджменту\n" 
            "• Поддержку сообщества\n"
            "• 15-летний опыт в вашем распоряжении\n\n"
            "🎯 *Начните свой путь к финансовой свободе!*",
            reply_markup=markup)

    def send_telegram_photo(self, chat_id, caption, with_button=False):
        """Отправка фото с подписью"""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        
        reply_markup = None
        if with_button:
            reply_markup = {
                "inline_keyboard": [[
                    {
                        "text": "📲 Присоединиться",
                        "url": CHANNEL_URL
                    }
                ]]
            }
        
        data = {
            'chat_id': chat_id,
            'photo': PHOTO_URL,
            'caption': caption,
            'parse_mode': 'Markdown',
            'reply_markup': reply_markup
        }
        
        try:
            requests.post(url, json=data, timeout=10)
        except Exception as e:
            print(f"Error sending photo: {e}")

    def send_telegram_message(self, chat_id, text, with_button=False):
        """Отправка обычного текстового сообщения"""
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        
        reply_markup = None
        if with_button:
            reply_markup = {
                "inline_keyboard": [[
                    {
                        "text": "📲 Присоединиться",
                        "url": CHANNEL_URL
                    }
                ]]
            }
        
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'Markdown',
            'reply_markup': reply_markup
        }
        
        try:
            requests.post(url, json=data, timeout=10)
        except Exception as e:
            print(f"Error: {e}")

def main(request, response):
    handler = Handler(request, response, {})
    handler.handle()
