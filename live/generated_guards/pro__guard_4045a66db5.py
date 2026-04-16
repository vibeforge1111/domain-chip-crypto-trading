def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using VWAP deviation."""
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Reject trades when price is too close to VWAP (no edge)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Reject overbought/oversold extremes with VWAP alignment
    if stoch_k > 85 and stoch_d > 80 and vwap_dev > 0:
        return "skip"
    if stoch_k < 15 and stoch_d < 20 and vwap_dev < 0:
        return "skip"
    
    return prediction