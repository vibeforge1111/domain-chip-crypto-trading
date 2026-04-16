def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    threshold = 0.0005  # minimum slope indicating volume conviction
    
    # Skip if prediction contradicts OBV flow
    if obv_slope > threshold and prediction == "short":
        return "skip"
    if obv_slope < -threshold and prediction == "long":
        return "skip"
    
    return prediction