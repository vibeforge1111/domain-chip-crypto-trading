def guard(features: dict, prediction: str) -> str:
    """Filter trades against OBV volume flow direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when OBV is declining (smart money distributing)
    if prediction == "long" and obv_slope < -0.05:
        return "skip"
    
    # Skip shorts when OBV is rising (smart money accumulating)
    if prediction == "short" and obv_slope > 0.05:
        return "skip"
    
    return prediction