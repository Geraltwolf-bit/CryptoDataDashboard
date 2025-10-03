#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
def get_stockmarket():
    try:
        data = yf.Ticker("^GSPC").history(period = '1mo')
        print(f"data is type: {type(data)}")
        return data
    except Exception as e:
        print(f"Error getting stock market data: {e}")
        return None


# In[2]:


raw_sm = get_stockmarket()
raw_sm


# In[3]:


import pandas as pd
from datetime import datetime

def figure_stockmarket(data):
    if data.empty:
        print("No stock market data to clean")
        return None
    try:
        estimate = 0
        df = data.reset_index()[['Date', 'Close']].copy()
        df = df.rename(columns={'Date': 'date', 'Close': 'stockmarket_value'})
        df['date'] = df['date'].dt.date
        estimate = "Rising" if data.iloc[-1, 1] > data.iloc[0, 1] else "Falling"
        date = datetime.now().date()
        stockmarket = pd.DataFrame({'date': [date], 'stockmarket': [estimate]})
        print(f"data is type: {type(stockmarket)}")
        return stockmarket
    except Exception as e:
        print(f"Error cleaning stock market data: {e}")
        return None


# In[4]:


stockmarket = figure_stockmarket(raw_sm)
stockmarket

