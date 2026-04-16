def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    # Filter: skip trades too close to VWAP (low conviction)
    if abs(vwap_dev) < 0.002:
        return "skip"
    
    if prediction == "long":
        if features.get("obv_slope", 0) <= 0:
            return "skip"
    
    if prediction == "short":
        if features.get("obv_slope", 0) >= 0:
            return "skip"
    
    rsi_2h = features.get("rsi_2h", 50)
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction