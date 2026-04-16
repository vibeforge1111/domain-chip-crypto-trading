def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # OBV positive = accumulation, favor longs
    # OBV negative = distribution, favor shorts
    if prediction == "long" and obv_slope < -0.3:
        return "skip"
    if prediction == "short" and obv_slope > 0.3:
        return "skip"
    
    return prediction