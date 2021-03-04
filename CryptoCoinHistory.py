from Crypto_Price_Fetch import *
import datetime
import time

# Define class
ctools = cryptoTools()

# we set which pair we want to retrieve data for
coin_list = ['ALGO-USD','ETH-USD','BTC-USD','XLM-USD','XTZ-USD','FIL-USD']

# Set sample rate [seconds between sample] and collection period
granularity = 60
hours_of_data = 4
pull_count = int(granularity) * hours_of_data
if pull_count >= 300:
    print('Granularity is too small for collection period, pull_count cannot exceed 300')
    exit()
genesis = datetime.datetime.now()
genesis_month = genesis.month
loop_month = genesis.month

historic_end = datetime.datetime.now()
historic_start = historic_end - datetime.timedelta(hours = hours_of_data)

for coin in coin_list:
    history = ctools.fetch_price_history_data_nonAPI(coin, start = historic_start, end = historic_end, granularity=granularity)
    print(history)

# price_time = []
# price_low = []
# price_high = []
# price_open = []
# price_close = []
# price_volume = []

# i = 0
# while i >= 0:
#     historic_end = datetime.datetime.now() - datetime.timedelta(hours = i*hours_of_data)
#     historic_start = historic_end - datetime.timedelta(hours = hours_of_data)

#     left = i * pull_count
#     right = (i + 1) * pull_count

#     print('Pulling {} price data from {} to {}'.format(token,historic_start,historic_end))

#     try:
#         # Fetch price
#         price_chunk = ctools.fetch_price_history_data(symbol=pair, start = historic_start.isoformat(), end = historic_end.isoformat(), granularity = granularity)
        
#         for data_time in range(pull_count):
#             price_time.append(price_chunk[data_time][0])
#             price_low.append(price_chunk[data_time][1])
#             price_high.append(price_chunk[data_time][2])
#             price_open.append(price_chunk[data_time][3])
#             price_close.append(price_chunk[data_time][4])
#             price_volume.append(price_chunk[data_time][5])

#     except:
#         print('Unable to pull historic data, loop count: {}'.format(i+1))

#     if historic_end.month != historic_start.month:
#         print('New month! Let\'s save the data to a netCDF')

#         # Get indicies that correspond to data within this month
#         month_list = [datetime.datetime.fromtimestamp(price).month for price in price_time]
#         month_list = np.asarray(month_list, dtype = np.float64)
#         here_month = np.where((month_list == loop_month))[0]
#         month_list_confirm = month_list[here_month]
#         not_month = month_list[~here_month]

#         # Check that data with only this month were retained
#         print('Month retained for data file, should only be a single month: {}'.format(np.unique(month_list_confirm)))
#         print('Month removed for data file: {}'.format(np.unique(not_month)))

#         # Convert lists to arrays for indexing
#         price_time_array = np.asarray(price_time, dtype = np.float64)
#         price_low_array = np.asarray(price_low, dtype = np.float64)
#         price_high_array = np.asarray(price_high, dtype = np.float64)
#         price_open_array = np.asarray(price_open, dtype = np.float64)
#         price_close_array = np.asarray(price_close, dtype = np.float64)
#         price_volume_array = np.asarray(price_volume, dtype = np.float64)

#         # Sort by time
#         [price_time_sorted, idx_sort] = [np.sort(price_time[here_month]), np.argsort(price_time[here_month])]

#         # Index 
#         price_low_sorted = price_low_array[idx_sort]
#         price_high_sorted = price_high_array[idx_sort]
#         price_open_sorted = price_open_array[idx_sort]
#         price_close_sorted = price_close_array[idx_sort]
#         price_volume_sorted = price_volume_array[idx_sort]

#     i = i + 1
#     time.sleep(0.25)