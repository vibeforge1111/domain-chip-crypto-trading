def guard(features: dict, prediction: str) -> str:
    """Filter trades with vwap_deviation and momentum_score disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Reject if price above VWAP but momentum is bearish, or price below VWAP but momentum is bullish
    disagreement = (vwap_dev > 0.01 and momentum < -0.3) or (vwap_dev < -0.01 and momentum > 0.3)
    
    if disagreement:
        return "skip"
    return prediction