def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Bollinger Band confirmation
    if features.get("bb_pct_b", 0.5) > 0.6:
        confirmations += 1
    elif features.get("bb_pct_b", 0.5) < 0.4:
        confirmations -= 1
    
    # VWAP confirmation
    if features.get("vwap_deviation", 0) > 0.001:
        confirmations += 1
    elif features.get("vwap_deviation", 0) < -0.001:
        confirmations -= 1
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) > 60 and features.get("stoch_d", 50) > 50:
        confirmations += 1
    elif features.get("stoch_k", 50) < 40 and features.get("stoch_d", 50) < 50:
        confirmations -= 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        confirmations += 1
    elif features.get("macd_histogram", 0) < 0:
        confirmations -= 1
    
    # Require at least 2 indicators to agree with prediction direction
    if prediction == "long" and confirmations < 2:
        return "skip"
    if prediction == "short" and confirmations > -2:
        return "skip"
    
    return prediction