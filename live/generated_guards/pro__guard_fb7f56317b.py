def guard(features: dict, prediction: str) -> str:
    """Filter trades to high-confidence BB extremes (<0.05 or >0.95)."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    if prediction == "long" and bb_pct_b >= 0.05:
        return "skip"
    if prediction == "short" and bb_pct_b <= 0.95:
        return "skip"
    return prediction