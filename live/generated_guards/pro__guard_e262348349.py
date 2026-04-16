def guard(features: dict, prediction: str) -> str:
    """Filter trades against volume flow direction using OBV slope."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV slope is negative (distribution/weak volume)
    if prediction == "long" and obv_slope < 0:
        return "skip"
    
    # Skip shorts when OBV slope is positive (accumulation/strong volume)
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    return prediction