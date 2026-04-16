def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    count = 0
    
    # RSI confirmation (14 and 2h)
    if features.get("rsi_14", 50) > 50:
        count += 1
    elif features.get("rsi_14", 50) < 50:
        count -= 1
    
    if features.get("rsi_2h", 50) > 50:
        count += 1
    elif features.get("rsi_2h", 50) < 50:
        count -= 1
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) > features.get("stoch_d", 50):
        count += 1
    else:
        count -= 1
    
    # VWAP confirmation
    if features.get("vwap_deviation", 0) > 0:
        count += 1
    else:
        count -= 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        count += 1
    else:
        count -= 1
    
    # OBV slope confirmation
    if features.get("obv_slope", 0) > 0:
        count += 1
    else:
        count -= 1
    
    # Require net agreement of 2+ indicators
    if abs(count) < 2:
        return "skip"
    
    # Direction check: for longs need positive bias, shorts need negative
    if prediction == "long" and count < 0:
        return "skip"
    if prediction == "short" and count > 0:
        return "skip"
    
    return prediction