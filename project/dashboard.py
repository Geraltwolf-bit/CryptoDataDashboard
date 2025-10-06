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
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def main():
    st.title("Crypto Dashboard")
    df = load_data()

    if df.empty:
        st.warning("No data found in the database.")
        return
    st.subheader("Raw Data")
    st.dataframe(df)

    latest = df.iloc[0]

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        latest = df.iloc[0]
        st.metric("Latest Date", latest['date'].strftime('%Y-%m-%d'))

    with col2:
        st.metric("Fear and Greed", f"{latest.get('value', 'N/A')}")

    with col3:
        st.metric("Inflation", latest.get('inflation', 'N/A'))

    with col4:
        st.metric("Stockmarket", latest.get('stockmarket', 'N/A'))
    
    with col5:
        recommendation = latest.get('recommended_action', 'N/A')
        st.metric("Recommendation", recommendation)

    st.subheader("Trading Recommendation")
    recommendation = latest.get('recommended_action')

    if recommendation == 'Buy!':
        st.success(f"{recommendation}")
    else:
        st.error(f"{recommendation}")

    if 'value' in df.columns and 'date' in df.columns:
        st.subheader("Fear & Greed Index over time")
        fig = px.line(df, x = 'date', y = 'value', title = 'Fear & Greed index')
        st.plotly_chart(fig)

if __name__=="__main__":
    main()