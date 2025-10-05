import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from datetime import datetime, timedelta

#configurate page
st.set_page_config(page_title='Crypto Dashboard', page_icon = '📊', layout='wide')

#connect database
@st.cache_resource
def get_database_connection():
    database_url = 'postgresql://admin:admin@localhost:5432/mydb'
    return create_engine(database_url)

def load_data():
    """ Load data from PostgreSQL database """
    try:
        engine = get_database_connection()
        query = "SELECT * FROM dashboard_data ORDER BY date DESC"
        df = pd.read_sql(query, engine)
        st.write(df)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()