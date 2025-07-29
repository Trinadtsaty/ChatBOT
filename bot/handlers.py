import telebot
from telebot import types
import json
from .defs import *

# Общий базовый класс с полезными методами
class DefMessage:
    def defining_type(self, message):
        return message.chat.type

class Start(DefMessage):
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    def privat_start(self, message):
        answer = get_response_json("speech_patterns", "start_privat").format(username=message.from_user.first_name)
        markup = create_buttons_json("speech_patterns", "start_privat")

        self.bot.send_message(message.chat.id, answer, reply_markup=markup)

    def chat_start(self, message):
        self.bot.send_message(message.chat.id, "Я пока не умею общаться тут")

    def handle(self, message):
        message_type = self.defining_type(message)
        if message_type == "private":
            self.privat_start(message)
        else:
            self.chat_start(message)

        # self.bot.send_message(message.chat.id, message.text)
        # self.bot.send_message(message.chat.id, message_type)

class Help(DefMessage):
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

class Handlers_Text_Analysis(DefMessage):
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot



