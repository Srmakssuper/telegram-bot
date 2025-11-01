from http.server import BaseHTTPRequestHandler
import json
import os
import requests

BOT_TOKEN = "8191155033:AAHXqDCDxZVfHOhQ16WjGMIvGweFwUueh6M"
CHANNEL_URL = "https://t.me/SH_Trading_academy"
PHOTO_URL = "https://ibb.co.com/0RCVWmyb"
RISK_PHOTO_URL = "https://img.icons8.com/clouds/1000/security-checked.png"  # Фото для риск-менеджмента

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
        # Обработка callback от кнопок
        if 'callback_query' in update:
            chat_id = update['callback_query']['message']['chat']['id']
            callback_data = update['callback_query']['data']
            
            if callback_data == 'learn_risk':
                self.send_risk_education(chat_id)
            elif callback_data == 'risk_accepted':
                self.send_final_offer(chat_id)
            elif callback_data == 'learn_1':
                self.send_lesson_1(chat_id)
            elif callback_data == 'learn_2':
                self.send_lesson_2(chat_id)
            elif callback_data == 'learn_3':
                self.send_lesson_3(chat_id)
                
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

    def send_risk_disclaimer(self, chat_id):
        """Отправка риск-дисклеймера с кнопками"""
        markup = {
            "inline_keyboard": [
                [
                    {
                        "text": "📚 УЗНАТЬ ПРО РИСК-МЕНЕДЖМЕНТ",
                        "callback_data": "learn_risk"
                    }
                ],
                [
                    {
                        "text": "✅ Я УЖЕ ЗНАЮ И СОГЛАСЕН",
                        "callback_data": "risk_accepted"
                    }
                ]
            ]
        }
        
        self.send_telegram_photo(chat_id,
            "🔐 *Осознанная торговля — наша философия*\n\n"
            "📊 **Прежде чем начать, важно понимать:**\n"
            "• Трейдинг — это профессиональная деятельность\n"
            "• Вы принимаете полную ответственность за свои решения\n"
            "• Риск-менеджмент — основа сохранения капитала\n"
            "• Убыточные сделки — неотъемлемая часть процесса\n\n"
            "💎 *Знания защищают лучше, чем удача*",
            photo_url=RISK_PHOTO_URL,
            reply_markup=markup)

    def send_risk_education(self, chat_id):
        """Отправка меню обучения риск-менеджменту"""
        markup = {
            "inline_keyboard": [
                [
                    {"text": "💰 Правило 1-2%", "callback_data": "learn_1"},
                    {"text": "⚖️ Риск/Прибыль", "callback_data": "learn_2"}
                ],
                [
                    {"text": "🛡️ Стоп-лосс", "callback_data": "learn_3"},
                    {"text": "✅ ЗАКОНЧИТЬ ОБУЧЕНИЕ", "callback_data": "risk_accepted"}
                ]
            ]
        }
        
        self.send_telegram_message(chat_id,
            "📚 *Основы риск-менеджмента*\n\n"
            "Выберите тему для изучения:\n\n"
            "• 💰 **Правило 1-2%** - защита капитала\n"
            "• ⚖️ **Риск/Прибыль** - математика успеха\n"
            "• 🛡️ **Стоп-лосс** - ваш главный защитник\n\n"
            "Изучите основы перед стартом!",
            reply_markup=markup)

    def send_lesson_1(self, chat_id):
        """Урок 1: Правило 1-2%"""
        markup = {
            "inline_keyboard": [[
                {
                    "text": "📚 ВЕРНУТЬСЯ К ВЫБОРУ ТЕМ",
                    "callback_data": "learn_risk"
                }
            ]]
        }
        
        self.send_telegram_message(chat_id,
            "💰 *Правило 1-2% для защиты капитала*\n\n"
            "🎯 **Суть правила:**\n"
            "• Рискуйте не более 1-2% от депозита за сделку\n"
            "• При депозите $1000 = $10-20 риска на сделку\n"
            "• Это защищает от потери капитала при серии убытков\n\n"
            "📊 **Пример:**\n"
            "Депозит: $1,000\n"
            "Макс риск: $20 на сделку\n"
            "Можно допустить 50 убытков подряд до потери капитала\n\n"
            "🛡️ *Ваша финансовая безопасность — прежде всего!*",
            reply_markup=markup)

    def send_lesson_2(self, chat_id):
        """Урок 2: Соотношение риск/прибыль"""
        markup = {
            "inline_keyboard": [[
                {
                    "text": "📚 ВЕРНУТЬСЯ К ВЫБОРУ ТЕМ",
                    "callback_data": "learn_risk"
                }
            ]]
        }
        
        self.send_telegram_message(chat_id,
            "⚖️ *Соотношение риск/прибыль (R/R)*\n\n"
            "🎯 **Золотое правило:**\n"
            "• Минимум 1:2 (риск $10 → цель $20+)\n"
            "• При 40% прибыльных сделок вы в плюсе\n"
            "• Всегда считайте ДО входа в сделку\n\n"
            "📈 **Пример расчета:**\n"
            "Стоп-лосс: $90 (риск $10)\n"
            "Тейк-профит: $110 (прибыль $20)\n"
            "R/R = 1:2 ✓\n\n"
            "💡 *Правильная математика = стабильная прибыль!*",
            reply_markup=markup)

    def send_lesson_3(self, chat_id):
        """Урок 3: Стоп-лосс"""
        markup = {
            "inline_keyboard": [[
                {
                    "text": "📚 ВЕРНУТЬСЯ К ВЫБОРУ ТЕМ",
                    "callback_data": "learn_risk"
                }
            ]]
        }
        
        self.send_telegram_message(chat_id,
            "🛡️ *Стоп-лосс — ваш лучший друг*\n\n"
            "🎯 **Зачем нужен:**\n"
            "• Автоматически ограничивает убытки\n"
            "• Убирает эмоции из торговли\n"
            "• Сохраняет капитал для новых возможностей\n\n"
            "📊 **Как устанавливать:**\n"
            "• На основе технических уровней\n"
            "• С учетом волатильности актива\n"
            "• В соответствии с правилом 1-2%\n\n"
            "🚫 *Торговля без стоп-лосса = игра в рулетку!*",
            reply_markup=markup)

    def send_final_offer(self, chat_id):
        """Финальное предложение после согласия"""
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
            "📈 **Что вы получаете:**\n"
            "• Реальные сделки от профессионалов\n"
            "• Обучение риск-менеджменту на практике\n"
            "• Поддержку сообщества трейдеров\n"
            "• 15-летний опыт в вашем распоряжении\n\n"
            "🎯 *Начните свой путь к финансовой свободе!*",
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
            'reply_markup': json.dumps(reply_markup) if reply_markup else None
        }
        
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
            'reply_markup': json.dumps(reply_markup) if reply_markup else None
        }
        
        try:
            requests.post(url, json=data, timeout=10)
        except Exception as e:
            print(f"Error: {e}")

def main(request, response):
    handler = Handler(request, response, {})
    handler.handle()
