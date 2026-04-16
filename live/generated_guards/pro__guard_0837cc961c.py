def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using OBV slope."""
    obv_slope = features.get("obv_slope", 0)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Skip longs when OBV is in downtrend (diverging from bullish signal)
    if prediction == "long" and obv_slope < -0.1:
        return "skip"
    
    # Skip shorts when OBV is in uptrend (diverging from bearish signal)
    if prediction == "short" and obv_slope > 0.1:
        return "skip"
    
    # Additional VWAP alignment check
    if prediction == "long" and vwap_deviation < -0.005:
        return "skip"
    
    if prediction == "short" and vwap_deviation > 0.005:
        return "skip"
    
    return prediction