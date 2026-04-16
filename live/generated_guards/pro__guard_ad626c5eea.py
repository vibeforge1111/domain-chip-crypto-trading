def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using OBV slope."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs if OBV is declining (selling pressure outweighs buying)
    if prediction == "long" and obv_slope < -0.3:
        return "skip"
    
    # Skip shorts if OBV is rising (buying pressure outweighs selling)
    if prediction == "short" and obv_slope > 0.3:
        return "skip"
    
    return prediction