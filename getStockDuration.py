import getStock
import pandas as pd
import numpy as np
import datetime
import time

data = {}
n_months = 2
date = datetime.date.today()

current_day = date.day
first_day = datetime.date(day=1, month=date.month, year=date.year)

fail_count = 0
allow_continuous_fail_count = 5
for i in range(n_months):

    #一個月只撈一次
    print('parsing', date)
    month_data = getStock.crawl_stock(date,'2330')
    
    # 使用 crawPrice 爬資料
    try:
        # 抓資料
        month_data = getStock.crawl_stock(date,'2330')            
        print('success!')
        fail_count = 0

        data_col = month_data.shape[0] - 1
    except:
        # 假日爬不到
        print('fail! check the date is holiday')
        fail_count += 1
        if fail_count == allow_continuous_fail_count:
            raise 
       
    for j in range(date.day):
        if date.weekday() != 5 and date.weekday() != 6 :
            data[date] = month_data.iloc[data_col,:]
            data_col -= 1

        date -= datetime.timedelta(days=1)
       
    # 減一月    
    date = first_day - datetime.timedelta(days=1)
    #date -= datetime.timedelta(days=1)

    #不要撈太快, 避免被鎖IP
    time.sleep(10)

"""
for k,d in data.items():
    print(k)

dir = {
    int(str(k.year)+str(k.month)+str(k.day)):d['收盤價'] for k,d in data.items()
}
"""

close = pd.DataFrame({k:d['收盤價'] for k,d in data.items()},index=[0]).transpose()
close.index = pd.to_datetime(close.index)
close

