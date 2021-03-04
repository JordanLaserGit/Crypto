# First import the libraries that we need to use
import cbpro
import os
import time
import datetime
import numpy as np
import netCDF4 as nc
from Crypto_Price_Fetch import *

# define class
ctools = cryptoTools()
public_client = cbpro.PublicClient()

# we set which pair we want to retrieve data for
# [ time, low, high, open, close, volume ]
coin_list = ['ALGO-USD','ETH-USD','LINK-USD','UNI-USD',\
            'BTC-USD','XLM-USD','XTZ-USD','FIL-USD',\
            'ATOM-USD','WBTC-USD','AAVE-USD',\
                'GRT-USD','COMP-USD','DASH-USD',\
                    'ETC-USD','YFI-USD','UMA-USD','REN-USD','ZRX-USD','BNT-USD',\
                        'CGLD-USD','LRC-USD','OMG-USD','KNC-USD',\
                            'REP-USD','NU-USD','BAND-USD','BAL-USD','NMR-USD','OXT-USD']

genesis = datetime.datetime.utcnow()
genesis_month = genesis.month
loop_year = genesis.year
loop_month = genesis_month
loop_day = genesis.day

price_array = np.ones((len(coin_list),24*3600+100))*np.nan
time_array = np.ones((len(coin_list),24*3600+100))*np.nan

i = 0
while i >= 0:
    tick_count = i
    for c,coin in enumerate(coin_list):
        try:
            time.sleep(0.25)
            ticker_data = public_client.get_product_ticker(product_id=coin)
            # print(ticker_data)
            price = float(ticker_data['price'])
            time_tick = datetime.datetime(year = int(ticker_data['time'][:4]), month = int(ticker_data['time'][5:7]),\
                day = int(ticker_data['time'][8:10]),hour = int(ticker_data['time'][11:13]), \
                    minute = int(ticker_data['time'][14:16]),second = int(ticker_data['time'][17:19]))

            price_array[c,tick_count] =  price
            time_array[c,tick_count] = time_tick.timestamp()
            print('Current price of {}: ${} at {}'.format(coin,price,time_tick))
        except:
            print('Unable to request data at {}'.format(datetime.datetime.now()))
            continue

    i = i + 1

    # save to data file at the end of each day
    if loop_day != time_tick.day:
        print('New day! Let\'s save the data to a netCDF')

        cut = np.where(price_array == np.nan)[0]
        print(cut)
        price_array = price_array[:,:cut]
        time_array = time_array[:,:cut]

        # Open a write to netCDF
        outdir = 'E:\CryptoData\TickerData'
        outname = '{}_{}_{}.nc'.format(loop_year,loop_month,loop_day)
        outpath = os.path.join(outdir,outname)
        ncoin = len(coin_list)
        nt = cut
        try:
            fout = nc.Dataset(outpath,"w")
        except:
            print('Could not create {}'.format(outpath))

        # Create variables
        fout.createDimension('NTick',nt)
        fout.createDimension('NCoin',ncoin)

        coin = fout.createVariable('COIN_LIST','S1',('NCoin'))
        coin.long_name = 'List of coins'
        coin.units = ''

        time_price = fout.createVariable('TIME',np.int32,('NCoin','NTick'))
        time_price.long_name = 'Time'
        time_price.units = 'YYYY-MM-DD HH:MM:SS'

        price = fout.createVariable('PRICE',np.float32,('NCoin','NTick'))
        price.long_name = 'Price per coin'
        price.units = '$'


        # Write variables to nerCDF
        fout.variables['COIN_LIST'][:] = coin_list
        fout.variables['TIME'][:] = time_array
        fout.variables['PRICE'][:,:] = price_array

        fout.close()
        del fout

        # Reinitialize
        price_array = np.ones((len(coin_list),24*3600))*np.nan
        time_array = np.ones((len(coin_list),24*3600))*np.nan
        genesis = datetime.datetime.now()
        loop_year = genesis.year
        loop_month = genesis_month
        loop_day = genesis.day