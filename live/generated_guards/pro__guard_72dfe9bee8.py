def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction (OBV slope alignment)."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV slope is negative (selling pressure / distribution)
    if prediction == "long" and obv_slope < -0.1:
        return "skip"
    
    # Skip shorts when OBV slope is positive (buying pressure / accumulation)
    if prediction == "short" and obv_slope > 0.1:
        return "skip"
    
    return prediction