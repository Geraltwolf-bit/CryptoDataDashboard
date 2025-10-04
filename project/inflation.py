#!/usr/bin/env python
# coding: utf-8

# In[27]:


import requests
import pandas as pd
import logging
from typing import Union
from constants import cpi_url, api_key_cpi

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def get_inflation(
        url: str,
        key: str,
        limit: int = 2,
        format: str = "json",
        timeout: int = 10
) -> Union[dict, None]:
    """
    Fetches the CPI index for the last two months; used to calculate inflation.
    Parameters:
    - url (str): The API endpoint with placeholders for key, format, and limit.
    - key (str): API key provided by World Bank.
    - limit (int): The number months for which to receive CPI indexes.
    - format (str): The response format: "json", "csv", "xml", or "xlsx".
    - timeout (int): The timeout for HTTP request in seconds.
    Returns:
    - dict or None.
    """

    url = url.format(key = key, limit = limit, format = format, timeout = timeout)
    try:
        response = requests.get(url, timeout=10)        
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Error getting fear & greed data: %s", e)
        return None


# In[28]:


cpi = get_inflation(cpi_url, key = api_key_cpi)
cpi


# In[39]:


from datetime import datetime

def preprocess_inflation(cpi_data: dict) -> Union[pd.DataFrame, None]:
    """
    Converts dict with cpi indexes into dataframe showing inflation estimate: "High", "Moderate", "Low".
    Parameters: 
    - cpi indexes (dict).
    Returns:
    - pd.DataFrame containing inflation trend for the current date.
    """

    try:
        #enter the dict and extract only the value under the key "observations"
        raw = cpi_data['observations']
        #transform into dataframe
        df = pd.DataFrame(raw)
        #reset index and drop all the columns except "date" and "value"
        data = df.reset_index()[['date', 'value']].copy()
        #transform string "value" to numerical value
        data['value'] = pd.to_numeric(data['value'], errors = 'coerce')
        #transform "date" to proper date format
        data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
        #sort by "date" in descending order
        data.sort_values(by = 'date', ascending=False)
        #extract the cpi value for the recent month
        first_value = float(round(data['value'].iloc[0], 2))
        #extract the cpi value for the previous month
        last_value = float(round(data['value'].iloc[1], 2))
        #calculate monthly inflation
        monthly_inflation_rate = ((first_value / last_value) - 1) * 100
        #based on the monthly inflation, assume what annual inflation would be
        annualized_inflation = ((1 + monthly_inflation_rate / 100) ** 12 - 1) * 100
        #compare annual inflation to Central Bank target and produce estimate
        if annualized_inflation <= 2:
            estimate = "Low"
        elif annualized_inflation <= 5:
            estimate = "Moderate"
        elif annualized_inflation > 5:
            estimate = "High"
        #get the current date
        date = datetime.now().date()
        #create a final dataframe with the current date and inflation estimate
        inflation = pd.DataFrame({'date': [date], 'inflation': [estimate]})
        return inflation
    except Exception as e:
        logger.info("Error processing data into DataFrame: %s", e)
        return None


# In[40]:


inflation = preprocess_inflation(cpi)
inflation

