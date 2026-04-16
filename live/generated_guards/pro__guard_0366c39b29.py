def guard(features: dict, prediction: str) -> str:
    """Filter trades with vwap_deviation and momentum_score disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Strong disagreement: price above VWAP but momentum bearish
    if vwap_dev > 0.015 and momentum < -0.2:
        return "skip"
    # Strong disagreement: price below VWAP but momentum bullish
    if vwap_dev < -0.015 and momentum > 0.2:
        return "skip"
    
    return prediction