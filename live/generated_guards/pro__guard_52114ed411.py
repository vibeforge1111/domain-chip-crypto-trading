def guard(features: dict, prediction: str) -> str:
    """Filter trades against broader 2-hour trend using rsi_2h."""
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when 2h RSI is oversold (counter-trend)
    if prediction == "long" and rsi_2h < 40:
        return "skip"
    # Skip shorts when 2h RSI is overbought (counter-trend)
    if prediction == "short" and rsi_2h > 60:
        return "skip"
    
    return prediction