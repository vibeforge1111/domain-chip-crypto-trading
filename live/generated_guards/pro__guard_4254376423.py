def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction (OBV slope)."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV shows strong distribution (negative slope)
    if prediction == "long" and obv_slope < -0.3:
        return "skip"
    
    # Skip shorts when OBV shows strong accumulation (positive slope)
    if prediction == "short" and obv_slope > 0.3:
        return "skip"
    
    return prediction