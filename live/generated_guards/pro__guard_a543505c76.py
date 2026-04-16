def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Reject if price above VWAP but momentum bearish, or vice versa
    if (vwap_dev > 0.003 and momentum < -0.05) or (vwap_dev < -0.003 and momentum > 0.05):
        return "skip"
    
    return prediction