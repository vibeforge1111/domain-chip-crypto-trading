def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV flow direction."""
    obv_slope = features.get("obv_slope", 0)
    volume_ratio = features.get("volume_ratio", 1)
    
    if volume_ratio > 0.7:
        if prediction == "long" and obv_slope < -0.01:
            return "skip"
        if prediction == "short" and obv_slope > 0.01:
            return "skip"
    
    return prediction