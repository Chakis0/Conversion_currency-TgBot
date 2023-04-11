import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('6148860517:AAEbcrq8HzMZw5q-I9Jnc6Y9rD1CkKcRZso')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. Введите сумму')
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/KRW', callback_data='usd/krw')
        btn2 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
        btn3 = types.InlineKeyboardButton('RUB/KRW', callback_data='rub/krw')
        btn4 = types.InlineKeyboardButton('KRW/USD', callback_data='krw/usd')
        btn5 = types.InlineKeyboardButton('Другое', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, 'Выберите валюты',
                         reply_markup=markup)
    else:
        bot.send_message(
            message.chat.id, 'Число должно быть больше 0. Введите сумму')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id,
                         f'В данный момент: {round(res, 2)}')
      #   bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id,
                         'Введите пару значений, через /')
        bot.register_next_step_handler(call.message, mycurrency)


def mycurrency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'В данный момент: {res}')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так((')
        bot.register_next_step_handler(message, summa)


bot.polling(none_stop=True)
