def guard(features: dict, prediction: str) -> str:
    """Filter trades based on MACD momentum confirmation."""
    macd_hist = features.get('macd_histogram', 0)
    
    # Longs require positive MACD histogram (bullish momentum)
    if prediction == "long" and macd_hist <= 0:
        return "skip"
    
    # Shorts require negative MACD histogram (bearish momentum)
    if prediction == "short" and macd_hist >= 0:
        return "skip"
    
    return prediction