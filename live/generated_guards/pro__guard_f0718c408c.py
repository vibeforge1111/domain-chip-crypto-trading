def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    volume_ratio = features.get("volume_ratio", 1)
    
    # Only filter if volume confirms the signal (not low volume noise)
    if volume_ratio < 1.0:
        return prediction
    
    # Skip longs when OBV shows distribution (selling pressure)
    if prediction == "long" and obv_slope < -0.3:
        return "skip"
    
    # Skip shorts when OBV shows accumulation (buying pressure)
    if prediction == "short" and obv_slope > 0.3:
        return "skip"
    
    return prediction