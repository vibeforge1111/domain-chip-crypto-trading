def guard(features: dict, prediction: str) -> str:
    rsi_2h = features.get('rsi_2h', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    if abs(vwap_dev) > 0.03:
        return "skip"
    
    return prediction