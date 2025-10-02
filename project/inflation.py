#!/usr/bin/env python
# coding: utf-8

# In[37]:


import os
import requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def get_cpi():
    key = os.getenv('api_key')
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id=CPIAUCSL&api_key={key}&file_type=json&sort_order=desc"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        raw = response.json()
        raw = raw['observations']
        df = pd.DataFrame(raw)
        data = df.reset_index()[['date', 'value']].copy()
        data = data.iloc[0:2]
        data['value'] = pd.to_numeric(data['value'], errors = 'coerce')
        data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
        return data
    except Exception as e:
        print(f"Error getting Consumer Price Index: {e}")
        return None


# In[38]:


cpi = get_cpi()
cpi


# In[39]:


def figure_inflation(data):
    if data.empty:
        print("No inflation data")
        return None
    try:
        first_value = float(round(data['value'].iloc[0], 2))
        last_value = float(round(data['value'].iloc[1], 2))
        monthly_inflation_rate = ((first_value / last_value) - 1) * 100
        monthly_inflation_rate = float(round(monthly_inflation_rate, 2))
        annualized_inflation = ((1 + monthly_inflation_rate / 100) ** 12 - 1) * 100
        annualized_inflation = float(round(annualized_inflation, 2))
        if annualized_inflation <= 2:
            return "Low"
        elif annualized_inflation <= 5:
            return "Moderate"
        elif annualized_inflation > 5:
            return "High"
    except Exception as e:
        print(f"Error figuring inflation: {e}")
        return None


# In[40]:


from datetime import datetime
inflation_estimate = figure_inflation(cpi)
date = datetime.now().date()
inflation = pd.DataFrame({'date': [date], 'inflation': [inflation_estimate]})
inflation

