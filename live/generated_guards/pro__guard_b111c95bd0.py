def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    # Count confirmations using NEW features (bb_pct_b, vwap_deviation, stoch_k, stoch_d, obv_slope, macd_histogram, rsi_2h)
    bullish = sum([
        features.get("stoch_k", 50) < 25,
        features.get("stoch_d", 50) < 25,
        features.get("vwap_deviation", 0) > 0.005,
        features.get("obv_slope", 0) > 0,
        features.get("macd_histogram", 0) > 0,
        features.get("bb_pct_b", 0.5) < 0.25,
        features.get("rsi_2h", 50) < 45,
    ])
    
    bearish = sum([
        features.get("stoch_k", 50) > 75,
        features.get("stoch_d", 50) > 75,
        features.get("vwap_deviation", 0) < -0.005,
        features.get("obv_slope", 0) < 0,
        features.get("macd_histogram", 0) < 0,
        features.get("bb_pct_b", 0.5) > 0.75,
        features.get("rsi_2h", 50) > 55,
    ])
    
    if prediction == "long" and bullish >= 2:
        return "long"
    elif prediction == "short" and bearish >= 2:
        return "short"
    
    return "skip"