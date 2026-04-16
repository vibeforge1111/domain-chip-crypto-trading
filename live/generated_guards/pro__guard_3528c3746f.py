def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count confirming signals for the predicted direction
    confirmations = 0
    
    # RSI confirmation (not overbought/oversold)
    if prediction == "long" and features.get("rsi_14", 50) < 70:
        confirmations += 1
    elif prediction == "short" and features.get("rsi_14", 50) > 30:
        confirmations += 1
    
    # Stochastic confirmation
    if prediction == "long" and features.get("stoch_k", 50) < 80:
        confirmations += 1
    elif prediction == "short" and features.get("stoch_k", 50) > 20:
        confirmations += 1
    
    # VWAP confirmation
    if prediction == "long" and features.get("vwap_deviation", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0:
        confirmations += 1
    
    # OBV slope confirmation
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        confirmations += 1
    
    # MACD histogram confirmation
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        confirmations += 1
    
    # Require at least 2 confirming signals
    if confirmations < 2:
        return "skip"
    
    return prediction