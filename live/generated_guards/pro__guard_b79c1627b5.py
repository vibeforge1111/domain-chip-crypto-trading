def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    obv_slope = features.get("obv_slope", 0)
    vwap_deviation = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long" and obv_slope < 0.1:
        return "skip"
    
    if prediction == "short" and obv_slope > -0.1:
        return "skip"
    
    if prediction == "long" and vwap_deviation < -0.01 and rsi_2h < 45:
        return "skip"
    
    return prediction