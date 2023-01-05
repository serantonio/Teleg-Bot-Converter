import telebot
from config import keys, TOKEN
from extensions import ConvertionExeption, ValueConveter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start_comm(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Ку-ку, {message.chat.username}")


@bot.message_handler(commands=["help"])
def help_comm(message: telebot.types.Message):
    text = "Для того, чтобы начать со мной работу, введите команду в следующей форме:\n" \
           "\n"\
           "<Валюта>, которую вы хотите конвертировать\n"\
           "<Валюта>, в котору вы хотите конвертировать\n"\
           "<Сумма>\n"\
           "Пример - доллар рубль 1000 (конвертировать 1000 долларов в рубли)\n" \
           "\n" \
           "Увидеть список всех доступных валют можно при помощи команды /values"\

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["values"])
def values_comm(message: telebot.types.Message):
    text = "Доступные валюты"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def convertion(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionExeption("Введите по примеру из /help")

        quote, base, amount = values
        total_base = ValueConveter.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду.\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling()