# -*- coding: utf-8 -*-
"""
Created on Wed May 25 19:58:27 2022

@author: Krithikavvgreat
"""

import yfinance as yf
import numpy as np

stocks = ["AMZN", "GOOG", "MSFT", "AAPL"]
ohlcv = {}
for stock in stocks:
    temp = yf.download(stock, period = "1mo", interval = "5m")
    temp.dropna(how = "any", inplace = True)
    ohlcv[stock] = temp

def ATR(DF, n =14):
    df = DF.copy()
    df["lvl1"] = df["High"] - df["Adj Close"]
    df["lvl2"] = df["Low"] - df["Adj Close"]
    df["lvl3"] = df["Adj Close"] - df["Adj Close"].shift(1)
    df["TR"] = df[["lvl1","lvl2","lvl3"]].max(axis = 1, skipna = False)
    df["ATR"] = df["TR"].ewm(com =n, min_periods= n).mean()
    return df["ATR"]

def ADX(DF, n = 14):
    df = DF.copy()
    df["diff_high"] = df["High"] - df["High"].shift(1) 
    df["diff_low"]  = df["Low"].shift(1) -df["Low"]
    df["DM+"] = np.where( (df["diff_high"]>df["diff_low"]) & (df["diff_high"]>0), df["diff_high"], 0)
    df["DM-"] = np.where( (df["diff_high"]<df["diff_low"]) & (df["diff_low"]>0),  df["diff_low"], 0)
    df["ATR"] = ATR(df, n)
    df["+DI"] = (df["DM+"]/df["ATR"]).ewm(alpha = 1/n, min_periods = n).mean()*100
    df["-DI"] = (df["DM-"]/df["ATR"]).ewm(alpha = 1/n, min_periods = n).mean()*100
    df["DX"] = abs(df["+DI"] - df["-DI"])/(df["+DI"] + df["-DI"])
    df["ADX"] = 100*df["DX"].ewm(alpha = 1/n, min_periods =n).mean()
    return df["ADX"]

for stock in stocks:
    ohlcv[stock]["ADX"] = ADX(ohlcv[stock],20) 
    