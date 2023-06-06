import telebot
from config import TOKEN, keys
from extensions import APIException, СurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести><количество переводимой валюты>\nПример: доллар рубль 1\nУвидеть список всех доступных валют: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:\n'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert(message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное количество параметров.')

        base, quote, amount = values
        total_base = СurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {round(total_base, 2)}'
        bot.send_message(message.chat.id, text)

bot.polling()