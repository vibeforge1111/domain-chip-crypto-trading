def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    if features.get("bb_pct_b", 0.5) > 0.6:
        bullish += 1
    elif features.get("bb_pct_b", 0.5) < 0.4:
        bearish += 1
    
    if features.get("vwap_deviation", 0) > 0.005:
        bullish += 1
    elif features.get("vwap_deviation", 0) < -0.005:
        bearish += 1
    
    if features.get("stoch_k", 50) > features.get("stoch_d", 50):
        bullish += 1
    else:
        bearish += 1
    
    if features.get("obv_slope", 0) > 0:
        bullish += 1
    elif features.get("obv_slope", 0) < 0:
        bearish += 1
    
    if features.get("macd_histogram", 0) > 0:
        bullish += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish += 1
    
    if features.get("rsi_2h", 50) > 55:
        bullish += 1
    elif features.get("rsi_2h", 50) < 45:
        bearish += 1
    
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction