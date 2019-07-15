import requests
import json
import os
from datetime import date
from src import settings

today = date.today()
crypto_data_folder_path = settings.DATASET_PATH + '/crypto'

def overwrite_file(currency_data, param):
    if os.path.isfile(param):
        os.remove(param)
    with open(param, 'w') as outfile:
        json.dump(currency_data, outfile)


def save_alphavantage_digital_currency_daily(currncy):

    url = "https://www.alphavantage.co/query"
    params = {'function': 'DIGITAL_CURRENCY_DAILY', 'market': 'EUR', 'apikey':'7Q781R33LC06GR2Y'}

    try:
        params['symbol'] = currncy
        currency_data = requests.get(url=url, params=params).json()

    except Exception as e:
        return "alphavantage not responding"

    overwrite_file(currency_data, settings.DATASET_PATH + '/crypto/'+ currncy+'.json')
    print(currncy + ' updated on', today)


def create_cryptto_folder_if_not_exist():

    if os.path.isdir(crypto_data_folder_path) is False:
        try:
            os.mkdir(crypto_data_folder_path)
        except OSError:
            print("Creation of the directory %s failed" % crypto_data_folder_path)
        else:
            print("Successfully created the directory %s " % crypto_data_folder_path)

