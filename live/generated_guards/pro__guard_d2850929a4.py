def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    agree_count = 0
    
    if prediction == "long":
        # Bullish conditions
        if features.get("rsi_14", 50) < 65:
            agree_count += 1
        if features.get("stoch_k", 50) < 75:
            agree_count += 1
        if features.get("macd_histogram", 0) > 0:
            agree_count += 1
        if features.get("vwap_deviation", 0) < 0.005:
            agree_count += 1
        if features.get("bb_pct_b", 0.5) < 0.25:
            agree_count += 1
        if features.get("rsi_2h", 50) < 70:
            agree_count += 1
        if features.get("obv_slope", 0) > 0:
            agree_count += 1
    elif prediction == "short":
        # Bearish conditions
        if features.get("rsi_14", 50) > 35:
            agree_count += 1
        if features.get("stoch_k", 50) > 25:
            agree_count += 1
        if features.get("macd_histogram", 0) < 0:
            agree_count += 1
        if features.get("vwap_deviation", 0) > 0.005:
            agree_count += 1
        if features.get("bb_pct_b", 0.5) > 0.75:
            agree_count += 1
        if features.get("rsi_2h", 50) > 30:
            agree_count += 1
        if features.get("obv_slope", 0) < 0:
            agree_count += 1
    
    return prediction if agree_count >= 2 else "skip"