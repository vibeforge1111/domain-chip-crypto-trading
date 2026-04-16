def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Stochastic momentum
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    if prediction == "long" and stoch_k > stoch_d:
        confirmations += 1
    elif prediction == "short" and stoch_k < stoch_d:
        confirmations += 1
    
    # OBV accumulation/distribution
    obv_slope = features.get("obv_slope", 0)
    if prediction == "long" and obv_slope > 0:
        confirmations += 1
    elif prediction == "short" and obv_slope < 0:
        confirmations += 1
    
    # MACD momentum
    macd_histogram = features.get("macd_histogram", 0)
    if prediction == "long" and macd_histogram > 0:
        confirmations += 1
    elif prediction == "short" and macd_histogram < 0:
        confirmations += 1
    
    # VWAP position
    vwap_deviation = features.get("vwap_deviation", 0)
    if prediction == "long" and vwap_deviation >= 0:
        confirmations += 1
    elif prediction == "short" and vwap_deviation <= 0:
        confirmations += 1
    
    # BB position
    bb_pct_b = features.get("bb_pct_b", 0.5)
    if prediction == "long" and bb_pct_b < 0.7:
        confirmations += 1
    elif prediction == "short" and bb_pct_b > 0.3:
        confirmations += 1
    
    return prediction if confirmations >= 2 else "skip"