def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if price significantly above VWAP but momentum is bearish
    if vwap_dev > 0.005 and momentum < 0:
        return "skip"
    
    # Skip if price significantly below VWAP but momentum is bullish
    if vwap_dev < -0.005 and momentum > 0:
        return "skip"
    
    return prediction