# -*- coding: utf-8 -*-
"""
Created on Tue May 24 13:33:55 2022

@author: Krithikavvgreat
"""

import yfinance as yf
import numpy as np

# Download historical data for required stocks
tickers = ["AMZN","GOOG","MSFT"]
ohlcv_data = {}
hour_data = {}
renko_data2 = {}

# looping over tickers and storing OHLCV dataframe in dictionary
for ticker in tickers:
    temp = yf.download(ticker,period='1mo',interval='5m')
    temp.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = temp
    temp = yf.download(ticker,period='1y',interval='1h')
    temp.dropna(how="any",inplace=True)
    hour_data[ticker] = temp
    
def ATR(DF, n=14):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df["H-L"] = df["High"] - df["Low"]
    df["H-PC"] = abs(df["High"] - df["Adj Close"].shift(1))
    df["L-PC"] = abs(df["Low"] - df["Adj Close"].shift(1))
    df["TR"] = df[["H-L","H-PC","L-PC"]].max(axis=1, skipna=False)
    df["ATR"] = df["TR"].ewm(com=n, min_periods=n).mean()
    return df["ATR"]

def renko_DF(DF, hourly_df):
    "function to convert ohlc data into renko bricks"
    df = DF.copy()
    base = df["Adj Close"][0]
    brick_size = 3*round(ATR(hourly_df,120).iloc[-1],0)
    up_trend = -1
    df["up_trend"] = None
    df["down_trend"] = None
    i=0
    for elem in df["Adj Close"]:
        
        if (elem- base)>brick_size and up_trend == -1:
            base = elem
            up_trend = True
            df["up_trend"].iat[i] = True
        
        elif (elem-base)<0 and abs(base-elem)>brick_size and up_trend == -1:
            up_trend = False
            base = elem
            df["down_trend"].iat[i] = True
            
        elif (elem- base)>brick_size and up_trend:
            base = elem
            df["up_trend"].iat[i] = True
        
        elif (elem-base)<0 and abs(base-elem)>2*brick_size and up_trend:
            up_trend = False
            base = elem
            df["down_trend"].iat[i] = True
        
        elif (elem- base)>2*brick_size and not up_trend:
            base = elem
            up_trend = True
            df["up_trend"].iat[i] = True
        
        elif (elem-base)<0 and abs(base-elem)>brick_size and not up_trend:
            base = elem
            df["down_trend"].iat[i] = True
        i+=1
    df.dropna(how = "all", subset = ["up_trend", "down_trend"], inplace = True)
    df["uptrend"] = np.where(df["up_trend"] == True, True, False)
    df.drop(["up_trend", "down_trend"], axis = 1, inplace = True)
    return df

for ticker in tickers:
    renko_data2[ticker] = renko_DF(ohlcv_data[ticker], hour_data[ticker])