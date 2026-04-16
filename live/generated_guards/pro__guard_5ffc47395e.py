def guard(features: dict, prediction: str) -> str:
    vwap_deviation = features.get("vwap_deviation", 0)
    momentum_score = features.get("momentum_score", 0)
    
    if prediction == "long":
        # Skip long if price below VWAP AND weak/negative momentum
        if vwap_deviation < -0.005 and momentum_score < 0.1:
            return "skip"
    elif prediction == "short":
        # Skip short if price above VWAP AND weak/positive momentum
        if vwap_deviation > 0.005 and momentum_score > -0.1:
            return "skip"
    
    return prediction