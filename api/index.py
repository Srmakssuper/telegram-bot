from http.server import BaseHTTPRequestHandler
import json
import os
import requests

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8191155033:AAHXqDCDxZVfHOhQ16WjGMIvGweFwUueh6M')
CHANNEL_URL = "https://t.me/SH_Trading_academy"

def send_telegram_message(chat_id, text, with_button=False):
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
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def handle_update(update):
    if 'message' in update:
        chat_id = update['message']['chat']['id']
        text = update['message'].get('text', '')
        
        if text == '/start':
            send_telegram_message(chat_id, 
                "🚀 *SH. Trading Academy* — команда профессионалов с 15-летним опытом торговли 💪\n"
                "Следите за нашими входами, учитесь и растите вместе с нами!", 
                True)
        elif text in ['/help', '/info']:
            send_telegram_message(chat_id,
                "🤖 *Что умеет этот бот?*\n\n"
                "💰 Делимся реальными сделками бесплатно, в которые входим сами, "
                "и помогаем нашим подписчикам зарабатывать вместе с нами 👇\n\n"
                "Нажми /start, чтобы увидеть подробности!")
        else:
            send_telegram_message(chat_id,
                "👋 Я бот *SH. Trading Academy*.\n\n"
                "Чтобы узнать, что я умею — напиши /help.\n"
                "Чтобы начать — нажми /start 🚀")

def set_webhook():
    webhook_url = "https://telegram-bot-laff.vercel.app/api/webhook"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {'url': webhook_url}
    try:
        response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        return {'error': str(e)}

def handler(request, response):
    if request.method == 'GET':
        if request.path == '/set-webhook':
            result = set_webhook()
            response.send(f'Webhook set! Result: {result}', 200)
        else:
            response.send('🤖 Бот SH. Trading Academy работает!', 200)
    
    elif request.method == 'POST' and request.path == '/api/webhook':
        update = request.json
        handle_update(update)
        response.send('OK', 200)
    
    else:
        response.send('Not Found', 404)
