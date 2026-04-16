def guard(features: dict, prediction: str) -> str:
    """Skip trades when momentum is against the trade direction."""
    macd = features.get('macd_histogram', 0)
    
    # Reject longs when macd_histogram is negative (bearish momentum)
    if prediction == 'long' and macd < -0.0003:
        return 'skip'
    
    # Reject shorts when macd_histogram is positive (bullish momentum)
    if prediction == 'short' and macd > 0.0003:
        return 'skip'
    
    return prediction