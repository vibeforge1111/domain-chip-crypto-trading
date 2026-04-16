def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bullish += features.get("rsi_14", 50) < 70
    bullish += features.get("stoch_k", 50) < 80
    bullish += features.get("vwap_deviation", 0) > 0
    bullish += features.get("macd_histogram", 0) > 0
    bullish += features.get("obv_slope", 0) > 0
    bullish += features.get("bb_pct_b", 0.5) < 0.5
    bullish += features.get("rsi_2h", 50) > 50
    
    bearish = 0
    bearish += features.get("rsi_14", 50) > 30
    bearish += features.get("stoch_k", 50) > 20
    bearish += features.get("vwap_deviation", 0) < 0
    bearish += features.get("macd_histogram", 0) < 0
    bearish += features.get("obv_slope", 0) < 0
    bearish += features.get("bb_pct_b", 0.5) > 0.5
    bearish += features.get("rsi_2h", 50) < 50
    
    if prediction == "long" and bullish >= 2:
        return prediction
    if prediction == "short" and bearish >= 2:
        return prediction
    
    return "skip"