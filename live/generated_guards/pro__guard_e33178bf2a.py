def guard(features: dict, prediction: str) -> str:
    """Filters trades on weak/consolidation candles or wick-exhaustion patterns."""
    body_ratio = features.get("body_ratio", 0)
    upper_wick_ratio = features.get("upper_wick_ratio", 0)
    lower_wick_ratio = features.get("lower_wick_ratio", 0)
    range_pct = features.get("range_pct", 0)
    trend_strength = features.get("trend_strength", 0)
    
    # Skip if candle is a doji/consolidation (small body, small range)
    if body_ratio < 0.15 and range_pct < 0.5:
        return "skip"
    
    # Skip long trades with upper wick exhaustion (>60% upper wick, small body)
    if prediction == "long" and upper_wick_ratio > 0.6 and body_ratio < 0.3:
        return "skip"
    
    # Skip short trades with lower wick exhaustion (>60% lower wick, small body)
    if prediction == "short" and lower_wick_ratio > 0.6 and body_ratio < 0.3:
        return "skip"
    
    return prediction