def guard(features: dict, prediction: str) -> str:
    """Reject trades when MACD histogram shows momentum deceleration."""
    if features.get('macd_histogram', 0) < 0.0005:
        return "skip"
    return prediction