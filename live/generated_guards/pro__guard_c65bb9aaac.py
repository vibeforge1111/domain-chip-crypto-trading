def guard(features: dict, prediction: str) -> str:
    """Filter trades based on VWAP deviation and new momentum features."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if too close to VWAP (no edge)
    if abs(vwap_dev) < 0.001:
        return "skip"
    
    # Skip if overextended with weak VWAP edge
    if (stoch_k > 85 or stoch_k < 15) and abs(vwap_dev) < 0.002:
        return "skip"
    
    # Skip if conflicting 2h RSI context
    if rsi_2h > 70 and vwap_dev < 0 and prediction == "long":
        return "skip"
    if rsi_2h < 30 and vwap_dev > 0 and prediction == "short":
        return "skip"
    
    return prediction