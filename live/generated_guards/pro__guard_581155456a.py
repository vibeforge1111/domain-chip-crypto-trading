def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD histogram shows momentum deceleration."""
    macd = features.get('macd_histogram', 0)
    threshold = 0.0001
    
    if prediction == 'long' and macd < threshold:
        return 'skip'
    if prediction == 'short' and macd > -threshold:
        return 'skip'
    return prediction