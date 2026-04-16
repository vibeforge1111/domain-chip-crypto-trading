def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # VWAP confirmation
    if features.get("vwap_deviation", 0) > 0:
        confirmations += 1
    elif features.get("vwap_deviation", 0) < 0:
        confirmations += 1
    
    # Stochastic confirmation (both K and D aligned)
    if features.get("stoch_k", 0) > features.get("stoch_d", 0):
        confirmations += 1
    else:
        confirmations += 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        confirmations += 1
    elif features.get("macd_histogram", 0) < 0:
        confirmations += 1
    
    # OBV slope confirmation
    if features.get("obv_slope", 0) > 0:
        confirmations += 1
    elif features.get("obv_slope", 0) < 0:
        confirmations += 1
    
    # Require at least 2 confirmations to proceed
    if confirmations >= 2:
        return prediction
    return "skip"