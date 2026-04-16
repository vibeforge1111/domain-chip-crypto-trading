def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using OBV slope."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV declining (volume flowing out)
    if prediction == "long" and obv_slope < 0:
        return "skip"
    
    # Skip shorts when OBV rising (volume flowing in)
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    return prediction