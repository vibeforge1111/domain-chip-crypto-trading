def guard(features: dict, prediction: str) -> str:
    """Filter trades based on MACD momentum alignment."""
    if prediction == "skip":
        return prediction
    
    macd_hist = features.get("macd_histogram", 0)
    
    # Reject longs if MACD histogram is negative (bearish momentum)
    if prediction == "long" and macd_hist < 0:
        return "skip"
    
    # Reject shorts if MACD histogram is positive (bullish momentum)
    if prediction == "short" and macd_hist > 0:
        return "skip"
    
    return prediction