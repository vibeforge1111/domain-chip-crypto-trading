def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Filter trades too close to fair value (VWAP within 0.15%)
    if abs(vwap_dev) < 0.0015:
        return "skip"
    
    # Reject longs at overbought levels
    if prediction == "long" and stoch_k > 85:
        return "skip"
    
    # Reject shorts at oversold levels
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction