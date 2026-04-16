def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction detected by OBV slope."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV shows distribution (negative slope)
    if prediction == "long" and obv_slope < -0.02:
        return "skip"
    
    # Skip shorts when OBV shows accumulation (positive slope)
    if prediction == "short" and obv_slope > 0.02:
        return "skip"
    
    return prediction