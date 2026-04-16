def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction based on OBV slope."""
    obv_slope = features.get("obv_slope", 0)
    obv_threshold = 0.08
    
    # Skip longs during significant distribution (negative OBV slope)
    if prediction == "long" and obv_slope < -obv_threshold:
        return "skip"
    
    # Skip shorts during significant accumulation (positive OBV slope)
    if prediction == "short" and obv_slope > obv_threshold:
        return "skip"
    
    return prediction