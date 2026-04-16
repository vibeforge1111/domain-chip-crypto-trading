def guard(features: dict, prediction: str) -> str:
    """Guard function using obv_slope to filter trades against volume flow."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs if OBV is declining (volume flow against long position)
    if prediction == "long" and obv_slope < -0.01:
        return "skip"
    
    # Skip shorts if OBV is rising (volume flow against short position)
    if prediction == "short" and obv_slope > 0.01:
        return "skip"
    
    return prediction