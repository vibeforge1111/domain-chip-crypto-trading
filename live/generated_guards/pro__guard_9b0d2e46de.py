def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Stochastic alignment (k above d for longs, below for shorts)
    if prediction == "long" and features.get("stoch_k", 50) > features.get("stoch_d", 50):
        confirmations += 1
    if prediction == "short" and features.get("stoch_k", 50) < features.get("stoch_d", 50):
        confirmations += 1
    
    # VWAP confirmation (above for longs, below for shorts)
    if prediction == "long" and features.get("vwap_deviation", 0) > 0:
        confirmations += 1
    if prediction == "short" and features.get("vwap_deviation", 0) < 0:
        confirmations += 1
    
    # RSI 2h trend confirmation
    if prediction == "long" and features.get("rsi_2h", 50) > 50:
        confirmations += 1
    if prediction == "short" and features.get("rsi_2h", 50) < 50:
        confirmations += 1
    
    # OBV momentum confirmation
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        confirmations += 1
    if prediction == "short" and features.get("obv_slope", 0) < 0:
        confirmations += 1
    
    # MACD histogram confirmation
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        confirmations += 1
    if prediction == "short" and features.get("macd_histogram", 0) < 0:
        confirmations += 1
    
    # Require at least 2 confirmations
    if confirmations < 2:
        return "skip"
    
    return prediction