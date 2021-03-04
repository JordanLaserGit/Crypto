# First import the libraries that we need to use
import pandas as pd
import requests
import json
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np
from Crypto_Price_Fetch import *

# define class
ctools = cryptoTools()

# use style for more sophisticated visuals
# Put matplotlib in interactive mode for updating
plt.style.use('dark_background')
plt.ion()

# Initialize lists
PRICE_TIME = []
empty = []
roll_count = 0
count = -1

# we set which pair we want to retrieve data for
pair = 'ALGO/USD'
plot_color = 'cyan'
coin_matrix = np.ones((1,3600))*np.nan

# Create price figure
fig = plt.figure(figsize=(13,6))
plt.ylabel('Price (USD)')
plt.title('{}'.format(pair))
plt.grid(True,alpha = 0.3)

i = 1
time_genesis = datetime.datetime.now()

# Run fetch_price_data every second forever
while i > 0 :
    # Start time (official sample time)
    time_start = datetime.datetime.now()

    # Only plot X hours worth of data
    x_hrs = 1
    roll_switch = False
    if len(PRICE_TIME) > 0:
        delta_plotted_time = time_start - time_genesis
        if delta_plotted_time.seconds/3660 > x_hrs:
            PRICE_TIME = PRICE_TIME[1:]
            roll_switch = True
            roll_count = roll_count + 1
            plt.xlim(PRICE_TIME[0],PRICE_TIME[-1])

    PRICE_TIME.append(time_start)
    count = count + 1

    # Fetch price
    current_price = ctools.fetch_price_data(symbol=pair, start = time_start)

    # Update real time plotter
    # if roll_switch:
    #     ax[coin].set_xlim(PRICE_TIME[0],PRICE_TIME[-1])
    coin_matrix[0,count] = current_price
    coin_prices = coin_matrix[0,roll_count:len(PRICE_TIME) + roll_count]
    if count != 0:
        old_line.remove()
    old_line = ctools.live_plotter(x_vec = PRICE_TIME,y1_data = coin_prices,line1=empty,identifier = '{}'.format(pair),plot_color = plot_color,pause_time = 1)

    time_end = datetime.datetime.now()
    execution_time = time_end-time_start
    sleep_time = datetime.timedelta(seconds = 5)-execution_time
    sleep_time_seconds = sleep_time.microseconds/(10**6)
    # i = i + 1
    time.sleep(sleep_time_seconds)
