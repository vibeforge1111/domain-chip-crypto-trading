def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Disagreement: price significantly below VWAP but momentum positive, or vice versa
    disagreement = (vwap_dev < -0.003 and momentum > 0.25) or (vwap_dev > 0.003 and momentum < -0.25)
    
    if disagreement:
        return "skip"
    
    return prediction