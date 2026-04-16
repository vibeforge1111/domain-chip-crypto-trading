def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if price above VWAP but momentum is bearish
    if vwap_dev > 0.015 and momentum < -0.25:
        return "skip"
    
    # Skip if price below VWAP but momentum is bullish
    if vwap_dev < -0.015 and momentum > 0.25:
        return "skip"
    
    return prediction