def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD histogram indicates momentum against position direction."""
    macd = features.get('macd_histogram', 0)
    # Momentum deceleration: MACD histogram opposes trade direction
    if prediction == "long" and macd < 0:
        return "skip"
    if prediction == "short" and macd > 0:
        return "skip"
    return prediction