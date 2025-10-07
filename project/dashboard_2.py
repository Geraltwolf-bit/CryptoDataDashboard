import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import logging
from sqlalchemy import create_engine
from datetime import datetime, timedelta

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

st.set_page_config(page_title='Crypto Dashboard', page_icon ='📊', layout = 'wide')

#connect to database
@st.cache_resource
def get_database_connection():
    databese_url = 'postgresql://admin:admin@localhost:5432/mydb'
    return create_engine(databese_url)

def load_data():
    """Load data from PostgreSQL database"""
    try:
        engine = get_database_connection()
        query = 'SELECT * FROM dashboard_data ORDER BY date ASC'
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Failed to load data. Please, try again.")
        logger.error("Error loading data: {e}")
        return pd.DataFrame()

def create_gauge_chart(value, title):
    """Create a speedometer gauge chart for Fear & Greed Index"""
    fig = go.Figure(go.Indicator(
        mode = 'gauge+number',
        value = value,
        title = {'text': title},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': 'darkblue'},
            'bar': {'color': 'darkblue'},
            'bgcolor': 'white',
            'borderwidth': 2,
            'bordercolor': 'gray',
            'steps': [
                {'range': [0, 25], 'color': 'red'},
                {'range': [25, 50], 'color': 'orange'},
                {'range': [50, 75], 'color': 'yellow'},
                {'range': [75, 100], 'color': 'green'}],
                'threshold': {
                    'line': {'color': 'red', 'width': 4},
                    'thickness': 0.75,
                    'value': value
                }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=50, r=50, t=50, b=50))
    return fig

def get_fear_greed_interpretation(value, sentiment):
    """Get interpretation text for Fear&Greed Index"""
    interpretations={
        'Extreme Fear': 'People are selling crypto due to fear!',
        'Fear': 'People are hesitant to buy crypto.',
        'Neutral': 'Market is balanced',
        'Greed': 'People are buying crypto out of fear to miss out.'
        'Extreme Greed': 'People buy crypto at any price!'
    }