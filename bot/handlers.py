import telebot
from telebot import types
import json
from .defs import *
from .buttons import Whitelist

# Общий базовый класс с полезными методами
class DefMessage:
    def defining_type(self, message):
        return message.chat.type

class Start(DefMessage):
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    def privat_start(self, message):
        answer = get_response_json("speech_patterns", "start_privat")["response"].format(username=message.from_user.first_name)
        markup = create_buttons_json("speech_patterns", "start_privat", self.bot)

        self.bot.send_message(message.chat.id, answer, reply_markup=markup)

    def chat_start(self, message):
        self.bot.send_message(message.chat.id, "Я пока не умею общаться тут, чат ID:" + str(message.chat.id))

    # -1002897239436

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

        self.whitelist = Whitelist(self.bot)

    def privat_start(self, message):

        dict = get_response_json(json_name="user_states", json_key=message.chat.id)
        print(dict)

        if dict:
            if dict["states"] == "give_id_group":
                self.bot.send_message(message.chat.id, "Сообщение получено")
                if dict ["action"] == "ID":
                    self.whitelist.add_id(message)
                elif dict ["action"] == "link":
                    self.whitelist.add_link(message)
                elif dict ["action"] == "message":
                    self.whitelist.add_message(message)

    def chat_start(self, message):
        pass

    def handle(self, message):
        message_type = self.defining_type(message)

        if message_type == "private":
            self.privat_start(message)
        else:
            self.chat_start(message)