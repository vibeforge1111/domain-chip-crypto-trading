def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # VWAP confirmation (strong level)
    vwap_dev = features.get("vwap_deviation", 0)
    if prediction == "long" and vwap_dev > 0:
        confirmations += 1
    elif prediction == "short" and vwap_dev < 0:
        confirmations += 1
    
    # Stochastic confirmation
    stoch_k = features.get("stoch_k", 50)
    if prediction == "long" and stoch_k < 80:
        confirmations += 1
    elif prediction == "short" and stoch_k > 20:
        confirmations += 1
    
    # MACD histogram confirmation
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        confirmations += 1
    
    # RSI 2h trend confirmation
    rsi_2h = features.get("rsi_2h", 50)
    if prediction == "long" and 30 < rsi_2h < 70:
        confirmations += 1
    elif prediction == "short" and 30 < rsi_2h < 70:
        confirmations += 1
    
    # OBV slope confirmation
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        confirmations += 1
    
    return "skip" if confirmations < 2 else prediction