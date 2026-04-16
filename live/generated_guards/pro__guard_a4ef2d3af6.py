def guard(features: dict, prediction: str) -> str:
    """Filter trades against the broader 2h trend.

    Args:
        features: Dict with market features
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    if prediction == "skip":
        return prediction

    rsi_2h = features.get("rsi_2h")
    if rsi_2h is None:
        return prediction

    # Align long entries with bullish 2h context (rsi_2h < 45 = weak/bearish)
    if prediction == "long" and rsi_2h < 45:
        return "skip"

    # Align short entries with bearish 2h context (rsi_2h > 55 = strong/bullish)
    if prediction == "short" and rsi_2h > 55:
        return "skip"

    return prediction