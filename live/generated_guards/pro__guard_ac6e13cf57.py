def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    rsi_14 = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    macd = features.get("macd_histogram", 0)
    vwap = features.get("vwap_deviation", 0)
    
    long_count = sum([
        rsi_14 < 40,
        rsi_2h < 45,
        stoch_k < 30,
        macd > 0,
        vwap > 0
    ])
    
    short_count = sum([
        rsi_14 > 60,
        rsi_2h > 55,
        stoch_k > 70,
        macd < 0,
        vwap < 0
    ])
    
    if prediction == "long" and long_count >= 2:
        return prediction
    if prediction == "short" and short_count >= 2:
        return prediction
    
    return "skip"