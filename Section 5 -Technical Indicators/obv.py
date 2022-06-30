#import yfinance as yf
import numpy as np
import datetime as dt
tickers = ["AMZN","GOOG","MSFT"]

ohlc_data = {}
start = dt.date.today()-dt.timedelta(1825)
end = dt.datetime.today()
for ticker in tickers:
    temp = yf.download(ticker, interval = "1d", start = start, end = end)
    temp.dropna(inplace =True)
    ohlc_data[ticker] = temp
    
def OBV(DF):
    df = DF.copy()
    df["change"] = df["Adj Close"].pct_change()
    df["direction"] = np.sign(df["change"])
    df["Vol_new"] = df["Volume"] * df["direction"]
    df["Vol_new"].iat[0] = 0
    df["OBV"] = df["Vol_new"].cumsum()
    return df["OBV"]
for ticker in tickers:
    ohlc_data[ticker]["OBV"] = OBV(ohlc_data[ticker])
    
ticker = "AMZN"
ohlcv = yf.download(ticker,dt.date.today()-dt.timedelta(1825),dt.datetime.today())
'''
In sirs code he has used obv = obv_prev + vol(if change>=0)/ -vol(if change<0) wherease I have use 
                         obv = obv_prev + vol(if change> 0)/ -vol(if change<0) /0(if change =0)
'''
def OBV(DF):
    """function to calculate On Balance Volume"""
    df = DF.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()
    df['direction'] = np.where(df['daily_ret']>=0,1,-1)
    df['direction'].iat[0] = 0
    df['vol_adj'] = df['Volume'] * df['direction']
    df['obv'] = df['vol_adj'].cumsum()
    return df['obv']

ohlcv["obv"] = OBV(ohlcv)
