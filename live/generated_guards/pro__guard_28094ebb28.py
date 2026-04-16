def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    # Reject longs when MACD histogram is negative (momentum weakening)
    if prediction == "long" and features.get("macd_histogram", 0) < 0:
        return "skip"
    # Reject shorts when MACD histogram is positive (momentum strengthening)
    if prediction == "short" and features.get("macd_histogram", 0) > 0:
        return "skip"
    return prediction