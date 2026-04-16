def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using OBV slope."""
    obv_slope = features.get("obv_slope", 0)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Skip longs when OBV slope is negative (distribution)
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    
    # Skip shorts when OBV slope is positive (accumulation)
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    # Additional VWAP alignment filter
    if prediction == "long" and vwap_deviation < -0.015:
        return "skip"
    if prediction == "short" and vwap_deviation > 0.015:
        return "skip"
    
    return prediction