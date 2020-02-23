import requests
from io import StringIO
import pandas as pd
import numpy as np

import datetime
import time

def crawl_all(date):
    r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + str(date).split(' ')[0].replace('-','') + '&type=ALL')
    print(r.text)
    ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                        for i in r.text.split('\n') 
                                        if len(i.split('",')) == 17 and i[0] != '='])), header=0)
    print(ret)
    ret = ret.set_index('證券代號')
    ret['成交金額'] = ret['成交金額'].str.replace(',','')
    ret['成交股數'] = ret['成交股數'].str.replace(',','')
    return ret

def crawl_stock(date, stockNo):
    r = requests.post('http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date=' + str(date) + '&stockNo=' + str(stockNo))
   # print(r.text)
    ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                        for i in r.text.split('\n')
                                            if len(i.split('",')) == 10 and i[0] != '='])), header=0)
    
    #ret = pd.read_csv(r.text)
   # print(ret)
    ret = ret.set_index('日期')
    ret['成交金額'] = ret['成交金額'].str.replace(',','')
    ret['成交股數'] = ret['成交股數'].str.replace(',','')
    return ret
"""
#撈每一隻股票資料
#test = crawl_all("2020-02-21 11:38:35.231800")

#撈特定日期, 特定股票
test = crawl_stock("20200101","2330")
df = pd.DataFrame(test)

#全部資料:
#df.index[0] 
#日期 
#df.iloc[:,0] to df.iloc[:,7]
#成交股數, 成交金額, 開盤價, 最高價, 最低價, 收盤價, 漲跌價差, 成交筆數
print(df)

#某一天的收盤價
print(str(df.index[0]) + "日, 成交張數=" + str(int(df.iloc[0,0])/1000) +", 收盤價=" + str(df.iloc[0,5]))


#to-do: 指標, 趨勢, 周月K
"""