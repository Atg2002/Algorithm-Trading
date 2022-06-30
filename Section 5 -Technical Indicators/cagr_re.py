# -*- coding: utf-8 -*-
"""
Created on Sat May 28 20:33:55 2022

@author: Krithikavvgreat
"""

import yfinance as yf
import numpy as np

stocks = ["AMZN", "GOOG", "MSFT"]
ohlcv = {}
for stock in stocks:
    temp = yf.download(stock, period = "7mo", interval = "1d")
    temp.dropna(how = "any", inplace = True)
    ohlcv[stock] = temp

def CAGR1(DF, n):
    df = DF.copy()
    df["1+pct_change"] = 1+df["Adj Close"].pct_change()
    cagr = (df["1+pct_change"].prod() )**(1/n) -1
    return cagr

for stock in stocks:
    print("CAGR for{} is : {}".format(stock, CAGR1(ohlcv[stock], len(ohlcv[stock])/252)))

'''    
def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["return"] = DF["Adj Close"].pct_change()
    df["cum_return"] = (1 + df["return"]).cumprod()
    n = len(df)/252
    CAGR = (df["cum_return"][-1])**(1/n) - 1
    return CAGR

for ticker in ohlcv_data:
    print("CAGR of {} = {}".format(ticker,CAGR(ohlcv_data[ticker])))'''