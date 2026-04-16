def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    macd_histogram = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip if momentum is decelerating (negative macd_histogram)
    if macd_histogram < -0.0005:
        return "skip"
    
    # Skip if momentum decelerating AND overbought/oversold mismatch
    if prediction == "long" and macd_histogram < 0 and stoch_k > 80:
        return "skip"
    if prediction == "short" and macd_histogram < 0 and stoch_k < 20:
        return "skip"
    
    # Skip if 2h RSI contradicts direction with decelerating momentum
    if prediction == "long" and macd_histogram < 0 and rsi_2h > 70:
        return "skip"
    if prediction == "short" and macd_histogram < 0 and rsi_2h < 30:
        return "skip"
    
    return prediction