# This script will alert on crypto coin prices that surpass predefined thresholds
import cbpro
from datetime import datetime
import time
from EmailCryptoAlert import *

email = Emailer()

public_client = cbpro.PublicClient()

# Set coin_list and associated buy/sell prices
coin_list = [['ALGO-USD','ETH-USD','BTC-USD','XLM-USD','XTZ-USD','FIL-USD'],
            [1.10,1300,45000,0.35,3.10,32.00],\
            [1.30,2000,55000,0.50,5.00,45]]\

i = 0
while i >= 0:
    for c,coin in enumerate(coin_list[0][:]):
        try:
            ticker_data = public_client.get_product_ticker(product_id=coin)
            price = float(ticker_data['price'])
            time_tick = ticker_data['time']
            print('Current price of {}: ${} at {}'.format(coin,price,time_tick))
            time.sleep(1)
        except:
            print('Unable to request data at {}'.format(datetime.now()))
            continue

        # Send alert if price is below buy_price
        if price <= coin_list[1][c]:
            recepient = 'jordan.laser@hotmail.com'
            subject = 'Coin Price Alert: {}'.format(coin)
            content = '{} price has dropped below {}\n Current price: {}\n Ticker time: {}'.format(coin,coin_list[1][c],price,time_tick)
            email.sendmail(recepient,subject,content)
            exit()
            # user_input = input('Continue to alert on {}?'.format(coin))
            # if user_input != 'No':
            #     continue
            # else:
            #     coin_list = coin_list[~c]
            #     buy_list = buy_list[~c]
            #     sell_list = sell_list[~c]
        # Send alert if price is above sell_price
        elif price >= coin_list[2][c]:
            recepient = 'jordan.laser@hotmail.com'
            subject = 'Coin Price Alert: {}'.format(coin)
            content = '{} price has risen above {}\n Current Price: {}, Ticker time: {}'.format(coin,coin_list[2][c],price,time_tick)
            email.sendmail(recepient,subject,content)
            exit()
            # user_input = input('Continue to alert on {}?'.format(coin))
            # if user_input != 'No':
            #     continue
            # else:
            #     coin_list = coin_list[~c]
            #     buy_list = buy_list[~c]
            #     sell_list = sell_list[~c]
        else:
            continue
        time.sleep(0.25)