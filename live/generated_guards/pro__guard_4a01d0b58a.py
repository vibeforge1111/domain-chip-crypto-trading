def guard(features: dict, prediction: str) -> str:
    """Filter trades against the broader 2-hour trend."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # Reject longs when 2-hour RSI is above 60 (overbought broader context)
    if prediction == "long" and rsi_2h > 60:
        return "skip"
    
    # Reject shorts when 2-hour RSI is below 40 (oversold broader context)
    if prediction == "short" and rsi_2h < 40:
        return "skip"
    
    return prediction