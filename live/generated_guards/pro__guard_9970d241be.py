def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP position and momentum disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Disagreement: price above VWAP but momentum is negative
    if vwap_dev > 0.005 and momentum < -0.15:
        return "skip"
    # Disagreement: price below VWAP but momentum is positive
    if vwap_dev < -0.005 and momentum > 0.15:
        return "skip"
    
    return prediction