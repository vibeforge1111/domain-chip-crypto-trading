def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum is decelerating (weak macd_histogram)."""
    hist = features.get('macd_histogram', 0)
    if abs(hist) < 0.00015 and prediction in ('long', 'short'):
        return "skip"
    return prediction