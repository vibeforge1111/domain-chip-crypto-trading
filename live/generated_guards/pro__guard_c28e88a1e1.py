def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV slope is negative (selling pressure/institutional distribution)
    if prediction == "long" and obv_slope < -0.01:
        return "skip"
    
    # Skip shorts when OBV slope is positive (buying pressure/institutional accumulation)
    if prediction == "short" and obv_slope > 0.01:
        return "skip"
    
    return prediction