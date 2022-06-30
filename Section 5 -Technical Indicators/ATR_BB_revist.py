# -*- coding: utf-8 -*-
"""
Created on Sat May  7 11:19:50 2022

@author: Krithikavvgreat
"""

import yfinance as yf

stocks = ["MSFT","AAPL","GOOG"]
ohlcv = {}

for stock in stocks:
    temp = yf.download(stock, period = "1mo", interval = "5m")
    temp.dropna(how= "any", inplace=True)
    ohlcv[stock] = temp
    
def ATR(DF, n=14):
    df = DF.copy()
    df["comp1"] = df["High"] - df["Low"]
    df["comp2"] = (df["High"] - df["Adj Close"].shift(1)).abs()
    df["comp3"] = (df["Low"] - df["Adj Close"].shift(1)).abs()
    
    df["TR"] = df[["comp1","comp2","comp3"]].max(axis =1, skipna = False)
    df["ATR"] = df["TR"].ewm(com = n, min_periods= n).mean()#use com instead of span to get closer to yahoo finances values
    return df["ATR"]


def BB(DF, n=14 ,m=2):
    df = DF.copy()
    df["MB"] = df["Adj Close"].rolling(n).mean()
    df["LB"] = df["MB"] - m*df["Adj Close"].rolling(n).std(ddof = 0)
    df["UB"] = df["MB"] + m*df["Adj Close"].rolling(n).std(ddof = 0)
    df["BB_width"] = df["UB"] -df["LB"]
    return df[["MB","LB", "UB","BB_width"]]
    
for stock in stocks:
    ohlcv[stock]["ATR"] = ATR(ohlcv[stock])
    ohlcv[stock][["MB","LB", "UB","BB_width"]] = BB(ohlcv[stock])
    
