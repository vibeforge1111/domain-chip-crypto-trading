def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = abs(features.get("vwap_deviation", 0))
    
    # Reject if too close to VWAP (no clear directional signal)
    if vwap_dev < 0.003:
        return "skip"
    
    return prediction