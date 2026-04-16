def guard(features: dict, prediction: str) -> str:
    """Skip trades that contradict volume flow direction (OBV slope)."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    threshold = 0.01
    
    # Skip longs when OBV is declining (smart money distributing)
    if prediction == "long" and obv_slope < -threshold:
        return "skip"
    
    # Skip shorts when OBV is rising (smart money accumulating)
    if prediction == "short" and obv_slope > threshold:
        return "skip"
    
    return prediction