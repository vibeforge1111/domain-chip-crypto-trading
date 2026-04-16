def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Skip longs when volume flow (OBV) is against the trade direction
    if prediction == "long" and obv_slope < 0:
        return "skip"
    
    # Skip shorts when volume flow (OBV) is against the trade direction
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    # Additional alignment check: price should be above VWAP for longs
    if prediction == "long" and vwap_deviation < 0:
        return "skip"
    
    # Additional alignment check: price should be below VWAP for shorts
    if prediction == "short" and vwap_deviation > 0:
        return "skip"
    
    return prediction