#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
def get_stockmarket():
    try:
        data = yf.Ticker("^GSPC").history(period = '1mo')
        return data
    except Exception as e:
        print(f"Error getting stock market data: {e}")
        return None


# In[2]:


raw_sm = get_stockmarket()
raw_sm


# In[6]:


import pandas as pd
from datetime import datetime

def clean_stockmarket(data):
    if data.empty:
        print("No stock market data to clean")
        return None
    try:
        df = data.reset_index()[['Date', 'Close']].copy()
        df = df.rename(columns={'Date': 'date', 'Close': 'stockmarket_value'})
        df['date'] = df['date'].dt.date
        return df
    except Exception as e:
        print(f"Error cleaning stock market data: {e}")
        return None


# In[8]:


stockmarket_data = clean_stockmarket(raw_sm)
stockmarket_data


# In[24]:


def figure_stockmarket(data):
    if data.empty:
        print("Error estimating stock market trend")
        return None
    try:
        return "Rising" if data.iloc[-1, 1] > data.iloc[0, 1] else "Falling"
    except Exception as e:
        print(f"Error estimating stock market trend: {e}")


# In[33]:


from datetime import datetime
stockmarket_estimate = figure_stockmarket(stockmarket_data)
date = datetime.now().date()
stockmarket = pd.DataFrame({'date': [date], 'stockmarket': [stockmarket_estimate]})
stockmarket

