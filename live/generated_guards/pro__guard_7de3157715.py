def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram indicates momentum deceleration."""
    if features.get('macd_histogram', 0) < -0.0003:
        return "skip"
    return prediction