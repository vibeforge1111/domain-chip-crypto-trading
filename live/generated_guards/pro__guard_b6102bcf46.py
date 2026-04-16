def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum decelerates against position direction."""
    if prediction == "skip":
        return prediction
    
    macd_hist = features.get("macd_histogram", 0)
    
    # Skip longs when macd_histogram is negative (bearish momentum strengthening)
    if prediction == "long" and macd_hist < 0:
        return "skip"
    
    # Skip shorts when macd_histogram is positive (bullish momentum strengthening)
    if prediction == "short" and macd_hist > 0:
        return "skip"
    
    return prediction