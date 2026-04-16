def guard(features: dict, prediction: str) -> str:
    rsi_2h = features.get("rsi_2h", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Align with broader trend using 2h RSI
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    # Additional filter: entry should be on correct side of VWAP
    if prediction == "long" and vwap_dev < -0.005:
        return "skip"
    if prediction == "short" and vwap_dev > 0.005:
        return "skip"
    
    return prediction