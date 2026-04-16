def guard(features: dict, prediction: str) -> str:
    """Filter trades when price is too close to VWAP (low conviction)."""
    vwap_dev = features.get('vwap_deviation', 0)
    volume_ratio = features.get('volume_ratio', 1)
    
    # Skip if too close to fair value AND low volume (consolidation)
    if abs(vwap_dev) < 0.002 and volume_ratio < 1.2:
        return "skip"
    return prediction