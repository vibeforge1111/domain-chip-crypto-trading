def guard(features: dict, prediction: str) -> str:
    """Skip if MACD histogram indicates momentum deceleration."""
    if features.get('macd_histogram', 0) < 0.0003:
        return "skip"
    if features.get('macd_histogram', 0) < 0:
        return "skip"
    return prediction