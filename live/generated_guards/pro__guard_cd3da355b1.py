def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Filter trades too close to VWAP (no edge)
    if prediction == "long" and vwap_dev < 0.005:
        return "skip"
    if prediction == "short" and vwap_dev > -0.005:
        return "skip"
    
    # Additional filter: reject overextended entries using 2h RSI
    rsi_2h = features.get('rsi_2h', 50)
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction