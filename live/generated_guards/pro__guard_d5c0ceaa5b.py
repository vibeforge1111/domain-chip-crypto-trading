def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP and momentum disagreement."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Skip long if price below VWAP with negative momentum
    if prediction == "long" and vwap_dev < -0.005 and momentum < -0.1:
        return "skip"
    
    # Skip short if price above VWAP with positive momentum
    if prediction == "short" and vwap_dev > 0.005 and momentum > 0.1:
        return "skip"
    
    return prediction