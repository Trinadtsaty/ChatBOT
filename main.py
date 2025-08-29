from secret.bot.bot_key import token
from bot.handlers import Start, Handlers_Text_Analysis, Help, Error, Median_Arithmetic_Mean
from bot.buttons import Buttons, Whitelist
import telebot
import json
import os

class TelegramBot_Chat:
    def __init__(self, token: str):
        self.bot = telebot.TeleBot(token)

        self.start_bot = Start(self.bot)
        self.buttons = Buttons(self.bot)
        self.echo_handler = Handlers_Text_Analysis(self.bot)
        self.help = Help(self.bot)
        self.error = Error(self.bot)
        self.median_arithmetic = Median_Arithmetic_Mean(self.bot)
        self.count = Median_Arithmetic_Mean(self.bot)
        self.whitelist = Whitelist(self.bot)

        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.start_bot.handle(message)

        @self.bot.message_handler(commands=['help'])
        def help(message):
            self.help.handle(message)

        @self.bot.message_handler(commands=['counting'])
        def counting(message):
            self.count.handle(message)

        @self.bot.message_handler(commands=['whitelist'])
        def whitelist(message):
            self.whitelist.message_type_id(message)

        @self.bot.message_handler(func=lambda message: message.text.startswith('/'))
        def unknown_command(message):
            self.error.get_unknown_command(message)

        # Обработка нажатий на inline-кнопки
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_inline_buttons(call):
            self.buttons.type_button(call)

        # Функция будет вызываться на все входящие текстовые сообщения боту.
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
