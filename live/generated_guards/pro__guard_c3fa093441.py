def guard(features: dict, prediction: str) -> str:
    """Filter trades against volume flow using OBV slope."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when volume flowing out, skip shorts when accumulating
    if prediction == "long" and obv_slope < -0.5:
        return "skip"
    if prediction == "short" and obv_slope > 0.5:
        return "skip"
    
    return prediction