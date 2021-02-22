import telebot
import psycopg2
import re
from api_utils import get_data, api_exchange_result, api_history_result

bot = telebot.TeleBot('1622944117:AAECB2DnUyHiHlSkWHIrjkiN4p3UruR7Zvc')


@bot.message_handler(commands=['start'])
def start_command(message):
    """
    Simple start message
    """
    bot.send_message(
       message.chat.id,
       'Greetings! I can show you exchangeratesapi.io exchange rates.\n' +
       'To get the exchange rates press /list.'
    )


@bot.message_handler(commands=['list'])
def list_command(message):
    """
    List or saves all currency rates
    """
    # conn = psycopg2.connect("host=localhost dbname=exchange_telegram_bot user=postgres password=123")
    conn = psycopg2.connect("""host=ec2-54-228-174-49.eu-west-1.compute.amazonaws.com dbname=d1avn6tj5dp6nq user=roveelrynqhhhh password=a1ec97e026438ca25e4131e45fc0d853b236b7ecdac114d91c186c657a33aee6""")

    data = get_data(conn)
    print(data)

    bot.send_message(
        message.chat.id,
        data
    )
    conn.close()


@bot.message_handler(commands=['exchange'])
def exchange(message):
    """
    Prints exchange rate for specific pair
    """
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
    """
    Prints historical data
    """
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

