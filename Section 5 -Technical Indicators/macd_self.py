# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 20:07:40 2022

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

''' 
def MACD(DF, a=12, b=24, c=9):
    df = DF.copy()
    count =0
    SMA = []
    for row in df.loc[:, "Adj Close"]:
        if count<a:
            SMA[count] = None
            count+=1
            print(count)
        
        else :
            SMA[count] = (df.loc[:count, "Adj Close"].sum(axis =1))/a
            count+=1
    
    multiplier = 2/(a+1)
    return SMA

MACD(ohlc["RELIANCE.NS"])'''



    
def MACD(DF, a=12, b=26, c=9):
    df = DF.copy()
    df["fast_emv"] =df["Adj Close"].ewm(span = a, min_periods = a).mean()
    df["slow_emv"] =df["Adj Close"].ewm(span = b, min_periods = b).mean()
    df["mcd"] = df["fast_emv"]  -df["slow_emv"]
    df["signal"]   =df["mcd"].ewm(span = c, min_periods = c).mean() 
    
    return df.loc[:, ["mcd", "signal"]]

for stock in stocks:
    ohlc[stock][["mcd", "signal"]] = MACD(ohlc[stock])

