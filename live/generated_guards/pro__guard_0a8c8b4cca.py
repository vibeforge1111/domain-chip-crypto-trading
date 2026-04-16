def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    
    # Skip longs if OBV slope negative (volume distribution/bearish flow)
    if prediction == "long" and obv_slope < -0.1:
        return "skip"
    
    # Skip shorts if OBV slope positive (volume accumulation/bullish flow)
    if prediction == "short" and obv_slope > 0.1:
        return "skip"
    
    return prediction