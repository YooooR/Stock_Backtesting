import getStock
import pandas as pd
import numpy as np
import datetime
import time

import matplotlib.pyplot as plt

data = {}
n_days = 4
date = datetime.datetime.now()
fail_count = 0
allow_continuous_fail_count = 5
while len(data) < n_days:

    print('parsing', date)
    # 使用 crawPrice 爬資料
    try:
        # 抓資料
        data[date.date()] = getStock.crawl_all(date)
        print('success!')
        fail_count = 0
    except:
        # 假日爬不到
        print('fail! check the date is holiday')
        fail_count += 1
        if fail_count == allow_continuous_fail_count:
            raise
            
    
    # 減一天
    date -= datetime.timedelta(days=1)
    time.sleep(10)

#print(data[datetime.date(2020, 2, 19)])

close = pd.DataFrame({k:d['收盤價'] for k,d in data.items()}).transpose()
close.index = pd.to_datetime(close.index)

open = pd.DataFrame({k:d['開盤價'] for k,d in data.items()}).transpose()
open.index = pd.to_datetime(open.index)

high = pd.DataFrame({k:d['最高價'] for k,d in data.items()}).transpose()
high.index = pd.to_datetime(high.index)

low = pd.DataFrame({k:d['最低價'] for k,d in data.items()}).transpose()
low.index = pd.to_datetime(low.index)

volume = pd.DataFrame({k:d['成交股數'] for k,d in data.items()}).transpose()
volume.index = pd.to_datetime(volume.index)

tsmc = {
    'close':close['2330']['2020'].dropna().astype(float),
    'open':open['2330']['2020'].dropna().astype(float),
    'high':high['2330']['2020'].dropna().astype(float),
    'low':low['2330']['2020'].dropna().astype(float),
    'volume': volume['2330']['2020'].dropna().astype(float),
}

plt.plot(tsmc['close'])
plt.show()