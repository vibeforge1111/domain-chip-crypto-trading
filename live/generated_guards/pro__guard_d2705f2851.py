def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard - requires 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation
    if prediction == "long" and features.get("rsi_14", 50) < 35:
        confirmations += 1
    if prediction == "short" and features.get("rsi_14", 50) > 65:
        confirmations += 1
    
    # VWAP confirmation
    if prediction == "long" and features.get("vwap_deviation", 0) > 0.002:
        confirmations += 1
    if prediction == "short" and features.get("vwap_deviation", 0) < -0.002:
        confirmations += 1
    
    # Stochastic confirmation
    if prediction == "long" and features.get("stoch_k", 50) < 25:
        confirmations += 1
    if prediction == "short" and features.get("stoch_k", 50) > 75:
        confirmations += 1
    
    # OBV slope confirmation
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        confirmations += 1
    if prediction == "short" and features.get("obv_slope", 0) < 0:
        confirmations += 1
    
    # MACD histogram confirmation
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        confirmations += 1
    if prediction == "short" and features.get("macd_histogram", 0) < 0:
        confirmations += 1
    
    if confirmations < 2:
        return "skip"
    return prediction