#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd
def get_index():
    url = f"https://api.alternative.me/fng/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error getting fear&greed data: {e}")
        return None


# In[2]:


index_data = get_index()
index_data


# In[11]:


from datetime import datetime

def clean_index(data):
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
        return df
    except Exception as e:
        print(f"Error cleaning fear&greed data: {e}")
        return None


# In[12]:


index = clean_index(index_data)
index

