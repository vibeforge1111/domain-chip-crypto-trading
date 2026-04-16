def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # VWAP confirmation
    if features.get("vwap_deviation", 0) > 0.002:
        confirmations += 1
    elif features.get("vwap_deviation", 0) < -0.002:
        confirmations -= 1
    
    # Stochastic confirmation
    stoch = features.get("stoch_k", 50)
    if prediction == "long" and stoch < 80 and stoch > 20:
        confirmations += 1
    elif prediction == "short" and stoch > 20 and stoch < 80:
        confirmations -= 1
    
    # OBV slope confirmation
    if features.get("obv_slope", 0) > 0:
        confirmations += 1
    elif features.get("obv_slope", 0) < 0:
        confirmations -= 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        confirmations += 1
    elif features.get("macd_histogram", 0) < 0:
        confirmations -= 1
    
    # RSI 2h confirmation
    rsi2h = features.get("rsi_2h", 50)
    if prediction == "long" and 30 < rsi2h < 70:
        confirmations += 1
    elif prediction == "short" and 30 < rsi2h < 70:
        confirmations -= 1
    
    # Require at least 2 confirmations in the right direction
    if prediction == "long" and confirmations < 2:
        return "skip"
    elif prediction == "short" and confirmations > -2:
        return "skip"
    
    return prediction