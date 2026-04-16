def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD histogram signals momentum deceleration."""
    if features.get('macd_histogram', 0) < 0:
        return "skip"
    return prediction