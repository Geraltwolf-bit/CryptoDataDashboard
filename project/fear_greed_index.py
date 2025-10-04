#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import pandas as pd
import logging
from datetime import datetime
from typing import Union
from constants import FEAR_GREED_INDEX_URL

logging.basicConfig(level=logging.ERROR)
logger  = logging.getLogger(__name__)

def get_index(
        url: str,
        timeout: int = 10,
        limit: int = 10,
        format: str = "json"
) -> Union[dict, None]:
    """
    Fetches the Fear and Greed Index from the specified URL.
    Parameters:
    - url (str): The API endpoint URL with placeholders for limit and format.
    - timeout (int): the timeout of the http request in seconds.
    - limit (int): the number of data points to fetch.
    - format (str): the response format, 'json'.
    Returns:
    - dict or None
    """
    url = url.format(limit = limit, format = format)
    try:
        response = requests.get(url, timeout=timeout)
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Error getting fear & greed data: %s", e)
        return None


# In[3]:


index_data = get_index(FEAR_GREED_INDEX_URL, limit = 1)
index_data


# In[ ]:


from datetime import datetime

def preprocess_index(index_data: dict) -> Union[pd.DataFrame, None]:
    """
    Converts Fear and Greed Index dict into a pd.DataFrame.
    Parameters:
    - index_data (dict).
    Returns:
    - pd.DataFrame | None if input is invalid.
    """
    try:
        data_list = index_data['data']
        df = pd.DataFrame(data_list)
        df = df.drop(columns=['time_until_update', 'timestamp'])
        df = df.rename(columns = {'value': 'value', 'value_classification': 'index'})
        df['date'] = datetime.now().date()
        df = df[['date', 'index', 'value']]
        return df
    except Exception as e:
        logger.info("Error preprocessing fear&greed data: %s", e)
        return None


# In[5]:


index = preprocess_index(index_data)
index

