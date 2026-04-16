def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if momentum and VWAP position strongly disagree
    if (vwap_dev < -0.003 and momentum > 0.05) or (vwap_dev > 0.003 and momentum < -0.05):
        return "skip"
    
    return prediction