def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is decelerating (negative macd_histogram)."""
    if features.get('macd_histogram', 0) < -0.0003:
        return "skip"
    return prediction