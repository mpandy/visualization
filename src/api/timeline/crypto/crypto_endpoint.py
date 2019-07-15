import json
import pygal
from src.api.restplus import api
from flask import render_template, send_from_directory
from flask_restplus import Resource
from src import settings


ns = api.namespace('timeline', description='A customizable timeline graph')

@ns.route('/crypto/<interval_days>')
@ns.doc(params={'interval_days': 'time interval (in days)'})
class CryptoTImeline(Resource):

    def get(self, interval_days):
        time_series_key = "Time Series (Digital Currency Daily)"

        with open(settings.DATASET_PATH + '/crypto/BCH.json') as json_file:
            bch = json.load(json_file)[time_series_key]
        with open(settings.DATASET_PATH + '/crypto/DASH.json') as json_file:
            dash = json.load(json_file)[time_series_key]
        with open(settings.DATASET_PATH + '/crypto/ETH.json') as json_file:
            eth = json.load(json_file)[time_series_key]
        with open(settings.DATASET_PATH + '/crypto/LTC.json') as json_file:
            ltc = json.load(json_file)[time_series_key]
        with open(settings.DATASET_PATH + '/crypto/XMR.json') as json_file:
            xmr = json.load(json_file)[time_series_key]

        x_labels = list(dash)[:int(interval_days)]

        dash_list = []
        ethereum_list = []
        bitcoin_cash_list = []
        litecoin_list = []
        monero_list = []

        for label in x_labels:
            dash_list.append(int(float(dash[label]['1a. open (EUR)'])))
            ethereum_list.append(int(float(eth[label]['1a. open (EUR)'])))
            bitcoin_cash_list.append(int(float(bch[label]['1a. open (EUR)'])))
            litecoin_list.append(int(float(ltc[label]['1a. open (EUR)'])))
            monero_list.append(int(float(xmr[label]['1a. open (EUR)'])))

        bitcoin_cash_list.reverse()
        dash_list.reverse()
        ethereum_list.reverse()
        litecoin_list.reverse()
        monero_list.reverse()

        graph = pygal.Line(title='Cryptocurrencies prices in last '+interval_days+' days', x_title='Day', y_title='Price(€)',
                           width=1500, x_label_rotation=20)
        labels = [x.split('-')[1] + '/' + x.split('-')[2] for x in x_labels]
        labels.reverse()
        graph.x_labels = labels
        graph.add('Bitcoin Cash', bitcoin_cash_list)
        graph.add('Dash', dash_list)
        graph.add('Ethereum', ethereum_list)
        graph.add('Litecoin', litecoin_list)
        graph.add('Monero', monero_list)

        # graph.render_data_uri()
        # return render_template("graphing.html", chart=graph)

        graph.render_to_file(settings.CHART_TMP_FOLDER + '/chart.svg')
        return send_from_directory(settings.CHART_TMP_FOLDER, 'chart.svg', as_attachment=True)
