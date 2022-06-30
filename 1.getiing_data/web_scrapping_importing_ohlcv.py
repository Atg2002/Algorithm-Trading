# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 08:07:35 2022

@author: Krithikavvgreat
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup

tickers = ["AAPL","FB","CSCO","INFY.NS","3988.HK"]

ohlc_intraday = {}

header = {"User-Agent" : "Chrome/96.0.4664.110"}

for ticker in tickers:
    url = "https://finance.yahoo.com/quote/{}/history?p={}".format(ticker, ticker)
    page = requests.get(url, headers =header)
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser")
    table = soup.find_all("div", {"class":"Pb(10px) Ovx(a) W(100%)"})
    rows = table[0].find_all("tr", {"class": "BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"})
    datas = [row.get_text(separator = "|").split("|") for row in rows]
    ohlc_intraday[ticker]  = pd.DataFrame( data = datas, columns = ["Date","Open","High","Low","Close","Adj Close","Volume"])
    ohlc_intraday[ticker].dropna(how = "any", inplace = True)
    ohlc_intraday[ticker]["Volume"] = ohlc_intraday[ticker]["Volume"].str.replace(",", "")
    ohlc_intraday[ticker].set_index("Date", inplace = True)
    ohlc_intraday[ticker].applymap(lambda x:float(x.rstrip('%'))/100)