def guard(features: dict, prediction: str) -> str:
    """Filter trades where MACD histogram shows momentum against direction."""
    if prediction == "skip":
        return prediction
    
    macd_hist = features.get("macd_histogram", 0)
    
    # Reject longs when MACD histogram is negative (bearish momentum)
    if prediction == "long" and macd_hist < -0.0002:
        return "skip"
    
    # Reject shorts when MACD histogram is positive (bullish momentum)
    if prediction == "short" and macd_hist > 0.0002:
        return "skip"
    
    return prediction