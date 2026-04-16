def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish signals
    bullish_count = 0
    if features.get("rsi_14", 50) < 65:
        bullish_count += 1
    if features.get("stoch_k", 50) < 75:
        bullish_count += 1
    if features.get("vwap_deviation", 0) > -0.015:
        bullish_count += 1
    if features.get("macd_histogram", 0) >= 0:
        bullish_count += 1
    if features.get("bb_pct_b", 0.5) < 0.8:
        bullish_count += 1
    
    # Count bearish signals
    bearish_count = 0
    if features.get("rsi_14", 50) > 35:
        bearish_count += 1
    if features.get("stoch_k", 50) > 25:
        bearish_count += 1
    if features.get("vwap_deviation", 0) < 0.015:
        bearish_count += 1
    if features.get("macd_histogram", 0) <= 0:
        bearish_count += 1
    if features.get("bb_pct_b", 0.5) > 0.2:
        bearish_count += 1
    
    # Require at least 2 signals to agree
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction