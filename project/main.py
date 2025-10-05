import pandas as pd
import logging

from sqlalchemy import create_engine

from fear_greed_index import get_index, preprocess_index
from inflation import get_inflation, preprocess_inflation
from stockmarket import get_stockmarket, preprocess_stockmarket
from constants import FEAR_GREED_INDEX_URL, cpi_url, api_key_cpi

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def get_df():
    """
    Collects fear&greed index, inflation, stockmarket and provides combined dataframe.
    """
    try:
        ind = get_index(FEAR_GREED_INDEX_URL, limit=1)
        index = preprocess_index(ind)
        inf = get_inflation(cpi_url, key = api_key_cpi)
        inflation = preprocess_inflation(inf)
        sm = get_stockmarket()
        stockmarket = preprocess_stockmarket(sm)
        df = pd.merge(index, inflation, on = 'date')
        df = pd.merge(df, stockmarket, on = 'date')
        return df
    except Exception as e:
        logger.error("Error %s", e)
        return None
    
def save_to_database(df: pd.DataFrame):
    """
    Saves pd.DataFrame to PostgreSQL database
    """
    try:
        #connect database
        database_url = 'postgresql://admin:admin@localhost:5432/mydb'
        engine = create_engine(database_url)

        #check if the data for the current date already exists in the base:
        existing_date_query = "SELECT date from dashboard_data WHERE date = %s"
        existing_date = pd.read_sql(existing_date_query, engine, params=(df['date'].iloc[-1],))
        
        #if data for the current date is absent, insert the data
        if existing_date.empty:
            df.to_sql(
                'dashboard_data',
                engine,
                if_exists='append',
                index = False
            )
            logger.info(f"Data saved for {df['date'].iloc[0]}")
        
        #if data for the current data is present, show it
        else:
            logger.info(f"Data for {df['date'].iloc[0]} already exists.")

    except Exception as e:
        logger.error("Error saving Dataframe to database: %s", e)
        return None

if __name__== "__main__":
    df = get_df()
    if df is not None:
        save_to_database(df)