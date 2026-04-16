def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using VWAP deviation."""
    vwap_dev = features.get("vwap_deviation", 0)
    rsi_14 = features.get("rsi_14", 50)
    stoch_k = features.get("stoch_k", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Skip if price is too close to VWAP (low edge) and RSI is neutral/misaligned
    if abs(vwap_dev) < 0.002 and 40 < rsi_14 < 60:
        return "skip"
    
    # Skip if price near VWAP and stochastic is in neutral zone
    if abs(vwap_dev) < 0.003 and 30 < stoch_k < 70:
        return "skip"
    
    # Skip if near VWAP and BB position is middle range (no edge)
    if abs(vwap_dev) < 0.002 and 0.35 < bb_pct_b < 0.65:
        return "skip"
    
    return prediction