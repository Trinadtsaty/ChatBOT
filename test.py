import telebot

# Замените 'YOUR_TOKEN' на ваш токен
bot = telebot.TeleBot('YOUR_TOKEN')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я тестовый бот.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Запуск бота
bot.polling()