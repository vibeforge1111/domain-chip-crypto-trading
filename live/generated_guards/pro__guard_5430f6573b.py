def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI 2h confirmation
    if prediction == "long" and features.get("rsi_2h", 50) < 55:
        confirmations += 1
    elif prediction == "short" and features.get("rsi_2h", 50) > 45:
        confirmations += 1
    
    # Stochastic confirmation (K crossing above D for long, below for short)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    if prediction == "long" and stoch_k > stoch_d and stoch_k < 50:
        confirmations += 1
    elif prediction == "short" and stoch_k < stoch_d and stoch_k > 50:
        confirmations += 1
    
    # VWAP deviation confirmation
    if prediction == "long" and features.get("vwap_deviation", 0) > -0.003:
        confirmations += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0.003:
        confirmations += 1
    
    # OBV slope confirmation
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        confirmations += 1
    
    # MACD histogram confirmation
    if prediction == "long" and features.get("macd_histogram", 0) > -0.0001:
        confirmations += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0.0001:
        confirmations += 1
    
    # BB position confirmation
    if prediction == "long" and features.get("bb_pct_b", 0.5) < 0.4:
        confirmations += 1
    elif prediction == "short" and features.get("bb_pct_b", 0.5) > 0.6:
        confirmations += 1
    
    return "skip" if confirmations < 2 else prediction