def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value using VWAP deviation."""
    vwap_dev = abs(features.get('vwap_deviation', 0))
    stoch_k = features.get('stoch_k', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Skip if price too close to VWAP (no edge)
    if vwap_dev < 0.003:
        return "skip"
    
    # Skip extreme stochastic readings
    if stoch_k > 85 or stoch_k < 15:
        return "skip"
    
    # Skip if price near Bollinger Band center in uncertain zone
    if 0.35 < bb_pct_b < 0.65 and vwap_dev < 0.006:
        return "skip"
    
    return prediction