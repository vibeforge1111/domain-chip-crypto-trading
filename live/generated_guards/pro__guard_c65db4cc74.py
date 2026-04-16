def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering based on volume flow."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip trades against OBV volume flow direction
    if obv_slope > 0 and prediction == "short":
        return "skip"
    if obv_slope < 0 and prediction == "long":
        return "skip"
    
    return prediction