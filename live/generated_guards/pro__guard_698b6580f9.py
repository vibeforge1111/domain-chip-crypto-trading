def guard(features: dict, prediction: str) -> str:
    """Reject trades when not at Bollinger Band extremes for high-confidence entries."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # High-confidence entries only at extremes
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # Reject if direction doesn't match band extreme
    if prediction == "long" and bb_pct_b > 0.5:
        return "skip"
    if prediction == "short" and bb_pct_b < 0.5:
        return "skip"
    
    return prediction