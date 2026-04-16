def guard(features: dict, prediction: str) -> str:
    """OBV flow direction guard - skip trades against volume flow."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV shows distribution (negative slope = weak volume)
    if prediction == "long" and obv_slope < -0.1:
        return "skip"
    
    # Skip shorts when OBV shows accumulation (positive slope = strong volume)
    if prediction == "short" and obv_slope > 0.1:
        return "skip"
    
    return prediction