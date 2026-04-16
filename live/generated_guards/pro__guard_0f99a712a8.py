def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction detected by OBV slope."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip long positions when OBV is declining (distribution)
    if prediction == "long" and obv_slope < -0.01:
        return "skip"
    
    # Skip short positions when OBV is rising (accumulation)
    if prediction == "short" and obv_slope > 0.01:
        return "skip"
    
    return prediction