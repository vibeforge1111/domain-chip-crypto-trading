def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Disagreement: price above VWAP but negative momentum
    if vwap_dev > 0.005 and momentum < -0.15:
        return "skip"
    
    # Disagreement: price below VWAP but positive momentum
    if vwap_dev < -0.005 and momentum > 0.15:
        return "skip"
    
    return prediction