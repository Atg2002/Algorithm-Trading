# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 14:20:20 2022

@author: Krithikavvgreat
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
stocks = ["RELIANCE.NS", "INFY.NS", "SBICARD.NS", "HDFCBANK.NS", "ITC.NS"]

ohlc = {}

for stock in stocks:
   temp = yf.download(stock, period = "1mo", interval = "15m")
   temp.dropna(how = "any", inplace =True)
   ohlc[stock] = temp


def MACD(DF, a=12, b=26, c=9):
    df = DF.copy()
    df["fast_emv"] =df["Adj Close"].ewm(span = a, min_periods = a).mean()
    df["slow_emv"] =df["Adj Close"].ewm(span = b, min_periods = b).mean()
    df["mcd"] = df["fast_emv"]  -df["slow_emv"]
    df["signal"]   =df["mcd"].ewm(span = c, min_periods = c).mean() 
    
    return df.loc[:, ["mcd", "signal"]]

for stock in stocks:
    ohlc[stock][["mcd", "signal"]] = MACD(ohlc[stock])
    
def a(DF, n=14):
    df = DF.copy()
    df["first"] = df["High"] - df["Low"]
   
    df["second"] = (df["High"] - df["Adj Close"].shift(1)).abs()
   
    df["third"] = (df["Low"] - df["Adj Close"].shift(1)).abs()
  
    
    df["True Range"] = df.loc[:, ["first","second","third"]].max(axis =1, skipna =False)
    df["ATR"] = df["True Range"].ewm(com = n, min_periods = n).mean()
    return df["ATR"]

for stock in stocks:
    ohlc[stock]["ATR"] = a(ohlc[stock])
