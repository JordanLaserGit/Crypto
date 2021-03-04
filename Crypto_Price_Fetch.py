import requests
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
from CryptoAPI import *
import pandas
import cbpro

class cryptoTools():

    def fetch_price_data_API(self,symbol,start):
        pair_split = symbol.split('/')  # symbol must be in format XXX/XXX ie. BTC/EUR
        symbol = pair_split[0] + '-' + pair_split[1]

        # SWITCH THIS BACK TO SPOT PRICE
        # USE WEBSOCKET AS OPPOSED TO POLLING PER COINBASE API
        # https://github.com/Marfusios/coinbase-client-websocket/blob/master/README.md
        api_url = f'https://api.pro.coinbase.com/'

        auth = CBProAuth(API_KEY, API_SECRET, API_PASS)

        response = requests.get(api_url + 'products/{}'.format(symbol), auth=auth)

        if response.status_code == 200:  # check to make sure the response from server is good
            theJSON = json.loads(response.text)
            print(theJSON)
            price = theJSON['data']['amount']
        else:
            print("Did not receieve OK response from Coinbase API")
            print("Status: {}".format(response.status_code))
            print('Text: {}'.format(response.text))
            print('Web Address: {}'.format(response.url))

        return price

    def fetch_price_history_data_API(self,symbol,start,end,granularity):
        pair_split = symbol.split('/')  # symbol must be in format XXX/XXX ie. BTC/EUR
        symbol = pair_split[0] + '-' + pair_split[1]

        api_url = f'https://api.pro.coinbase.com/'

        auth = CBProAuth(API_KEY, API_SECRET, API_PASS)

        # Get accounts
        response = requests.get(api_url + 'products/{}/candles?start={}&end={}&granularity={}'.format(symbol,start,end,granularity), auth=auth)

        if response.status_code == 200:  # check to make sure the response from server is good
            theJSON = json.loads(response.text)
            # print(theJSON)
            price = theJSON
        else:
            print("Did not receieve OK response from Coinbase API")
            print("Status: {}".format(response.status_code))
            print('Text: {}'.format(response.text))
            print('Web Address: {}'.format(response.url))

        return price
    
    def fetch_price_history_data_nonAPI(self,symbol,start,end,granularity):
        # define class
        public_client = cbpro.PublicClient()
        try:
            history = public_client.get_product_historic_rates(symbol, start, end, granularity)
        except:
            print('Error pulling historical data')
        return history

    def live_plotter(self,x_vec,y1_data,line1,identifier,plot_color,pause_time):
        if line1==[]:
            line1, = plt.plot(x_vec,y1_data,alpha=1,color = plot_color) 
           
            # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
            plt.pause(pause_time)
            
            # return line so we can update it again in the next iteration
            return line1

if __name__ == "__main__":
    symbol = 'BIT/USD'
    start = datetime.datetime.now()
    ctools = cryptoTools()
    ctools.fetch_price_data(symbol = symbol,start = start)

    x_vec = np.arange(10)
    y1_data = np.arange(10)
    line1 = []
    identifier = ''
    plot_color = 'blue'
    pause_time = 1
    ctools.live_plotter(x_vec = x_vec, y1_data = y1_data, line1 = line1, identifier = identifier, plot_color = plot_color, pause_time = pause_time)