def guard(features: dict, prediction: str) -> str:
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip longs when 2h RSI is overbought (counter-trend entry)
    if prediction == "long" and rsi_2h > 75:
        return "skip"
    
    # Skip shorts when 2h RSI is oversold (counter-trend entry)
    if prediction == "short" and rsi_2h < 25:
        return "skip"
    
    return prediction