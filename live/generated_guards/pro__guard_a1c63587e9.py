def guard(features: dict, prediction: str) -> str:
    """Filter trades against OBV volume flow direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs if OBV is declining (distribution pressure)
    if prediction == "long" and obv_slope < -0.01:
        return "skip"
    
    # Skip shorts if OBV is rising (accumulation pressure)
    if prediction == "short" and obv_slope > 0.01:
        return "skip"
    
    return prediction