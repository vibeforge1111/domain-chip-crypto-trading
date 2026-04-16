def guard(features: dict, prediction: str) -> str:
    """Reject trades where candle structure contradicts momentum direction."""
    if prediction == "skip":
        return prediction
    
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    body_ratio = features.get("body_ratio", 0)
    momentum = features.get("momentum_score", 0)
    
    # Skip weak candles (low body ratio)
    if body_ratio < 0.15:
        return "skip"
    
    # For longs: want bullish structure + positive momentum
    if prediction == "long":
        if upper_wick > 0.35 and lower_wick < 0.1:  # rejection from above
            return "skip"
        if momentum < -0.05:  # momentum contradicts direction
            return "skip"
    
    # For shorts: want bearish structure + negative momentum
    if prediction == "short":
        if lower_wick > 0.35 and upper_wick < 0.1:  # rejection from below
            return "skip"
        if momentum > 0.05:  # momentum contradicts direction
            return "skip"
    
    return prediction