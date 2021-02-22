from io import StringIO

import matplotlib.pyplot as plt
import requests
import json
import datetime
from datetime import date
from db_utils import insert_values, get_last_data, get_last_timestamp
import matplotlib
matplotlib.use('Agg')


def get_data(conn):

    data_list = []
    text = ' \n'

    curr_time = datetime.datetime.now()

    db_timestamp = get_last_timestamp(conn)[0][0]
    dates_difference = (curr_time - db_timestamp).seconds/60
    print('TIME DIFFERENCE             ', dates_difference)

    if dates_difference > 10:

        response = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
        json_data = json.loads(response.content)

        for curr, val in json_data['rates'].items():
            data_list.append('  '.join((curr, str("{:.2f}".format(val)))))
            insert_values(conn, curr, str("{:.2f}".format(val)), curr_time)
            txt = text.join(data_list)
        return txt

    else:
        last_db_data = get_last_data(conn)
        for row in last_db_data:
            # api_data = curr, str("{:.2f}".format(val))
            data_list.append('  '.join((row[0], row[1])))
            txt = text.join(data_list)
        return txt


def api_exchange_result(curr_1, curr_2):
    response = requests.get('https://api.exchangeratesapi.io/latest?symbols={}&base={}'.format(curr_2, curr_1))
    json_data = json.loads(response.content)
    ex_rate = json_data['rates']

    return ex_rate


def api_history_result(message_text, days, curr_1, curr_2):

    curr_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    d2 = (today - datetime.timedelta(days=days))
    response = requests.get('https://api.exchangeratesapi.io/history?start_at={}&end_at={}&base={}&symbols={}'.format(d2, d1, curr_1, curr_2))
    json_data = json.loads(response.content)

    json_response = json_data['rates']

    history_data = []
    for (day, val) in json_data['rates'].items():
        history_data.append(val[curr_2])

    plt.plot(history_data, color='green', marker='o')
    plt.xlabel(days)
    plt.ylabel('{}/{}'.format(curr_1, curr_2))
    plt.title(' '. join(message_text.split(' ')[1:]))
    plt.savefig('charts/{}_{}_{}.png'.format(curr_1, curr_2, curr_time))
    plt.close()

    return curr_time, len(json_response)

