def guard(features: dict, prediction: str) -> str:
    """Reject signals when candle shows rejection (large wick) with weak momentum."""
    if prediction == "skip":
        return prediction
    
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    body = features.get("body_ratio", 1)
    momentum = features.get("momentum_score", 0.5)
    
    # Longs: skip if upper wick dominates AND momentum is weak
    if prediction == "long" and upper_wick > 0.3 and momentum < 0.45:
        return "skip"
    
    # Shorts: skip if lower wick dominates AND momentum is weak
    if prediction == "short" and lower_wick > 0.3 and momentum < 0.45:
        return "skip"
    
    return prediction