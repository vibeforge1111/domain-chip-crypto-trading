def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV flow direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV is declining (distribution flow)
    if prediction == "long" and obv_slope < -0.3:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation flow)
    if prediction == "short" and obv_slope > 0.3:
        return "skip"
    
    return prediction