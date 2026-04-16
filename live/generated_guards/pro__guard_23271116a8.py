def guard(features: dict, prediction: str) -> str:
    """BB extreme zone guard - only allow signals at Bollinger Band extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    # High-confidence long entries only at lower BB extreme
    if prediction == "long" and bb_pct_b >= 0.05:
        return "skip"
    # High-confidence short entries only at upper BB extreme
    if prediction == "short" and bb_pct_b <= 0.95:
        return "skip"
    return prediction