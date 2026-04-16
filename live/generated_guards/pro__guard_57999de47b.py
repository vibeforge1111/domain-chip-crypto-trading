def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD histogram contradicts momentum direction."""
    macd_histogram = features.get('macd_histogram', 0)
    
    # For longs, histogram must be positive (bullish momentum)
    if prediction == 'long' and macd_histogram < 0:
        return 'skip'
    
    # For shorts, histogram must be negative (bearish momentum)
    if prediction == 'short' and macd_histogram > 0:
        return 'skip'
    
    return prediction