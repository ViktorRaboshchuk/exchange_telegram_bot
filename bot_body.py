import telebot
import psycopg2
import re
from api_utils import get_data, api_exchange_result, api_history_result

bot = telebot.TeleBot('1622944117:AAECB2DnUyHiHlSkWHIrjkiN4p3UruR7Zvc')


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
       message.chat.id,
       'Greetings! I can show you exchangeratesapi.io exchange rates.\n' +
       'To get the exchange rates press /list.\n'
    )


@bot.message_handler(commands=['list'])
def start_command(message):

    conn = psycopg2.connect("host=localhost dbname=exchange_telegram_bot user=postgres password=123")

    data = get_data(conn)
    print(data)

    bot.send_message(
        message.chat.id,
        data
    )
    conn.close()


@bot.message_handler(commands=['exchange'])
def exchange(message):
    message_text = message.text
    amount = int(re.search(r'\d+', message.text).group())
    curr_1 = message_text.split(' ')[2]
    curr_2 = message_text.split(' ')[4]

    rate = api_exchange_result(curr_1, curr_2)

    bot.send_message(
        message.chat.id,
        "{:.2f}".format(amount * rate[curr_2])
    )


@bot.message_handler(commands=['history'])
def history_graph(message):
    message_text = message.text
    history_pair = message_text.split(' ')
    curr_1, curr_2 = history_pair[1].split('/')
    days = int(re.search(r'\d+', message.text).group())

    hist_graph, response_length = api_history_result(message_text, days, curr_1, curr_2)

    if response_length == 0:

        bot.send_message(
            message.chat.id,
            'No exchange data available for the selected currencies'
        )
    else:
        bot.send_photo(
            message.chat.id,
            photo=open('charts/{}_{}_{}.png'.format(curr_1, curr_2, hist_graph), 'rb')
        )


if __name__ == '__main__':
    bot.polling(none_stop=True)

