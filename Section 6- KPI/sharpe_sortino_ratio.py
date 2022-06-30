# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 09:03:44 2022

@author: Krithikavvgreat
"""

import yfinance as yf
import numpy as np

ohlc = {}
stocks = ["RELIANCE.NS", "INFY.NS", "SBICARD.NS", "HDFCBANK.NS", "ITC.NS"]

for stock in stocks:
    temp = yf.download(stock, period="7mo", interval="1d")
    temp.dropna(axis = 0,how = "any", inplace=True)
    ohlc[stock] = temp
    
def CAGR(DF):
    df = DF.copy()
    df["pct_change"] = df["Adj Close"].pct_change()
    df["Cumulative Return"] = (df["pct_change"]+1).cumprod()
    n = len(df)/252
    return (df["Cumulative Return"][-1])**(1/n)  -1

def Volatility(DF):
    df = DF.copy()
    df["Daily Return"] = df["Adj Close"].pct_change()
    volatilty = df["Daily Return"].std() * np.sqrt(252)
    return volatilty

def Sharpe(DF):
    df = DF.copy()
    ratio = (CAGR(df) - 0.0667)/Volatility(df)
    return ratio

def Sortino(DF):
    df = DF.copy()
    df["Return"] = df["Adj Close"].pct_change()
    neg_return = np.where(df["Return"]>0, 0, df["Return"])
    lst = []
    for val in neg_return:
        if val<0:
            lst.append(val)
    array = np.array(lst)
    volatilty = array.std() *np.sqrt(252)
    
    return (CAGR(df) -0.0667)/volatilty
    
for stock in ohlc:
    print("Sharpe Ratio for {} is {}".format(stock, Sharpe(ohlc[stock])))
    print("Sortino Ratio for {} is {}".format(stock, Sortino(ohlc[stock])))
    
import yfinance as yf
import pandas as pd
import numpy as np

# Download historical data for required stocks
tickers = ["RELIANCE.NS", "INFY.NS", "SBICARD.NS", "HDFCBANK.NS", "ITC.NS"]
ohlcv_data = {}

# looping over tickers and storing OHLCV dataframe in dictionary
for ticker in tickers:
    temp = yf.download(ticker,period='7mo',interval='1d')
    temp.dropna(how="any",inplace=True)
    ohlcv_data[ticker] = temp
    
def CAGR(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["return"] = DF["Adj Close"].pct_change()
    df["cum_return"] = (1 + df["return"]).cumprod()
    n = len(df)/252
    CAGR = (df["cum_return"][-1])**(1/n) - 1
    return CAGR
    
def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    vol = df["return"].std() * np.sqrt(252)
    return vol

def sharpe(DF, rf):
    "function to calculate Sharpe Ratio of a trading strategy"
    df = DF.copy()
    return (CAGR(df) - rf)/volatility(df)

def sortino(DF, rf):
    "function to calculate Sortino Ratio of a trading strategy"
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    neg_return1 = np.where(df["return"]>0,0,df["return"])
    neg_vol = pd.Series(neg_return1[neg_return1!=0]).std() * np.sqrt(252)
    return (CAGR(df) - rf)/neg_vol

for ticker in ohlcv_data:
    print("Sharpe of {} = {}".format(ticker,sharpe(ohlcv_data[ticker],0.0667)))
    print("Sortino of {} = {}".format(ticker,sortino(ohlcv_data[ticker],0.0667)))
    
    
    