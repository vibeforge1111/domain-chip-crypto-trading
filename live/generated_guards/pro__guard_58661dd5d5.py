def guard(features: dict, prediction: str) -> str:
    """Filter trades against OBV volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV is falling (distribution, not accumulation)
    if prediction == "long" and obv_slope < -0.01:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation, not distribution)
    if prediction == "short" and obv_slope > 0.01:
        return "skip"
    
    return prediction