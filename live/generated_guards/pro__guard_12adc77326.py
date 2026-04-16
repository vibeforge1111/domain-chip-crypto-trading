def guard(features: dict, prediction: str) -> str:
    """Skip trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Disagreement: price above VWAP but momentum bearish
    if vwap_dev > 0.003 and momentum < -0.15:
        return "skip"
    
    # Disagreement: price below VWAP but momentum bullish
    if vwap_dev < -0.003 and momentum > 0.15:
        return "skip"
    
    return prediction