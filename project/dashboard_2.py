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
    #Determine bar color based on value
    if value <= 25:
        color = 'red'
    elif value <= 45:
        color = 'orange'
    elif value <= 55:
        color = 'yellow'
    elif value <= 75:
        color = 'lightgreen'
    else:
        color = 'green'

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

def get_fear_greed_sentiment(value):
    """Convert numeric value """
    if value <= 25:
        return "Extreme Fear"
    elif value <= 45:
        return 'Fear'
    elif value <= 55:
        return "Neutral"
    elif value <= 74:
        return 'Greed'
    else:
        return 'Extreme Greed'
    
def get_explanation_part_i(sentiment):
    """Get Part I explanation based on sentiment"""
    explanations = {
        "Extreme Fear": "crypto market crashed. Most people sell in panic; others buy hoping for profit.",
        'Fear': 'crypto market is down. Most people sell at a loss.',
        'Neutral': 'crypto market is balanced. People buy crypto.',
        "Greed": "crypto market is excited. Everybody buys.",
        "Extreme Greed": "crypto market is in frenzy! Everybody buys disregarding the price."
        }
    return explanations.get(sentiment, "")


    
definite_answer = ['Yes!', 'No!']
recommendation = ["Buy now!", "Don’t buy!", "It’s safe to buy!", "Sell now!"]
explanation_part_ii = [
	"Indicators show that economy is stable – crypto crash is caused by social media hype.",
	"Indicators show that economy is tanking. Crypto price may never recover.",
	"Indicators show that economy is stable. Crypto price will rise further.",
	"Indicators show that economy is weak. Crypto price will stay weak too.",
	"Indicators show that economy is balanced. Crypto price will rise.",
	"Indicators show that economy is strong. Crypto price will continue to rise.",
	"Indicators show that economy is struggling. Crypto price is overvalued. Better sell!",
	"Indicators show that economy is on the rise. What seems to be historic top, soon will be normal price.",
	"Indicators show that economy is in trouble. Crypto is bubble now. Time to sell!"
]


