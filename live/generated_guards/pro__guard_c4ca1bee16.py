def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return "skip"
    
    macd = features.get("macd_histogram", 0)
    stoch = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip if momentum is decelerating (negative macd histogram)
    if macd < -0.0003:
        return "skip"
    
    # Skip long entries in overbought zone with bearish momentum
    if prediction == "long" and stoch > 75 and macd < 0:
        return "skip"
    
    # Skip short entries in oversold zone with bullish momentum
    if prediction == "short" and stoch < 25 and macd > 0:
        return "skip"
    
    # Skip if wider timeframe is stretched and local momentum contradicts
    if rsi_2h > 65 and macd < 0 and prediction == "long":
        return "skip"
    if rsi_2h < 35 and macd > 0 and prediction == "short":
        return "skip"
    
    return prediction