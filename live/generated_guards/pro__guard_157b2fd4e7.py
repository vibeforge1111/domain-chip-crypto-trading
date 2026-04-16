def guard(features: dict, prediction: str) -> str:
    """Filter trades where high volume meets large wick - potential exhaustion move."""
    volume = features.get("volume_ratio", 1.0)
    upper_wick = features.get("upper_wick_ratio", 0.0)
    lower_wick = features.get("lower_wick_ratio", 0.0)
    body_ratio = features.get("body_ratio", 0.5)
    
    # Skip if high volume + dominant wick (exhaustion signal)
    if volume > 1.4 and body_ratio < 0.4:
        return "skip"
    
    # Additional filter: large opposing wick during momentum
    if prediction == "long" and upper_wick > 0.5 and volume > 1.2:
        return "skip"
    if prediction == "short" and lower_wick > 0.5 and volume > 1.2:
        return "skip"
    
    return prediction