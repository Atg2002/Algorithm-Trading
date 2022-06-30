# -*- coding: utf-8 -*-
"""
Created on Tue May 24 13:33:55 2022

@author: Krithikavvgreat
"""

import yfinance as yf
import numpy as np

stocks = ["AMZN", "GOOG", "MSFT"]
ohlcv = {}
for stock in stocks:
    temp = yf.download(stock, period = "1mo", interval = "5m")
    temp.dropna(how = "any", inplace = True)
    ohlcv[stock] = temp
    
def rsi(DF,n=14):
    df = DF.copy()
    df["diff"] = df["Adj Close"] - df["Adj Close"].shift(1)
    df["Gain"] = np.where(df["diff"]>0, df["diff"], 0)
    df["Loss"] = np.where(df["diff"]<0, abs(df["diff"]), 0)
    df["Avg Gain"] = df["Gain"].ewm(alpha = 1/n, min_periods = n).mean()
    df["Avg Loss"] = df["Loss"].ewm(alpha = 1/n, min_periods = n).mean()
    df["RS"] = df["Avg Gain"]/df["Avg Loss"]
    df["RSI"] = 100 - (100/(1+df["RS"]))
    return df["RSI"]

for stock in stocks:
    ohlcv[stock]["RSI"] = rsi(ohlcv[stock])