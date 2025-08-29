
import telebot
from bot.handlers import Start, Handlers_Text_Analysis, Help, Error, Median_Arithmetic_Mean, WorkComands
from bot.buttons import Buttons, Whitelist
from .defs import get_response_json
from .math import Median, ArithmeticMean, MedianAndArithmeticMean


class Comands:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

        self.start_bot = Start(self.bot)
        self.buttons = Buttons(self.bot)
        self.echo_handler = Handlers_Text_Analysis(self.bot)
        self.help = Help(self.bot)
        self.error = Error(self.bot)
        self.median_arithmetic = Median_Arithmetic_Mean(self.bot)
        self.count = Median_Arithmetic_Mean(self.bot)
        self.whitelist = Whitelist(self.bot)
        self.work_comands = WorkComands(self.bot)

        self.median = Median(self.bot)
        self.mean = ArithmeticMean(self.bot)
        self.together_mean_median = MedianAndArithmeticMean(self.bot)

    def register_handlers(self):
        @self.bot.message_handler(commands=['start', 'Start'])
        def start(message):
            self.start_bot.handle(message)

        @self.bot.message_handler(commands=['help', 'Help'])
        def help(message):
            self.help.handle(message)

        @self.bot.message_handler(commands=['counting', 'Counting'])
        def counting(message):
            self.count.handle(message)

        @self.bot.message_handler(commands=['whitelist', 'Whitelist'])
        def whitelist(message):
            self.whitelist.message_type_id(message)

        @self.bot.message_handler(commands=['stop', 'Stop'])
        def stop(message):
            self.work_comands.stop(message)

        @self.bot.message_handler(commands=['Yes', 'yes'])
        def Yes(message):
            self.work_comands.yes(message)

        @self.bot.message_handler(commands=['No', 'no'])
        def No(message):
            self.work_comands.no(message)

        @self.bot.message_handler(commands=['create_graf', 'Create_graf'])
        def create_graf(message):
            dict = get_response_json(json_name="user_states", json_key=message.chat.id)
            if dict and dict["states"] == "Computation":
                if dict["tipe"] == "Median":
                    self.median.create_graf(message)
                elif dict["tipe"] == "ArithmeticMean":
                    self.mean.create_graf(message)
                elif dict["tipe"] == "MedianAndArithmeticMea":
                    self.together_mean_median.create_graf(message)
            else:
                self.error.get_unknown_command(message)



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