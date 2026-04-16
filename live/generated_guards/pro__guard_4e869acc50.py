def guard(features: dict, prediction: str) -> str:
    """Filter trades using BB extreme zones for high-confidence entries."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    if prediction == "long" and bb_pct_b < 0.05:
        return prediction
    if prediction == "short" and bb_pct_b > 0.95:
        return prediction
    
    return "skip"