def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum contradicts direction."""
    macd = features.get('macd_histogram', 0)
    
    # Skip longs when macd histogram is negative (bearish momentum)
    if prediction == 'long' and macd < -0.0003:
        return 'skip'
    
    # Skip shorts when macd histogram is positive (bullish momentum)
    if prediction == 'short' and macd > 0.0003:
        return 'skip'
    
    return prediction