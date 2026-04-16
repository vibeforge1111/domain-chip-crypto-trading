def guard(features: dict, prediction: str) -> str:
    """Filter trades when both BB position and Stochastic show extreme conditions."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Reject when overbought (both indicators confirm)
    if bb_pct_b > 0.90 and stoch_k > 80 and prediction == "long":
        return "skip"
    
    # Reject when oversold (both indicators confirm)
    if bb_pct_b < 0.10 and stoch_k < 20 and prediction == "short":
        return "skip"
    
    # Additional filter: reject trades too far from VWAP
    if abs(vwap_dev) > 0.02:
        return "skip"
    
    return prediction