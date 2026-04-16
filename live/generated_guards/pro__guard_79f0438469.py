def guard(features: dict, prediction: str) -> str:
    """Filter trades with disagreement between VWAP deviation and momentum."""
    vwap_deviation = features.get('vwap_deviation', 0)
    momentum_score = features.get('momentum_score', 0)
    
    # Skip if momentum disagrees with VWAP position
    if vwap_deviation < -0.005 and momentum_score > 0.3:
        return "skip"
    if vwap_deviation > 0.005 and momentum_score < -0.3:
        return "skip"
    
    return prediction