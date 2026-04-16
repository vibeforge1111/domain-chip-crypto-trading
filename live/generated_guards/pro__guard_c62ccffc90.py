def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish = sum([
        features.get("rsi_14", 50) < 65,
        features.get("stoch_k", 50) < 75,
        features.get("vwap_deviation", 0) > 0,
        features.get("macd_histogram", 0) > 0,
        features.get("obv_slope", 0) > 0,
        features.get("bb_pct_b", 0.5) < 0.85,
        features.get("rsi_2h", 50) < 70
    ])
    
    bearish = sum([
        features.get("rsi_14", 50) > 35,
        features.get("stoch_k", 50) > 25,
        features.get("vwap_deviation", 0) < 0,
        features.get("macd_histogram", 0) < 0,
        features.get("obv_slope", 0) < 0,
        features.get("bb_pct_b", 0.5) > 0.15,
        features.get("rsi_2h", 50) > 30
    ])
    
    if prediction == "long" and bullish >= 2:
        return prediction
    if prediction == "short" and bearish >= 2:
        return prediction
    
    return "skip"