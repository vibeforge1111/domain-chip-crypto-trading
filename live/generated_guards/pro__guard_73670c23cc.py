def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Reject longs when price significantly below VWAP (negative deviation)
    if prediction == "long" and vwap_dev < -0.008:
        return "skip"
    
    # Reject shorts when price significantly above VWAP (positive deviation)
    if prediction == "short" and vwap_dev > 0.008:
        return "skip"
    
    # Additional filter: reject when momentum disagrees with prediction
    if prediction == "long" and momentum < -0.3:
        return "skip"
    if prediction == "short" and momentum > 0.3:
        return "skip"
    
    return prediction