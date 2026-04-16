def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP) with weak momentum."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if price is within 0.3% of VWAP AND momentum is weak
    if abs(vwap_dev) < 0.003 and momentum < 0.4:
        return "skip"
    return prediction