def guard(features: dict, prediction: str) -> str:
    """Filter trades against MACD momentum direction (deceleration detection)."""
    macd = features.get('macd_histogram', 0)
    # Skip long entries when MACD histogram is bearish (momentum deceleration)
    if prediction == "long" and macd < -0.00005:
        return "skip"
    # Skip short entries when MACD histogram is bullish (momentum deceleration)
    if prediction == "short" and macd > 0.00005:
        return "skip"
    return prediction