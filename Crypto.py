# First import the libraries that we need to use
import pandas as pd
import requests
import json
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np
import Crypto_Price_Fetch

# use ggplot style for more sophisticated visuals
plt.style.use('dark_background')

ALGO_LIST_PRICE_SECONDS = []
ETH_LIST_PRICE_SECONDS = []
PRICE_TIME = []
empty = []

# we set which pair we want to retrieve data for
pair_list = ["ALGO/USD", "ETH/USD","XLM/USD","XTZ/USD","FIL/USD"]
plot_color_list =['grey','green','yellow','cyan','blue']
coin_matrix = np.ones((len(pair_list),24*3600))*np.nan

# Create figure for real time plotter
# this is the call to matplotlib that allows dynamic plotting
plt.ion()

for i_plot in range(len(pair_list)):
    fig = plt.figure(figsize=(13,6))
    fig, ax1 = fig.add_subplot(111)
    ax = fig.add_subplot(111)
    ax.set_ylabel('Price (USD)')
    ax.set_title('{}'.format(pair_list[i_plot]))
    plt.grid(True,alpha = 0.3)

if __name__ == "__main__":

    ctools = cryptoTools()

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
            delta_plotted_time = time_start - PRICE_TIME[0]
            if delta_plotted_time.seconds/60 > x_hrs:
                PRICE_TIME = PRICE_TIME[1:]
                roll_switch = True

        PRICE_TIME.append(time_start)
        count = len(PRICE_TIME)-1

        # Fetch price
        current_prices = ctools.fetch_price_data(symbols=pair_list, start = time_start,genesis = time_genesis, count = i)

        # Update real time plotter
        for coin in range(len(pair_list)):
            if roll_switch:
                ax[coin].set_xlim(PRICE_TIME[0],PRICE_TIME[-1])
            coin_matrix[coin,count] = current_prices[coin]
            coin_prices = coin_matrix[coin,:len(PRICE_TIME)]
            ctools.live_plotter(x_vec = PRICE_TIME,y1_data = coin_prices[:len(PRICE_TIME)],line1=empty,identifier = '{}'.format(pair_list[coin]),plot_color = plot_color_list[coin],plot_index = coin)

        time_end = datetime.datetime.now()
        execution_time = time_end-time_start
        sleep_time = datetime.timedelta(seconds = 5)-execution_time
        sleep_time_seconds = sleep_time.microseconds/(10**6)
        # i = i + 1
        time.sleep(sleep_time_seconds)


# Code to try to write flowing data to text file.
# myFile = 'ALGO log.txt'

# with open(myFile,'r+')as fin:
#     entries = open(myFile,'r')
#     number_entries = len(entries.readlines())
    
#     if number_entries != 0:
#             # If txt file is empty, fill first line with current data
#             if number_entries == 0:
#                 fin.write('{}: {}\n'.format(start, theJSON))
#             # If txt file is not empty, fill first line with current data and shift every other data entry down a line
#             else:
#                 fin.seek(0)
#                 fin.write('{}: {}\n'.format(start, theJSON))
#                 for line_idx in range(number_entries):
#                     fin.seek(number_entries + 1 + line_idx)
#                     fin.write('{}: {}\n'.format(start, entries))
#     else:
#         fin.write('{}: {}\n'.format(start, theJSON))
# fin.close()