def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    macd_histogram = features.get("macd_histogram", 0)
    
    # Detect momentum deceleration: reject longs when macd_histogram is negative
    if prediction == "long" and macd_histogram < -0.0001:
        return "skip"
    
    # Detect momentum deceleration: reject shorts when macd_histogram is positive
    if prediction == "short" and macd_histogram > 0.0001:
        return "skip"
    
    return prediction