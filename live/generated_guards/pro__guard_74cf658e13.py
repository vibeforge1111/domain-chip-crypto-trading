def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    
    # Skip longs when OBV is declining (distribution against longs)
    if prediction == "long" and obv_slope < -0.3 and macd_histogram < 0:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation against shorts)
    if prediction == "short" and obv_slope > 0.3 and macd_histogram > 0:
        return "skip"
    
    return prediction