def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    rsi = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    macd = features.get("macd_histogram", 0)
    obv = features.get("obv_slope", 0)
    stoch_k = features.get("stoch_k", 50)
    vwap = features.get("vwap_deviation", 0)
    bb_pos = features.get("bb_pct_b", 0.5)
    
    bullish_count = (rsi < 30) + (rsi_2h < 40) + (macd > 0) + (obv > 0) + (stoch_k < 25)
    bearish_count = (rsi > 70) + (rsi_2h > 60) + (macd < 0) + (obv < 0) + (stoch_k > 75)
    
    if prediction == "long" and (bullish_count < 2 or vwap > 0.005 or bb_pos > 0.9):
        return "skip"
    if prediction == "short" and (bearish_count < 2 or vwap < -0.005 or bb_pos < 0.1):
        return "skip"
    
    return prediction