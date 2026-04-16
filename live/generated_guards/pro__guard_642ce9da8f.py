def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is decelerating (macd near zero)."""
    macd = features.get('macd_histogram', 0)
    if abs(macd) < 0.00015:  # Near zero = momentum losing strength
        return "skip"
    return prediction