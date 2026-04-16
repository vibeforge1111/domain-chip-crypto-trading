def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    obv_slope = features.get("obv_slope", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip longs when OBV slope is negative (volume flowing against)
    if prediction == "long" and obv_slope < 0:
        return "skip"
    
    # Skip shorts when OBV slope is positive (volume flowing against)
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    # Additional confirmation: skip overbought longs and oversold shorts
    if prediction == "long" and stoch_k > 80:
        return "skip"
    if prediction == "short" and stoch_k < 20:
        return "skip"
    
    return prediction