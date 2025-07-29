from secret.bot.bot_key import token
from bot.handlers import Start, Handlers_Text_Analysis
from bot.buttons import Buttons
import telebot
import json
import os

class TelegramBot_Chat:
    def __init__(self, token: str):
        self.bot = telebot.TeleBot(token)

        self.start_bot = Start(self.bot)
        self.buttons = Buttons(self.bot)
        self.echo_handler = Handlers_Text_Analysis(self.bot)

        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.start_bot.handle(message)

        # Обработка нажатий на inline-кнопки
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_inline_buttons(call):
            self.buttons.type_button(call)

        @self.bot.message_handler(func=lambda message: True, content_types=['text'])
        def echo(message):
            # Игнорируем команды, чтобы не пересекаться с start_handler
            if not message.text.startswith('/'):
                self.echo_handler.handle(message)

    def run(self):
        db_files = [
            "DB/user_states.json",
            "DB/whitelist.json"
        ]
        for file_path in db_files:
            # Создаем директорию DB, если ее нет
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if not os.path.exists(file_path):
                # Создаем файл с пустым JSON-объектом {}
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f, ensure_ascii=False, indent=4)

        print("Бот запущен")
        self.bot.infinity_polling()

if __name__ == "__main__":
    bot = TelegramBot_Chat(token["bot_key"])
    bot.run()
