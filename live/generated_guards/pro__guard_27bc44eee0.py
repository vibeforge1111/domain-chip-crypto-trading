def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is decelerating (negative macd histogram)."""
    macd = features.get('macd_histogram', 0)
    if macd < -0.0003:
        return "skip"
    return prediction