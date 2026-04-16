def guard(features: dict, prediction: str) -> str:
    """Filter trades against volume flow direction using OBV slope."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip long trades when OBV is declining (distribution/selling pressure)
    if prediction == "long" and obv_slope < -0.005:
        return "skip"
    
    # Skip short trades when OBV is rising (accumulation/buying pressure)
    if prediction == "short" and obv_slope > 0.005:
        return "skip"
    
    return prediction