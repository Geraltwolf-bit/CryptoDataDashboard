def get_recommendation(index_sentiment, inflation_level, stockmarket_trend):
    """
    Determine Buy/Don't buy recommendation based on inticators combination.
    """
    #define the decision rules
    if (index_sentiment == 'Fear' and inflation_level == 'Moderate' and stockmarket_trend == 'Rising'):
        return "Buy!"
    elif (index_sentiment == 'Fear' and inflation_level == 'Low' and stockmarket_trend == 'Rising'):
        return "Buy!"
    elif (index_sentiment == 'Greed' and inflation_level == 'Moderate' and stockmarket_trend == 'Rising'):
        return "Buy!"
    elif (index_sentiment == 'Greed' and inflation_level == 'High' and stockmarket_trend == 'Falling'):
        return "Don't buy!"
    else:
        return "Don't buy!"