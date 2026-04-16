def guard(features: dict, prediction: str) -> str:
    """Skip trades where VWAP deviation contradicts momentum direction."""
    vwap_deviation = features.get('vwap_deviation', 0)
    momentum_score = features.get('momentum_score', 0)
    
    # Disagreement: price extended from VWAP but momentum opposes direction
    if vwap_deviation > 0.015 and momentum_score < -0.1:
        return "skip"
    if vwap_deviation < -0.015 and momentum_score > 0.1:
        return "skip"
    
    return prediction