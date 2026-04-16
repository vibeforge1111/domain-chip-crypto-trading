def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    # Filter trades too close to VWAP (fair value zone - no edge)
    vwap_dev = abs(features.get('vwap_deviation', 0))
    if vwap_dev < 0.002:
        return "skip"
    return prediction