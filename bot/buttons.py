import telebot
from telebot import types
import json
from .defs import *

class Buttons:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

        self.whitelist = Whitelist(self.bot)

    def type_button(self, call):


        # self.bot.send_message(call.message.chat.id, "Я пока не умею работать с кнопками")
        # call.data
        if call.data == "whitelist_add_options":
            self.whitelist.message_type_id(call)
        elif call.data == "ID" or "link" or "message":
            self.bot.send_message(call.message.chat.id, call.data)

        self.bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )

class Whitelist:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    def message_type_id(self, call):
        answer = get_response_json("speech_patterns", "get_id")
        markup = create_buttons_json("speech_patterns", "get_id")

        self.bot.send_message(call.message.chat.id, answer, reply_markup=markup)

    def add_id(self, call):
        pass

    def add_link(self, call):
        pass

    def add_message(self, call):
        pass

