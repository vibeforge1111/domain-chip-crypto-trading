def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    rsi_ok = features.get("rsi_2h", 50)
    stoch_ok = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    obv = features.get("obv_slope", 0)
    macd = features.get("macd_histogram", 0)
    
    if prediction == "long":
        bullish = int(rsi_ok < 70) + int(stoch_ok < 80) + int(vwap_dev > 0) + int(obv > 0) + int(macd > 0)
        return prediction if bullish >= 2 else "skip"
    
    if prediction == "short":
        bearish = int(rsi_ok > 30) + int(stoch_ok > 20) + int(vwap_dev < 0) + int(obv < 0) + int(macd < 0)
        return prediction if bearish >= 2 else "skip"
    
    return prediction