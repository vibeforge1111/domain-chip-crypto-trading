def guard(features: dict, prediction: str) -> str:
    """Guard against trades with unfavorable wick imbalance.

    For longs: reject if upper wick dominates (resistance pressure)
    For shorts: reject if lower wick dominates (support pressure)
    """
    if prediction == "skip":
        return prediction
    
    upper = features.get("upper_wick_ratio", 0)
    lower = features.get("lower_wick_ratio", 0)
    body = features.get("body_ratio", 0)
    
    # Reject if candle has very small body (indecision) with wick imbalance
    if body < 0.2 and abs(upper - lower) > 0.15:
        return "skip"
    
    # Wick dominance check for longs
    if prediction == "long" and upper > lower * 1.4:
        return "skip"
    
    # Wick dominance check for shorts
    if prediction == "short" and lower > upper * 1.4:
        return "skip"
    
    return prediction