def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs when OBV slope is negative (distribution against longs)
    if prediction == "long" and obv_slope < 0:
        return "skip"
    
    # Skip shorts when OBV slope is positive (accumulation against shorts)
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    return prediction