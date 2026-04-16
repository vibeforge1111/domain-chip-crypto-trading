def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using RSI."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # Reject longs when 2h RSI is overbought (>65) - broad trend may be exhausted
    if prediction == "long" and rsi_2h > 65:
        return "skip"
    
    # Reject shorts when 2h RSI is oversold (<35) - broad trend may be recovering
    if prediction == "short" and rsi_2h < 35:
        return "skip"
    
    return prediction