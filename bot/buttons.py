import telebot
import json


class Buttons:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    def type_button(self, call):
        self.bot.send_message(call.message.chat.id, "Я пока не умею работать с кнопками")
        self.bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )

class whitelist:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot