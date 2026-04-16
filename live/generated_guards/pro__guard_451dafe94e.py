def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV momentum flow, with VWAP confirmation."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Skip longs if OBV is declining (distribution) or price well below VWAP
    if prediction == "long":
        if obv_slope < -0.3 or vwap_deviation < -0.015:
            return "skip"
    
    # Skip shorts if OBV is rising (accumulation) or price well above VWAP
    if prediction == "short":
        if obv_slope > 0.3 or vwap_deviation > 0.015:
            return "skip"
    
    return prediction