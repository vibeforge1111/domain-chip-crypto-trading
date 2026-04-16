def guard(features: dict, prediction: str) -> str:
    """Filter for BB extreme entries only."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    if bb_pct_b < 0.05 and prediction == "long":
        return prediction
    if bb_pct_b > 0.95 and prediction == "short":
        return prediction
    
    return "skip"