def guard(features: dict, prediction: str) -> str:
    """Reject trades where wick structure contradicts prediction direction."""
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    bb_pos = features.get("bb_position", 0.5)
    
    if prediction == "long" and upper_wick > 0.4:
        return "skip"
    if prediction == "short" and lower_wick > 0.4:
        return "skip"
    if prediction == "long" and bb_pos > 0.92:
        return "skip"
    if prediction == "short" and bb_pos < 0.08:
        return "skip"
    return prediction