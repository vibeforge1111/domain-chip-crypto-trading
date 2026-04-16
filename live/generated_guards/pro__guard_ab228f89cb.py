def guard(features: dict, prediction: str) -> str:
    """Reject trades when macd_histogram shows momentum deceleration against direction."""
    macd = features.get("macd_histogram", 0)
    
    # Skip longs when macd histogram is negative (momentum bearish)
    if prediction == "long" and macd < 0:
        return "skip"
    
    # Skip shorts when macd histogram is positive (momentum bullish)
    if prediction == "short" and macd > 0:
        return "skip"
    
    return prediction