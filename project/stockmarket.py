#!/usr/bin/env python
# coding: utf-8

# In[1]:


import yfinance as yf
import pandas as pd
import logging

from typing import Union

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_stockmarket(ticker_name: str="^GSPC", period: str="1mo") -> Union[pd.DataFrame, None]:
    """
    Fetches stock market value for the last month.
    Parameters:
    - ticker_name (str): symbol for stockmarket value, specified by the yfinance library.
    - period (str): period for which to fetch data. Default is 1 month.
    Returns:
    - pd.DataFrame | None
    """
    try:
        data = yf.Ticker(ticker_name).history(period = period)
        if data.empty:
            logger.info("No stock market data found for the ticker: %s", ticker_name)
            return None
        return data
    except Exception as e:
        logger.error(f"Error getting stock market data: %s", e)
        return None


# In[2]:


raw_sm = get_stockmarket()
raw_sm


# In[ ]:


import pandas as pd
from datetime import datetime

def preprocess_stockmarket(stockmarket_data: pd.DataFrame) -> Union[pd.DataFrame, None]:
    """
    Converts the raw stockmarket pd.DataFrame into a pd.DataFrame that contains:
    - current data;
    - trend estimator showing if stock market is "Rising" or "Falling".
    Parameters:
    - stockmarket_data (dataframe).
    Returns:
    - pd.DataFrame | None
    """
    try:
        df = stockmarket_data.reset_index()[['Close']].copy()
        df = df.rename(columns={'Close': 'stockmarket_value'})
        start_month = stockmarket_data.iloc[-1, 1]
        end_month = stockmarket_data.iloc[0, 1]
        if start_month > end_month:
            estimate = "Rising"
        elif start_month == end_month:
            estimate = "Stable"
        else:
            estimate = "Falling"
        date = datetime.now().date()
        stockmarket = pd.DataFrame({'date': [date], 'stockmarket': [estimate]})
        return stockmarket
    except Exception as e:
        logger.info("Error preprocessing stock market data: %s", e)
        return None


# In[14]:


stockmarket = preprocess_stockmarket(raw_sm)
stockmarket

