def guard(features: dict, prediction: str) -> str:
    """Guard using BB extremes with momentum confirmation."""
    bb_pct = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    obv_slope = features.get("obv_slope", 0)
    
    # Long requires BB at lower extreme (<0.05) and bullish confirmation
    if prediction == "long":
        if bb_pct >= 0.05:
            return "skip"
        if vwap_dev > 0.005:  # Price too far above VWAP
            return "skip"
        if stoch_k > 80 and obv_slope < 0:  # Not oversold or no accumulation
            return "skip"
    
    # Short requires BB at upper extreme (>0.95) and bearish confirmation
    if prediction == "short":
        if bb_pct <= 0.95:
            return "skip"
        if vwap_dev < -0.005:  # Price too far below VWAP
            return "skip"
        if stoch_k < 20 and obv_slope > 0:  # Not overbought or still accumulating
            return "skip"
    
    return prediction