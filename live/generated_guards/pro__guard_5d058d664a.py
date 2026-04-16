def guard(features: dict, prediction: str) -> str:
    """Filter trades that are too close to fair value using VWAP deviation."""
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip if price is within 0.3% of VWAP (too close to fair value)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Skip if stochastic is in extreme zone (80+ or 20-) and far from VWAP
    # This suggests mean-reversion risk
    if stoch_k > 85 or stoch_k < 15:
        if abs(vwap_dev) > 0.01:
            return "skip"
    
    # Skip if 2h RSI disagrees with prediction direction
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    
    return prediction