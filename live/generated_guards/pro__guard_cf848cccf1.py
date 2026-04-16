def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction based on OBV slope."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    threshold = 0.1
    
    # Skip longs when OBV slope is negative (bearish volume flow)
    if prediction == "long" and obv_slope < -threshold:
        return "skip"
    
    # Skip shorts when OBV slope is positive (bullish volume flow)
    if prediction == "short" and obv_slope > threshold:
        return "skip"
    
    return prediction