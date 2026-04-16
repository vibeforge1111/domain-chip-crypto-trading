def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip long trades when OBV slope is negative (volume flow against longs)
    if prediction == "long" and obv_slope < 0:
        return "skip"
    
    # Skip short trades when OBV slope is positive (volume flow against shorts)
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    return prediction