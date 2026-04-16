def guard(features: dict, prediction: str) -> str:
    """Reject trades with conflicting wick-momentum signals or weak momentum."""
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    momentum = features.get("momentum_score", 0.5)
    volume = features.get("volume_ratio", 1)
    
    # Reject if wick contradicts prediction direction (rejection pattern)
    if prediction == "long" and upper_wick > 0.35:
        return "skip"
    if prediction == "short" and lower_wick > 0.35:
        return "skip"
    
    # Reject low momentum trades with elevated volume (exhaustion risk)
    if momentum < 0.35 and volume > 1.2:
        return "skip"
    
    return prediction