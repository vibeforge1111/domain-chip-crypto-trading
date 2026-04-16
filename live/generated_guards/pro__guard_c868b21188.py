def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV is falling (selling pressure)
    if prediction == "long" and obv_slope < -0.001:
        return "skip"
    # Skip shorts when OBV is rising (buying pressure)
    if prediction == "short" and obv_slope > 0.001:
        return "skip"
    
    return prediction