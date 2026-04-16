def guard(features: dict, prediction: str) -> str:
    """Filter trades where candle wicks dominate the move (rejection signals)."""
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    body_ratio = features.get("body_ratio", 0.5)
    bb_width = features.get("bb_width", 1.0)
    
    # For long signals: large upper wick = selling rejection
    if prediction == "long" and upper_wick > 0.4:
        return "skip"
    
    # For short signals: large lower wick = buying rejection
    if prediction == "short" and lower_wick > 0.4:
        return "skip"
    
    # Skip if body is too small relative to wicks (choppy/inconclusive candle)
    if body_ratio < 0.3:
        return "skip"
    
    return prediction