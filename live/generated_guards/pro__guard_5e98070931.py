def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    if prediction == "long":
        if vwap_dev < 0 and momentum < 0:
            return "skip"
    elif prediction == "short":
        if vwap_dev > 0 and momentum > 0:
            return "skip"
    
    return prediction