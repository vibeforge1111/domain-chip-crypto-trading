def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Strong disagreement: price far above VWAP but momentum bearish
    if vwap_dev > 0.008 and momentum < -0.25:
        return "skip"
    # Strong disagreement: price far below VWAP but momentum bullish
    if vwap_dev < -0.008 and momentum > 0.25:
        return "skip"
    
    return prediction