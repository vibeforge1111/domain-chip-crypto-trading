def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is decelerating (negative MACD histogram)."""
    if features.get('macd_histogram', 0) < 0:
        return "skip"
    return prediction