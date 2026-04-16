def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV is falling (distribution) and shorts when rising (accumulation)
    if prediction == "long" and obv_slope < 0:
        return "skip"
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    return prediction