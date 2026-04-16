def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP deviation and momentum score disagreement."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Skip if strong disagreement between VWAP position and momentum
    # Price well below VWAP but positive momentum (potential reversal setup)
    if vwap_dev < -0.01 and momentum > 0.2:
        return "skip"
    # Price well above VWAP but negative momentum (momentum fade)
    if vwap_dev > 0.01 and momentum < -0.2:
        return "skip"
    
    return prediction