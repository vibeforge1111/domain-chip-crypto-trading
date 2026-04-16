def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP and momentum_score disagree."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # VWAP position and momentum must agree with prediction
    if prediction == "long":
        if vwap_dev < -0.002 and momentum < 0:
            return "skip"
    elif prediction == "short":
        if vwap_dev > 0.002 and momentum > 0:
            return "skip"
    
    return prediction