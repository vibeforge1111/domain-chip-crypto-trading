def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard - requires 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # VWAP alignment check
    vwap_ok = features.get("vwap_deviation", 0) > 0 if prediction == "long" else features.get("vwap_deviation", 0) < 0
    if vwap_ok:
        confirmations += 1
    
    # Stochastic position check (not overbought/oversold extremes)
    stoch_ok = 30 < features.get("stoch_k", 50) < 70
    if stoch_ok:
        confirmations += 1
    
    # OBV slope alignment check
    obv_ok = features.get("obv_slope", 0) > 0 if prediction == "long" else features.get("obv_slope", 0) < 0
    if obv_ok:
        confirmations += 1
    
    # MACD histogram alignment check
    macd_ok = features.get("macd_histogram", 0) > 0 if prediction == "long" else features.get("macd_histogram", 0) < 0
    if macd_ok:
        confirmations += 1
    
    return "skip" if confirmations < 2 else prediction