def guard(features: dict, prediction: str) -> str:
    """Use OBV slope to filter trades against volume flow."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Skip longs when OBV is falling (distribution) AND price below VWAP
    if prediction == "long" and obv_slope < -0.3 and vwap_deviation < -0.002:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation) AND price above VWAP
    if prediction == "short" and obv_slope > 0.3 and vwap_deviation > 0.002:
        return "skip"
    
    return prediction