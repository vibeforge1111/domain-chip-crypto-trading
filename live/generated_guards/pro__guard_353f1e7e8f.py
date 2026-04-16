def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using rsi_2h."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # If 2h RSI > 55, reject shorts (broader uptrend)
    if rsi_2h > 55 and prediction == "short":
        return "skip"
    
    # If 2h RSI < 45, reject longs (broader downtrend)
    if rsi_2h < 45 and prediction == "long":
        return "skip"
    
    return prediction