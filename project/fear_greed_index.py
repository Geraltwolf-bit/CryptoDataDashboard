#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
import pandas as pd
def get_index():
    url = f"https://api.alternative.me/fng/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"data is type: {type(data)}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error getting fear&greed data: {e}")
        return None


# In[5]:


index_data = get_index()
index_data


# In[6]:


from datetime import datetime

def figure_index(data):
    if not data or 'data' not in data:
        print("No data to clean")
        return None
    try:
        data_list = data['data']
        df = pd.DataFrame(data_list)
        df['timestamp'] = pd.to_numeric(df['timestamp'], errors = 'coerce')
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit = 's')
        df = df.drop(columns=['time_until_update'])
        df = df.rename(columns = {'value': 'value', 'value_classification': 'index', 'timestamp': 'date'})
        df = df[['date', 'index', 'value']]
        print(f"data is type: {type(df)}")
        return df
    except Exception as e:
        print(f"Error cleaning fear&greed data: {e}")
        return None


# In[7]:


index = figure_index(index_data)
index

