def guard(features: dict, prediction: str) -> str:
    """Reject trades where VWAP deviation and momentum score disagree."""
    vwap_deviation = features.get("vwap_deviation", 0)
    momentum_score = features.get("momentum_score", 0)
    
    # Skip if price above VWAP but momentum is negative
    if vwap_deviation > 0.01 and momentum_score < -0.15:
        return "skip"
    
    # Skip if price below VWAP but momentum is positive
    if vwap_deviation < -0.01 and momentum_score > 0.15:
        return "skip"
    
    return prediction