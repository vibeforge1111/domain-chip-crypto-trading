def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction as indicated by OBV slope."""
    obv_slope = features.get("obv_slope", 0)
    
    # Reject longs when OBV shows distribution (negative slope)
    if prediction == "long" and obv_slope < -0.3:
        return "skip"
    
    # Reject shorts when OBV shows accumulation (positive slope)
    if prediction == "short" and obv_slope > 0.3:
        return "skip"
    
    return prediction