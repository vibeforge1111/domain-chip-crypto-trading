def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV is declining (distribution, not accumulation)
    if prediction == "long" and obv_slope < -0.005:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation, not distribution)
    if prediction == "short" and obv_slope > 0.005:
        return "skip"
    
    return prediction