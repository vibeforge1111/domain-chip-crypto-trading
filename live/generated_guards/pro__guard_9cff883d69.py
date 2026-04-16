def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is decelerating (weak/negative macd_histogram)."""
    if features.get('macd_histogram', 0) < 0.0001:
        return "skip"
    return prediction