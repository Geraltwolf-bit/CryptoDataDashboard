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

def get_analysis_result(fg_sentiment, inflation, stockmarket):
    """Get analysis result based on the combiantion of indicators"""
    rules = {
        #Extreme Fear cases
        ("Extreme Fear", 'Low', 'Rising'): {
            "definite_answer": "Yes!",
            "recommendation": "Buy now!",
            "explanation_part_i": "Indicators show that economy is stable. Crypto crash is caused by social media hype.",
            "fg_justified": "Not justified"
        },
        ("Extreme Fear", 'High', 'Falling'): {
            "definite_answer": "No!",
            "recommendation": "Don't buy!",
            "explanation_part_i": "Indicators show that economy is tanking. Crypto price may never recover.",
            "fg_justified": "Justified"    
        },
        #Fear cases
        ('Fear', 'Low', 'Rising'): {
            "definite_answer": "Yes!",
            "recommendation": "Buy now!",
            "explanation_part_i": "Indicators show that economy is stable. Crypto prices will rise.",
            "fg_justified": "Not justified"    
        },
        ("Fear", 'High', 'Falling'): {
            "definite_answer": "No!",
            "recommendation": "Don't buy!",
            "explanation_part_i": "Indicators show that economy is weak. Crypto price will stay weak too.",
            "fg_justified": "Justified"
        },
        #Neutral case
        ('Neutral', 'Low', 'Rising'): {
            "definite_answer": "Yes!",
            "recommendation": "It's safe to buy!",
            "explanation_part_i": "Indicators show that economy is balanced. Crypto price will rise.",
            "fg_justified": "Justified"    
        },
        #Greed cases
        ('Greed', 'Low', 'Rising'): {
            "definite_answer": "Yes!",
            "recommendation": "It's safe to buy!",
            "explanation_part_i": "Indicators show that economy is strong. Crypto price will continue to rise.",
            "fg_justified": "Justified"
        },
        ('Greed', 'High', 'Falling'): {
            "definite_answer": "No!",
            "recommendation": "Don't buy!",
            "explanation_part_i": "Indicators show that economy is struggling. Crypto price is overvalued. Better sell!",
            "fg_justified": "Not justified"
        },
        #Extreme Greed cases
        ('Extreme Greed', 'Low', 'Rising'): {
            "definite_answer": "Yes!",
            "recommendation": "It's safe to buy!",
            "explanation_part_i": "Indicators show that economy is on the rise. What seems to be historic top, soon will be normal price!",
            "fg_justified": "Justified"
        },
        ('Extreme Greed', 'High', 'Falling'): {
            "definite_answer": "No!",
            "recommendation": "Don't buy!",
            "explanation_part_i": "Indicators show that economy is in trouble. Crypto is a bubblel now. Time to sell!",
            "fg_justified": "Not justified"
        }
    }
    #Return the matching rule or a default
    return rules.get((fg_sentiment, inflation, stockmarket), "")

def create_historical_charts(df, column, title):
    """Create historical line charts"""
    if column in df.columns and 'date' in  df.columns:
        fig = px.line(df, x = 'date', y = column, title=title)
        fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
        return fig
    return None

def main():
    """Run the program"""
    st.title('Crypto Dashboard')
    df = load_data()
    if df.empty:
        st.warning("No data found in the database.")
        return
    
    #get latest data
    latest = df.iloc[-1]
    current_date = latest['date'].strftime('%B, %d')

    #Extract values
    fg_value = latest.get('value', 50)
    fg_sentiment = latest.get('index', get_fear_greed_sentiment(fg_value))
    inflation = latest.get('inflation', 'Low')
    stockmarket = latest.get('stockmarket', 'Rising')

    #Part I of the dashboard
    if not st.session_state.get('show_analysis', False):
        st.markdown("---")

        #Current date at top center
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"<h1 style='text-align: center;'>Today | {current_date}</h1>", unsafe_allow_html=True)
        st.markdown("---")

        #Fear&Greed Index gauge
        st.subheader("Fear & Greed Index")
        gauge_fig=create_gauge_chart(fg_value, 'Current Market Sentiment')
        st.plotly_chart(gauge_fig, use_container_width=True)

        #Explain text
        explanation_i = get_explanation_part_i(fg_sentiment)
        st.markdown(f"{fg_sentiment} means {explanation_i}")

        st.markdown('---')
        st.subheader("Should you?")

        #Pulsating button
        if st.button("Click here to find out",
                     type = 'primary',
                     use_container_width=True,
                     key = "reveal_analysis"):
            st.session_state.show_analysis = True
            st.rerun()
    
    #Part II of the dashboard
    else:
        #get analysis
        analysis = get_analysis_result(fg_sentiment, inflation, stockmarket)
        st.markdown('---')
        
        #Today's date at top center
        col1, col2, col3=st.columns([1, 2, 1])
        with col2:
            st.markdown(f"<h1 style='text-align: center;'>Today | {current_date}<h1>", unsafe_allow_html=True)

            #Define answer with emphasis
            st.markdown(f"<h2 style=\"text-align: center; color: {'green' if analysis['definite_answer']=='Yes!' else 'red'};\">{analysis['definite_answer']}</h2>", unsafe_allow_html=True)

            #Recommendation
            st.markdown(f"<h3 style='text-align: center;'>{analysis['recommendation']},/h3", unsafe_allow_html=True)

            #Explanation
            st.info(analysis['explanation_part_ii'])

            #Metrics and graph section
            col1, col2 = st.columns([1, 2])

            with col1:
                st.subheader('Market Indicators')

                #Fear & Greed Index
                st.metric(
                    "Fear & Greed Index",
                    f"{fg_value}",
                    f"{analysis['fg_justified']}"
                )

                #Inflation
                st.metric("Inflation", f"{latest.get('inflatioin_value', 'N/A')}" if 'inflation_value' in latest else inflation, inflation)

                #Stockmarket
                st.metric(
                    "Stockmarket",
                    f"{latest.get('stockmarket_value', 'N/A')}" if 'stockmarket_value' in latest else "See trend",
                    stockmarket
                )
            with col2:
                st.subheader('Historical Trends')
                df_2025 = df[df['date'] >= '2025-01-01']

                if not df_2025.empty:
                    #Fear & Greed chart
                    fg_chart = create_historical_charts(df_2025, 'value', 'Fear & Greed Index Trend')
                    if fg_chart:
                        st.plotly_chart(fg_chart, use_container_width=True)
                    
                    #Inflation chart
                    if 'inflation_value' in df_2025.columns:
                        inflation_chart=create_historical_charts(df_2025, 'inflation_value', 'Inflation_trend')
                        if inflation_chart:
                            st.plotly_chart(inflation_chart, use_container_width=True)
                    
                    #Stockmarket chart
                    if 'stockmarket_value' in df_2025.columns:
                        stock_chart = create_historical_charts(df_2025, 'stockmarket_value', 'Stock Market Trend')
                        if stock_chart:
                            st.plotly_chart(stock_chart, use_container_width=True)
            
            #Histotical scroller
            st.subheader("Historical Analysis")
            available_dates = sorted(df['date'].unique(), reverse=True)
            selected_date = st.selectbox("Select a date", available_dates)
            if selected_date:
                selected_data = df[df['date'] == selected_date].iloc[0]
                selected_fg_value = selected_data.get('value', 50)
                selected_sentiment = selected_data.get('index', get_fear_greed_sentiment(selected_fg_value))
                selected_inflation = selected_data.get('inflation', 'Low')
                selected_stockmarket = selected_data.get('stockmarket', 'Rising')
                selected_analysis = get_analysis_result(selected_sentiment, selected_inflation, selected_stockmarket)
                st.write(f"Analysis for {selected_date.strftime("%B, %d")}")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Fear & Greed", f"{selected_fg_value} - {selected_sentiment}")
                    st.metric("Inflation", selected_inflation)
                    st.metric("Stock Market", selected_stockmarket)

                with col2:
                    if selected_analysis['definite_answer']=='Yes!':
                        st.success(f"{selected_analysis['definite_answer']} {selected_analysis['recommendation']}")
                    else:
                        st.error(f"{selected_analysis['definite_answer']} {selected_analysis['recommendation']}")
                    st.write(selected_analysis['explanation_part_ii'])

if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False

if __name__=='__main__':
    main()