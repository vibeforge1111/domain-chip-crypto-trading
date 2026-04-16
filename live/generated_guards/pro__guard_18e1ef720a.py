def guard(features: dict, prediction: str) -> str:
    """Filter trades with vwap_deviation and momentum_score disagreement."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Skip if price below VWAP but momentum is positive (disagreement)
    if vwap_dev < -0.01 and momentum > 0.2:
        return "skip"
    
    # Skip if price above VWAP but momentum is negative (disagreement)
    if vwap_dev > 0.01 and momentum < -0.2:
        return "skip"
    
    return prediction