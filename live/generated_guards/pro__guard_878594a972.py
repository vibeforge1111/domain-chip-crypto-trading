def guard(features: dict, prediction: str) -> str:
    """Reject longs at upper BB and shorts at lower BB extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    if prediction == "long" and bb_pct_b > 0.95:
        return "skip"
    if prediction == "short" and bb_pct_b < 0.05:
        return "skip"
    
    return prediction