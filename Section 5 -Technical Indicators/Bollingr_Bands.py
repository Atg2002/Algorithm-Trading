# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 20:40:50 2022

@author: Krithikavvgreat
"""

import yfinance as yf

stocks = ["RELIANCE.NS", "INFY.NS", "SBICARD.NS", "HDFCBANK.NS", "ITC.NS"]

ohlc = {}

for stock in stocks:
       temp = yf.download(stock, period = "1mo", interval = "15m")
       temp.dropna(how = "any", inplace =True)
       ohlc[stock] = temp

def BB(DF, n=14):
    df = DF.copy()
    df["Middle Band"] = df["Adj Close"].rolling(n).mean()
    df["UB"] = df["Middle Band"] + 2*df["Adj Close"].rolling(n).std(ddof = 0)
    df["LB"] = df["Middle Band"] - 2*df["Adj Close"].rolling(n).std(ddof = 0)
    df["BB_width"] = df["UB"] - df["LB"]
    return df[["Middle Band", "UB", "LB", "BB_width"]]

for stock in stocks:
    ohlc[stock][["Middle Band", "UB", "LB", "BB_width"]] = BB(ohlc[stock], 20)