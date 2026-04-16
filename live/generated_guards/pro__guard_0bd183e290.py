def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum is decelerating (negative macd_histogram)."""
    macd_histogram = features.get('macd_histogram', 0)
    if macd_histogram < -0.0005:
        return "skip"
    return prediction