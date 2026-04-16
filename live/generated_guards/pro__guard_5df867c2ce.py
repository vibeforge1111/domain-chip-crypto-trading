def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Disagreement: price far below VWAP but momentum is bullish
    if vwap_dev < -0.015 and momentum > 0.25:
        return "skip"
    
    # Disagreement: price far above VWAP but momentum is bearish
    if vwap_dev > 0.015 and momentum < -0.25:
        return "skip"
    
    return prediction