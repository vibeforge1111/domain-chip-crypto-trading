def guard(features: dict, prediction: str) -> str:
    """Skip on extreme volatility regimes (too quiet or too wild)."""
    atr_ratio = features.get("atr_ratio", 1.0)
    if atr_ratio < 0.7 or atr_ratio > 1.6:
        return "skip"
    return prediction