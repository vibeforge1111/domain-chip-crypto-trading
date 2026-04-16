def guard(features: dict, prediction: str) -> str:
    """Skip trades where VWAP deviation and momentum score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Strong disagreement: price above VWAP but momentum is bearish
    if vwap_dev > 0.004 and momentum < -0.25:
        return "skip"
    
    # Strong disagreement: price below VWAP but momentum is bullish
    if vwap_dev < -0.004 and momentum > 0.25:
        return "skip"
    
    return prediction