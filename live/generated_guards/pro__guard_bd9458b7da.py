def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend using rsi_2h."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when 2h RSI is overbought (broader trend weakening)
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    
    # Skip shorts when 2h RSI is oversold (broader trend strengthening)
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction