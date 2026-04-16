def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree significantly."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if price below VWAP but momentum strongly bullish
    if vwap_dev < -0.003 and momentum > 0.4:
        return "skip"
    
    # Skip if price above VWAP but momentum strongly bearish
    if vwap_dev > 0.003 and momentum < -0.4:
        return "skip"
    
    return prediction