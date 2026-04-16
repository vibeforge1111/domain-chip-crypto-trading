def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using obv_slope."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when volume is distributing (negative obv_slope)
    if prediction == "long" and obv_slope < -0.001:
        return "skip"
    
    # Skip shorts when volume is accumulating (positive obv_slope)
    if prediction == "short" and obv_slope > 0.001:
        return "skip"
    
    return prediction