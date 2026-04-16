def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish signals
    bullish = 0
    if features.get("stoch_k", 50) < 70:
        bullish += 1
    if features.get("vwap_deviation", 0) > 0:
        bullish += 1
    if features.get("obv_slope", 0) > 0:
        bullish += 1
    if features.get("macd_histogram", 0) > 0:
        bullish += 1
    if features.get("rsi_2h", 50) < 60:
        bullish += 1
    if features.get("bb_pct_b", 0.5) > 0.3:
        bullish += 1
    
    # Count bearish signals
    bearish = 0
    if features.get("stoch_k", 50) > 30:
        bearish += 1
    if features.get("vwap_deviation", 0) < 0:
        bearish += 1
    if features.get("obv_slope", 0) < 0:
        bearish += 1
    if features.get("macd_histogram", 0) < 0:
        bearish += 1
    if features.get("rsi_2h", 50) > 40:
        bearish += 1
    if features.get("bb_pct_b", 0.5) < 0.7:
        bearish += 1
    
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction