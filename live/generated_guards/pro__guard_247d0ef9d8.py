def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    if prediction == "long":
        if features.get("vwap_deviation", 0) > 0.001:
            confirmations += 1
        if features.get("stoch_k", 50) < 80 and features.get("stoch_d", 50) < 80:
            confirmations += 1
        if features.get("obv_slope", 0) > 0:
            confirmations += 1
        if features.get("macd_histogram", 0) > 0:
            confirmations += 1
        if features.get("rsi_2h", 50) > 40:
            confirmations += 1
    elif prediction == "short":
        if features.get("vwap_deviation", 0) < -0.001:
            confirmations += 1
        if features.get("stoch_k", 50) > 20 and features.get("stoch_d", 50) > 20:
            confirmations += 1
        if features.get("obv_slope", 0) < 0:
            confirmations += 1
        if features.get("macd_histogram", 0) < 0:
            confirmations += 1
        if features.get("rsi_2h", 50) < 60:
            confirmations += 1
    
    return prediction if confirmations >= 2 else "skip"