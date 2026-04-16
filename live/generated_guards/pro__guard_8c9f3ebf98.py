def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Skip long trades when OBV is declining (distribution pressure)
    if prediction == "long" and obv_slope < -0.01:
        return "skip"
    
    # Skip short trades when OBV is rising (accumulation pressure)
    if prediction == "short" and obv_slope > 0.01:
        return "skip"
    
    # Additional filter: skip longs if price well below VWAP with negative OBV
    if prediction == "long" and vwap_deviation < -0.02 and obv_slope < 0:
        return "skip"
    
    return prediction