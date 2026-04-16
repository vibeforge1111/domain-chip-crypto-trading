def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation disagrees with momentum_score."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Reject if momentum contradicts VWAP position
    if vwap_dev > 0.003 and momentum < -0.1:
        return "skip"
    if vwap_dev < -0.003 and momentum > 0.1:
        return "skip"
    
    return prediction