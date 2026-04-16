def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Filter when vwap_deviation and momentum_score disagree
    # Long needs both positive, short needs both negative
    if prediction == "long":
        if not (vwap_dev > 0 and momentum > 0):
            return "skip"
    elif prediction == "short":
        if not (vwap_dev < 0 and momentum < 0):
            return "skip"
    
    return prediction