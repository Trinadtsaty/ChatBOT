from secret.bot.bot_key import token
from bot.handlers import Start
from bot.buttons import Buttons
import telebot
import json
import os

class TelegramBot_Chat:
    def __init__(self, token: str):
        self.bot = telebot.TeleBot(token)

        self.start_bot = Start(self.bot)
        self.buttons = Buttons(self.bot)

        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.start_bot.handle(message)

        # Обработка нажатий на inline-кнопки
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_inline_buttons(call):
            self.buttons.type_button(call)

        # @self.bot.message_handler(func=lambda message: True, content_types=['text'])
        # def echo(message):
        #     # Игнорируем команды, чтобы не пересекаться с start_handler
        #     if not message.text.startswith('/'):
        #         self.echo_handler.handle(message)


    def run(self):
        print("Бот запущен")
        self.bot.infinity_polling()

if __name__ == "__main__":
    bot = TelegramBot_Chat(token["bot_key"])
    bot.run()
