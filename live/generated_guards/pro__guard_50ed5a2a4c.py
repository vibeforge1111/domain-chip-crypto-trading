def guard(features: dict, prediction: str) -> str:
    """Filter trades on momentum deceleration via MACD histogram."""
    hist = features.get('macd_histogram', 0)
    if prediction == "long" and hist < 0:
        return "skip"
    if prediction == "short" and hist > 0:
        return "skip"
    return prediction