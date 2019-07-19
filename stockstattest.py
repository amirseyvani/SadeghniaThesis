import stockstats as ss
import pandas as pd
import lda as l
import numpy as np





def dash_date(da):
    y = da[0:4]
    m = da[4:6]
    d = da[6:8]
    return str(y)+'-'+str(m)+'-'+str(d)


def  edit_date(df):
    df['Date'][:] = [dash_date(str(da)) for da in df['Date']]
    return df

def getEMA(df):
    print('test')

df = (pd.read_csv('Data/sfars.csv'))
stock = ss.StockDataFrame.retype(df)

ema = getEMA(stock)
cci_20 = stock['cci']
adx_14 = stock['adx']
