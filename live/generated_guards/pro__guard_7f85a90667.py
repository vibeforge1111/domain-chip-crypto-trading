def guard(features: dict, prediction: str) -> str:
    """Custom guard using Bollinger Band extremes for high-confidence entries."""
    bb = features.get("bb_pct_b", 0.5)
    
    # Skip longs unless at extreme lower band (bb_pct_b < 0.05)
    if prediction == "long" and bb >= 0.05:
        return "skip"
    # Skip shorts unless at extreme upper band (bb_pct_b > 0.95)
    if prediction == "short" and bb <= 0.95:
        return "skip"
    return prediction