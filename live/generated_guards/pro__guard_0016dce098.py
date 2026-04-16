def guard(features: dict, prediction: str) -> str:
    """Guard using BB extremes with momentum confirmation."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    obv_slope = features.get("obv_slope", 0)
    
    # BB at extreme lower band (<0.05) - high confidence long zone
    if bb_pct < 0.05:
        if prediction == "long":
            if stoch_k < 20 and rsi_2h < 50:
                return prediction
        return "skip"
    
    # BB at extreme upper band (>0.95) - high confidence short zone
    if bb_pct > 0.95:
        if prediction == "short":
            if stoch_k > 80 and rsi_2h > 50:
                return prediction
        return "skip"
    
    # Outside extreme zones - skip
    return "skip"