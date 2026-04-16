def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram indicates momentum deceleration."""
    macd_hist = features.get('macd_histogram', 0)
    
    # For long trades, require positive MACD histogram (bullish momentum)
    if prediction == 'long' and macd_hist <= 0:
        return 'skip'
    
    # For short trades, require negative MACD histogram (bearish momentum)
    if prediction == 'short' and macd_hist >= 0:
        return 'skip'
    
    return prediction