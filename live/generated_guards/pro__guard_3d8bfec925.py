def guard(features: dict, prediction: str) -> str:
    """Guard: bb_pct_b extreme zones for high-confidence entries."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # High-confidence long: price near lower BB (< 5th percentile)
    if prediction == "long" and bb_pct_b < 0.05:
        return prediction
    
    # High-confidence short: price near upper BB (> 95th percentile)
    if prediction == "short" and bb_pct_b > 0.95:
        return prediction
    
    return "skip"