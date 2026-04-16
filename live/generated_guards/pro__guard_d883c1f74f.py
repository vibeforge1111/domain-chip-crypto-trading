def guard(features: dict, prediction: str) -> str:
    """Filter trades against the broader 2-hour trend."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Reject longs when 2h RSI shows bearish momentum
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    # Reject shorts when 2h RSI shows bullish momentum
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction