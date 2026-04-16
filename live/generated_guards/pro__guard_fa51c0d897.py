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
    
    # Detect momentum deceleration using macd_histogram
    # For longs: skip if momentum has turned negative or stoch overbought
    if prediction == "long" and (macd_histogram < -0.0001 or stoch_k > 80):
        return "skip"
    
    # For shorts: skip if momentum has turned positive or stoch oversold
    if prediction == "short" and (macd_histogram > 0.0001 or stoch_k < 20):
        return "skip"
    
    return prediction