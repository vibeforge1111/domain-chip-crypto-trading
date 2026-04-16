def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using obv_slope."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip trades against volume flow direction (magnitude threshold for meaningful flow)
    if prediction == "long" and obv_slope < -0.3:
        return "skip"
    if prediction == "short" and obv_slope > 0.3:
        return "skip"
    
    return prediction