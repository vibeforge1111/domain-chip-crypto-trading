def guard(features: dict, prediction: str) -> str:
    """Reject trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Significant disagreement: price far from VWAP but momentum contradicts direction
    if vwap_dev < -0.015 and momentum > 0.35:
        return "skip"
    if vwap_dev > 0.015 and momentum < -0.35:
        return "skip"
    
    # Additional check: long above VWAP with negative momentum, or short below with positive
    if prediction == "long" and vwap_dev > 0.02 and momentum < 0:
        return "skip"
    if prediction == "short" and vwap_dev < -0.02 and momentum > 0:
        return "skip"
    
    return prediction