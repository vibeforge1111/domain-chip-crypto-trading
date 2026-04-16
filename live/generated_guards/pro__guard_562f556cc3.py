def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Check for significant disagreement between price position and momentum
    # Positive vwap_dev = price above VWAP, positive momentum = bullish
    # Negative vwap_dev = price below VWAP, negative momentum = bearish
    in_disagreement = (vwap_dev > 0.005 and momentum < -0.1) or \
                      (vwap_dev < -0.005 and momentum > 0.1)
    
    if in_disagreement and prediction in ("long", "short"):
        return "skip"
    
    return prediction