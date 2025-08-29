import telebot
from telebot import types
import json
from datetime import datetime
# from bot.handlers import Start, Handlers_Text_Analysis, Help, Error, Median_Arithmetic_Mean
from .defs import *
from .math import Median, ArithmeticMean, MedianAndArithmeticMean
# give_response_json(json_name="user_states", json_key="", json_message={"action": call.data, "waiting_for_input": True})


class Buttons:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

        self.whitelist = Whitelist(self.bot)

        # Перенесите импорт сюда ↓
        from bot.handlers import Help, Median_Arithmetic_Mean
        self.help = Help(self.bot)
        self.median_arithmetic = Median_Arithmetic_Mean(self.bot)

        self.median = Median(self.bot)
        self.mean = ArithmeticMean(self.bot)
        self.together_mean_median = MedianAndArithmeticMean(self.bot)


    def type_button(self, call):

        # self.bot.send_message(call.message.chat.id, "Я пока не умею работать с кнопками")
        # call.data
        if call.data == "whitelist_add_options":
            self.whitelist.message_type_id(call.message)

        elif call.data == "ID" or call.data == "link" or call.data == "message":
            give_response_json(json_name="user_states", json_key=call.message.chat.id,
                               json_message={"states":"give_id_group", "action": call.data, "waiting_for_input": True})

            self.bot.send_message(call.message.chat.id, "Ожидаю сообщение")

        elif call.data == "help_privat":
            # self.help.privat_help(call.message)
            self.help.handle(call.message)

        elif call.data == "median_arithmetic_mean":
            self.median_arithmetic.handle(call.message)

        elif call.data == "median":
            self.median.calculations(call.message)


        elif call.data == "arithmetic_mean":
            self.mean.calculations(call.message)

        elif call.data == "together_mean_median":
            self.together_mean_median.calculations(call.message)



        self.bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )

class Whitelist:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    def message_type_id(self, message):
        answer = get_response_json("speech_patterns", "get_id")["response"]
        markup = create_buttons_json("speech_patterns", "get_id", self.bot)

        self.bot.send_message(message.chat.id, answer, reply_markup=markup)

    def add_id(self, message):
        group_id = message.text.strip()
        # Проверяем, что это число (возможно, ID группы)
        if not group_id.lstrip('-').isdigit():
            self.bot.send_message(message.chat.id, "ID группы должен быть числом")
            # raise ValueError("ID группы должен быть числом")

        give_response_json(json_name="whitelist", json_key=group_id, json_message={
            "sender": message.from_user.first_name,
            "sender_id": message.from_user.id,
            "type_message": message.chat.type,
            "data_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Формат: "2024-01-01 12:30:45"
        })
        give_response_json(json_name="user_states", json_key=message.chat.id, json_message=None)
        self.bot.send_message(message.chat.id, "ID добавлен")



    def add_link(self, message):
        print(message.text)
        try:
            chat = self.bot.get_chat(message.text)
            print(chat.id)
        except Exception as e:
            print("Ошибка:", e)
        # if 't.me' in message.text:
        #     # Пример: https://t.me/joinchat/AAAAAEEEEEEEEEE
        #     parts = message.text.split('/')
        #     group_id = parts[-1]
        # elif 'joinchat' in message.text:
        #     parts = message.text.split('joinchat/')
        #     group_id = parts[-1]
        # else:
        #     self.bot.send_message(message.chat.id, "Неверный формат ссылки-приглашения")
        #     # raise ValueError("Неверный формат ссылки-приглашения")
        # self.bot.send_message(message.chat.id, "ID добавлен" + str(group_id))

    def add_message(self, message):
        self.bot.send_message(message.chat.id, "Я пока так не умею")

