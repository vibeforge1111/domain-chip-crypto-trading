def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum shows deceleration via MACD histogram."""
    macd = features.get('macd_histogram', 0)
    
    # Skip longs when bearish momentum dominates (negative histogram)
    if prediction == 'long' and macd < -0.0002:
        return 'skip'
    
    # Skip shorts when bullish momentum dominates (positive histogram)
    if prediction == 'short' and macd > 0.0002:
        return 'skip'
    
    return prediction