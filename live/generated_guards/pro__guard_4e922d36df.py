def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree significantly."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Check for strong disagreement: momentum direction vs VWAP position
    if momentum > 0.4 and vwap_dev < -0.01:
        return "skip"
    if momentum < -0.4 and vwap_dev > 0.01:
        return "skip"
    
    # Combined disagreement score (negative product = disagreement)
    disagreement = vwap_dev * momentum
    if disagreement < -0.003:
        return "skip"
    
    return prediction