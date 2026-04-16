def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP) with momentum confirmation."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if price is too close to VWAP (within 0.2%)
    if abs(vwap_dev) < 0.002:
        return "skip"
    
    # Additional filter: skip long signals when stoch overbought
    if prediction == "long" and stoch_k > 80:
        return "skip"
    
    # Additional filter: skip short signals when stoch oversold
    if prediction == "short" and stoch_k < 20:
        return "skip"
    
    return prediction