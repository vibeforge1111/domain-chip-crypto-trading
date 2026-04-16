def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    obv_slope = features.get("obv_slope", 0)
    
    # Skip trades against OBV flow direction
    if prediction == "long" and obv_slope < -0.01:
        return "skip"
    if prediction == "short" and obv_slope > 0.01:
        return "skip"
    
    return prediction