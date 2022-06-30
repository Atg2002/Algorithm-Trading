import yfinance as yf


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

def Max_Drawdown(DF):
    df = DF.copy()
    max = df["Adj Close"].max()
    index = df["Adj Close"][df["Adj Close"] ==max].index(0)
    min = df["Adj Close"].loc[index:].min()
    return (max-min)

def Calmer_Ratio(DF):
    return CAGR(DF)/Max_Drawdown(DF)

for stock in ohlc:
    print("Calmer Ratio for {} is {}".format(stock,Calmer_Ratio(ohlc[stock])))


