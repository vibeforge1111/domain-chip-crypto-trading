def guard(features: dict, prediction: str) -> str:
    """Filter trades when MACD histogram shows momentum deceleration against direction."""
    macd = features.get("macd_histogram", 0)
    # Skip longs if MACD histogram negative (upward momentum weakening)
    if prediction == "long" and macd < 0:
        return "skip"
    # Skip shorts if MACD histogram positive (downward momentum weakening)
    if prediction == "short" and macd > 0:
        return "skip"
    return prediction