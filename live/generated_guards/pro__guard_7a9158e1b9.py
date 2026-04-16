def guard(features: dict, prediction: str) -> str:
    """Filter trades based on wick-body structure and momentum alignment."""
    if prediction == "skip":
        return prediction
    
    # Reject longs with dominant upper wick (resistance rejection)
    if prediction == "long" and features["upper_wick_ratio"] > 0.4:
        if features["upper_wick_ratio"] > features["body_ratio"] * 1.5:
            return "skip"
    
    # Reject shorts with dominant lower wick (support bounce)
    if prediction == "short" and features["lower_wick_ratio"] > 0.4:
        if features["lower_wick_ratio"] > features["body_ratio"] * 1.5:
            return "skip"
    
    # Reject when momentum contradicts trend direction
    if features["trend_strength"] > 0.5:
        if prediction == "long" and features["momentum_score"] < -0.2:
            return "skip"
        if prediction == "short" and features["momentum_score"] > 0.2:
            return "skip"
    
    return prediction