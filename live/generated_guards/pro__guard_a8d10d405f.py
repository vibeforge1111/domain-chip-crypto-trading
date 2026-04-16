def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction detected by obv_slope."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV is falling (distribution)
    if prediction == "long" and obv_slope < -0.5:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation)
    if prediction == "short" and obv_slope > 0.5:
        return "skip"
    
    return prediction