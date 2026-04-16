def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    macd_hist = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    
    if prediction == 'long' and (macd_hist < -0.0002 or stoch_k > 85):
        return "skip"
    if prediction == 'short' and (macd_hist > 0.0002 or stoch_k < 15):
        return "skip"
    return prediction