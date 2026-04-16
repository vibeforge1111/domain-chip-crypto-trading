def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    vwap_threshold = 0.005  # 0.5% significant deviation
    
    if prediction == "long":
        if vwap_dev > vwap_threshold and momentum < 0:
            return "skip"
    elif prediction == "short":
        if vwap_dev < -vwap_threshold and momentum > 0:
            return "skip"
    
    return prediction