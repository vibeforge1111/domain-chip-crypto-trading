def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum shows deceleration via MACD histogram."""
    macd = features.get("macd_histogram", 0)
    rsi = features.get("rsi_14", 50)
    
    if prediction == "long":
        # Reject longs when MACD histogram is negative (bearish momentum)
        if macd < 0:
            return "skip"
    elif prediction == "short":
        # Reject shorts when MACD histogram is positive (bullish momentum)
        if macd > 0:
            return "skip"
    
    return prediction