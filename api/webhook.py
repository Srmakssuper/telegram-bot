from http.server import BaseHTTPRequestHandler
import json
import os
import requests

BOT_TOKEN = "8191155033:AAHXqDCDxZVfHOhQ16WjGMIvGweFwUueh6M"
CHANNEL_URL = "https://t.me/SH_Trading_academy"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/webhook':
            # Читаем данные от Telegram
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data)
            
            # Обрабатываем сообщение
            self.handle_update(update)
            
            # Всегда возвращаем 200 OK для Telegram
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
                self.send_telegram_message(chat_id, 
                    "🚀 *SH. Trading Academy* — команда профессионалов с 15-летним опытом торговли 💪\n"
                    "Следите за нашими входами, учитесь и растите вместе с нами!", 
                    True)
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

    def send_telegram_message(self, chat_id, text, with_button=False):
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
