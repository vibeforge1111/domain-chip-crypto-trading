def guard(features: dict, prediction: str) -> str:
    """Filter trades when MACD histogram shows momentum deceleration against direction."""
    macd = features.get('macd_histogram', 0)
    # Skip long if histogram is negative (bearish momentum), skip short if positive (bullish)
    if prediction == "long" and macd < 0:
        return "skip"
    if prediction == "short" and macd > 0:
        return "skip"
    return prediction