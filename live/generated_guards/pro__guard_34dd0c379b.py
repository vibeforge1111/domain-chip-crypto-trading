def guard(features: dict, prediction: str) -> str:
    """Custom guard function filtering vwap_deviation and momentum disagreement."""
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Skip if price below VWAP but stoch overbought (bearish disagreement)
    if vwap_dev < -0.008 and stoch_k > 75 and stoch_d > 65:
        return "skip"
    
    # Skip if price above VWAP but stoch oversold (bullish disagreement)
    if vwap_dev > 0.008 and stoch_k < 25 and stoch_d < 35:
        return "skip"
    
    # Skip if BB position contradicts VWAP deviation
    if vwap_dev < -0.01 and bb_pct_b > 0.85:
        return "skip"
    if vwap_dev > 0.01 and bb_pct_b < 0.15:
        return "skip"
    
    return prediction