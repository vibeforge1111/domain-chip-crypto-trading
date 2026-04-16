def guard(features: dict, prediction: str) -> str:
    """Filter signals with disagreement between VWAP deviation and momentum."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Skip if momentum and VWAP position strongly disagree
    if momentum > 0.2 and vwap_dev < -0.005:
        return "skip"
    if momentum < -0.2 and vwap_dev > 0.005:
        return "skip"
    
    return prediction