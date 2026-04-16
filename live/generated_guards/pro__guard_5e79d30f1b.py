def guard(features: dict, prediction: str) -> str:
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    
    # For longs, skip if broader trend (2h RSI) is bearish
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    # For shorts, skip if broader trend (2h RSI) is bullish
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    # Avoid counter-trend entries: longs when 2h RSI bearish AND stoch overbought
    if prediction == "long" and rsi_2h < 45 and stoch_k > 70:
        return "skip"
    
    # Avoid counter-trend entries: shorts when 2h RSI bullish AND stoch oversold
    if prediction == "short" and rsi_2h > 55 and stoch_k < 30:
        return "skip"
    
    return prediction