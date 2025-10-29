from http.server import BaseHTTPRequestHandler
import json
import os
import requests

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8191155033:AAHXqDCDxZVfHOhQ16WjGMIvGweFwUueh6M')
CHANNEL_URL = "https://t.me/SH_Trading_academy"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'🤖 Бот SH. Trading Academy работает!')
        
        elif self.path == '/set-webhook':
            webhook_url = "https://telegram-bot-laff.vercel.app/api/webhook"
            result = self.set_webhook(webhook_url)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f'Webhook set to: {webhook_url}<br>Result: {result}'.encode())
        
        else:
            self.send_response(404)
            self.end_headers()

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

    def handle_update(self, update):
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            text = update['message'].get('text', '')
            
            if text == '/start':
                self.send_telegram_message(chat_id, '🚀 Добро пожаловать! Нажмите кнопку ниже чтобы присоединиться!', True)
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
            print(f"Error sending message: {e}")

    def set_webhook(self, webhook_url):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
        data = {'url': webhook_url}
        try:
            response = requests.post(url, json=data, timeout=10)
            return response.json()
        except Exception as e:
            return {'error': str(e)}

def main(request, response):
    handler = Handler(request, response, {})
    handler.handle()
