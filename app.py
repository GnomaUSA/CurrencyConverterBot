import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = (f'Здравствуйте, {message.chat.username}! Я маленький помощник :) Я умею переводить валюту по актуальному курсу'
            f'\n\nДля конвертации валюты введите:'
            f'\n * имя валюты'
            f'\n * в какую валюту перевести'
            f'\n * количество переводимой валюты'
            f'\n\nНажмите /values, чтобы увидеть все доступные валюты'
            f'\n\nЕсли Вы что-то забудите нажмите /help')
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = (f'{message.chat.username}! Я всегда готов помочь! Я умею переводить валюту по актуальному курсу'
            f'\n\nДля конвертации валюты введите:'
            f'\n * имя валюты'
            f'\n * в какую валюту перевести'
            f'\n * количество переводимой валюты'
            f'\n\nНажмите /values, чтобы увидеть все доступные валюты')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n*'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Некорректное количество параметров')

        base, quote, amount = values
        total_base = CurrencyConverter.convert(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось выполнить команду\n{e}')
    else:
        text = f'Переводим {base} в {quote} \n{amount} {base} = {total_base} {quote}'

        #f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}
        bot.send_message(message.chat.id, text)

bot.polling()