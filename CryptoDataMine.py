# First import the libraries that we need to use
import os
import time
import datetime
from datetime import datetime
import numpy as np
import netCDF4 as nc
from Crypto_Price_Fetch import *

# define class
ctools = cryptoTools()

# we set which pair we want to retrieve data for
# [ time, low, high, open, close, volume ]
token = 'ALGO'
pair = token + '/USD'

# Set sample rate [seconds between sample] and collection period
granularity = '60'
hours_of_data = 4
pull_count = int(granularity) * hours_of_data
if pull_count >= 300:
    print('Granularity is too small for collection period, pull_count cannot exceed 300')
    exit()
genesis = datetime.datetime.now()
genesis_month = genesis.month
loop_month = genesis.month
date_loop = genesis.date()
fail_count = 0 

price_time = []
price_low = []
price_high = []
price_open = []
price_close = []
price_volume = []

i = 0
while i >= 0:
    historic_end = datetime.datetime.now() - datetime.timedelta(hours = i*hours_of_data)
    historic_start = historic_end - datetime.timedelta(hours = hours_of_data)
    
    left = i * pull_count
    right = (i + 1) * pull_count

    print('Pulling {} price data from {} to {}'.format(token,historic_start,historic_end))

    # try:
        # Fetch price
    price_chunk = ctools.fetch_price_history_data_API(symbol=pair, start = historic_start.isoformat(), end = historic_end.isoformat(), granularity = granularity)
    # print(price_chunk)
    for data_time in range(len(price_chunk)):
        price_time.append(price_chunk[data_time][0])
        price_low.append(price_chunk[data_time][1])
        price_high.append(price_chunk[data_time][2])
        price_open.append(price_chunk[data_time][3])
        price_close.append(price_chunk[data_time][4])
        price_volume.append(price_chunk[data_time][5])

    i = i + 1
    time.sleep(0.2)
    # print(price_chunk)

    if len(price_chunk) == 0:
        break

# Convert lists to arrays for indexing
price_time_array = np.asarray(price_time,dtype = np.int32)
price_time_array = np.asarray(price_time, dtype = np.float64)
price_low_array = np.asarray(price_low, dtype = np.float64)
price_high_array = np.asarray(price_high, dtype = np.float64)
price_open_array = np.asarray(price_open, dtype = np.float64)
price_close_array = np.asarray(price_close, dtype = np.float64)
price_volume_array = np.asarray(price_volume, dtype = np.float64)

# Sort by time
[price_time_sorted, idx_sort] = [np.sort(price_time_array), np.argsort(price_time_array)]

# Index 
price_low_sorted = price_low_array[idx_sort]
price_high_sorted = price_high_array[idx_sort]
price_open_sorted = price_open_array[idx_sort]
price_close_sorted = price_close_array[idx_sort]
price_volume_sorted = price_volume_array[idx_sort]

# Open a write to netCDF
outdir = 'E:\CryptoData\TickerData'
outname = '{}_{}.nc'.format(token,genesis.date())
outpath = os.path.join(outdir,outname)
nt = len(price_low_sorted)
try:
    fout = nc.Dataset(outpath,"w")
except:
    print('Could not create {}'.format(outpath))

# Create variables
fout.createDimension('NT',nt)

time_price = fout.createVariable('TIME',np.int32,('NT'))
time_price.long_name = 'Time'
time_price.units = 'YYYY-MM-DD HH:MM:SS'

low = fout.createVariable('PRICE_LOW',np.float32,('NT'))
low.long_name = 'Lowest price over time interval'
low.units = '$'

high = fout.createVariable('PRICE_HIGH',np.float32,('NT'))
high.long_name = 'Highest price over time interval'
high.units = '$'

open_price = fout.createVariable('PRICE_OPEN',np.float32,('NT'))
open_price.long_name = 'Price at beginning of interval'
open_price.units = '$'

close_price = fout.createVariable('PRICE_CLOSE',np.float32,('NT'))
close_price.long_name = 'Price at end of interval'
close_price.units = '$'

volume = fout.createVariable('PRICE_VOLUME',np.float32,('NT'))
volume.long_name = 'Volume'
volume.units = '$'

# Write variables to nerCDF
# fout.variables['TIME'][:] = nc.stringtochar(np.asarray([datetime.datetime.fromtimestamp(int(price)).strftime('%Y-%m-%d %H:%M:%S') for price in price_time_sorted],dtype = np.float32),'S4')
fout.variables['TIME'][:] = price_time_sorted
fout.variables['PRICE_LOW'][:] = price_low_sorted
fout.variables['PRICE_HIGH'][:] = price_high_sorted
fout.variables['PRICE_OPEN'][:] = price_open_sorted
fout.variables['PRICE_CLOSE'][:]= price_close_sorted
fout.variables['PRICE_VOLUME'][:] = price_volume_sorted

fout.close()
del fout

# Reinitialize lists with left over data (data collected in loop_month that didn't belong)
# price_time = list(price_time_array[not_month_idx])
# price_low = list(price_low_array[not_month_idx])
# price_high = list(price_high_array[not_month_idx])
# price_open = list(price_open_array[not_month_idx])
# price_close = list(price_close_array[not_month_idx])
# price_volume = list(price_volume_array[not_month_idx])

# if loop_month != 1:
#     loop_month = loop_month - 1
# else:
#     loop_month = 12