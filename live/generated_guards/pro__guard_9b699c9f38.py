def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV momentum direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    return prediction