# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import yfinance as yf
import statsmodels.api as sm
import numpy as np
import datetime as dt

ticker = "AAPL"
start = dt.date.today() - dt.timedelta(365)
end = dt.date.today() 
ohlcv = yf.download(ticker, start = start, end = end, interval = "1d")

def slope(ser, n):
    slopes = [0 for i in range(n-1)]
    for i in range(n, len(ser)+1):
        y = ser[i-n:i]
        x = np.array(range(n))
        y_scaled = (y - y.min())/(y.max() - y.min())
        x_scaled = (x - x.min())/(x.max() - x.min())
        x_scaled = sm.add_constant(x_scaled)
        model = sm.OLS(y_scaled, x_scaled)
        result = model.fit()
        slopes.append(result.params[-1])
    return slopes

ohlcv["slope"] = slope(ohlcv["Adj Close"], 5)

ohlcv[["slope", "Adj Close"]].plot(subplot = True, layout = (2,1))