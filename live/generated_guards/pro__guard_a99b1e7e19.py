def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    macd_histogram = features.get("macd_histogram", 0)
    vwap_deviation = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip long trades when MACD histogram is negative (momentum decelerating)
    if prediction == "long" and macd_histogram < -0.0001:
        return "skip"
    
    # Skip short trades when MACD histogram is positive (momentum accelerating against short)
    if prediction == "short" and macd_histogram > 0.0001:
        return "skip"
    
    # Additional filter: skip if price is far from VWAP in direction opposite to trade
    if prediction == "long" and vwap_deviation < -0.005:
        return "skip"
    if prediction == "short" and vwap_deviation > 0.005:
        return "skip"
    
    return prediction