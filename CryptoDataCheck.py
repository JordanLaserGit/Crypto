import netCDF4
import os
import datetime

path = 'E:/CryptoData/ALGO-USD/'
filenames = os.listdir(path)

for f,infile in enumerate(filenames):
    file_path = os.path.join(path,infile)
    data = netCDF4.Dataset(file_path)
    print(file_path)
    try:
        print(datetime.datetime.fromtimestamp(data['TIME'][:][0]))
    except:
        continue
    # print(data['TIME'][:])