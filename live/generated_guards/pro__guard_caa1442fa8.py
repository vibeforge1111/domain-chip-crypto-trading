def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD histogram shows momentum deceleration."""
    macd = features.get('macd_histogram', 0)
    
    # For longs: skip if histogram is negative (upward momentum weakening)
    if prediction == 'long' and macd < 0:
        return 'skip'
    
    # For shorts: skip if histogram is positive (downward momentum weakening)
    if prediction == 'short' and macd > 0:
        return 'skip'
    
    return prediction