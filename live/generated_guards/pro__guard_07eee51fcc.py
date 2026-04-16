def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram shows momentum deceleration against direction."""
    macd_hist = features.get("macd_histogram", 0)
    
    # Skip longs when histogram is negative (momentum decelerating)
    if prediction == "long" and macd_hist < -0.0003:
        return "skip"
    
    # Skip shorts when histogram is positive (momentum decelerating)
    if prediction == "short" and macd_hist > 0.0003:
        return "skip"
    
    return prediction