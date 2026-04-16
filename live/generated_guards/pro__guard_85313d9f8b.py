def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP deviation and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if price above VWAP but momentum strongly negative
    if vwap_dev > 0.015 and momentum < -0.4:
        return "skip"
    
    # Skip if price below VWAP but momentum strongly positive
    if vwap_dev < -0.015 and momentum > 0.4:
        return "skip"
    
    return prediction