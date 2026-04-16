def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Reject trades conflicting with OBV flow
    if obv_slope > 0.05 and prediction == "short":
        return "skip"
    if obv_slope < -0.05 and prediction == "long":
        return "skip"
    
    # Avoid counter-trend entries at extremes
    if stoch_k > 80 and rsi_2h > 65 and prediction == "long":
        return "skip"
    if stoch_k < 20 and rsi_2h < 35 and prediction == "short":
        return "skip"
    
    return prediction