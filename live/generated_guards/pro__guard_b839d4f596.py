def guard(features: dict, prediction: str) -> str:
    """Skip trades where VWAP position and momentum disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Detect disagreement: price above VWAP but negative momentum, or vice versa
    disagreement = (vwap_dev > 0.005 and momentum < -0.3) or (vwap_dev < -0.005 and momentum > 0.3)
    
    if disagreement:
        return "skip"
    return prediction