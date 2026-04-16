def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like obv_slope, macd_histogram, rsi_2h, bb_pct_b
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    if prediction == "long" and features.get("obv_slope", 0) < -0.01:
        return "skip"
    if prediction == "short" and features.get("obv_slope", 0) > 0.01:
        return "skip"
    return prediction