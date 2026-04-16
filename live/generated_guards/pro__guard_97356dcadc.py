def guard(features: dict, prediction: str) -> str:
    """Filter trades conflicting with 2-hour RSI trend."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # Reject longs when 2h RSI is overbought (buying at resistance)
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    
    # Reject shorts when 2h RSI is oversold (shorting at support)
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction