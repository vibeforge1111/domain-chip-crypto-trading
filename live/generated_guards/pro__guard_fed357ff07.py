def guard(features: dict, prediction: str) -> str:
    """Accept trades only at Bollinger Band extremes with momentum confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    if prediction == "long":
        if bb_pct_b >= 0.05:
            return "skip"
        if stoch_k >= 25:
            return "skip"
        if vwap_deviation >= 0:
            return "skip"
    
    if prediction == "short":
        if bb_pct_b <= 0.95:
            return "skip"
        if stoch_k <= 75:
            return "skip"
        if vwap_deviation <= 0:
            return "skip"
    
    return prediction