def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using OBV slope."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV is declining (distribution against long)
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation against short)
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    return prediction