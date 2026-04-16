def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum disagree."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    if prediction == "long":
        # Reject if price far below VWAP but momentum also weak/negative
        if vwap_dev < -0.003 and momentum < -0.2:
            return "skip"
    elif prediction == "short":
        # Reject if price far above VWAP but momentum also strong/positive
        if vwap_dev > 0.003 and momentum > 0.2:
            return "skip"
    
    return prediction