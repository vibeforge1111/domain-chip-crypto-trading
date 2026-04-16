def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction detected by OBV slope."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV slope negative (distribution pressure)
    # Skip shorts when OBV slope positive (accumulation pressure)
    # Allow neutral zone (uncertain flow)
    if prediction == "long" and obv_slope < -0.15:
        return "skip"
    if prediction == "short" and obv_slope > 0.15:
        return "skip"
    
    return prediction