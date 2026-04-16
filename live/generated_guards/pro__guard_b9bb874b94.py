def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    if prediction == "long" and obv_slope < -0.01:
        return "skip"
    if prediction == "short" and obv_slope > 0.01:
        return "skip"
    
    return prediction