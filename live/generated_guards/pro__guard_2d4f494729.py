def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if price far above VWAP but momentum contradicts (weak/negative)
    if vwap_dev > 0.012 and momentum < 0:
        return "skip"
    # Skip if price far below VWAP but momentum contradicts (weak/positive)
    if vwap_dev < -0.012 and momentum > 0:
        return "skip"
    
    return prediction