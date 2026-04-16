def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using obv_slope."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV is declining (distribution), skip shorts when OBV is rising (accumulation)
    if prediction == "long" and obv_slope < -0.1:
        return "skip"
    if prediction == "short" and obv_slope > 0.1:
        return "skip"
    
    return prediction