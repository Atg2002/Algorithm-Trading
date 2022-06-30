# -*- coding: utf-8 -*-
"""
Created on Fri May  6 16:50:19 2022

@author: Krithikavvgreat
"""

import yfinance as yf
import pandas as pd

stocks = ["MSFT","AAPL","GOOG"]

ohlcv = {}
for stock in stocks:
    temp = yf.download(stock, period = "1mo", interval = "5m")
    temp.dropna(how = "any",inplace = True)
    ohlcv[stock] = temp
   
    
def MACD(DF, a=12, b=26, c=9):
    df = DF.copy()
    df["MACD"] = df["Adj Close"].ewm(span = a, min_periods =a ).mean() - df["Adj Close"].ewm(span = b, min_periods =b ).mean()
    df["signal"] = df["MACD"].ewm(span = c, min_periods =c ).mean()
    return df[["MACD", "signal"]]

for stock in stocks:
    ohlcv[stock][["MACD", "signal"]] = MACD(ohlcv[stock])