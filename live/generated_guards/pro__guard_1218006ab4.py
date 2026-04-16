def guard(features: dict, prediction: str) -> str:
    momentum = features.get("momentum_score", 0)
    vwap_dev = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        if momentum < -0.1:
            return "skip"
        if vwap_dev > 0.015 and rsi_2h > 70:
            return "skip"
    elif prediction == "short":
        if momentum > 0.1:
            return "skip"
        if vwap_dev < -0.015 and rsi_2h < 30:
            return "skip"
    
    return prediction