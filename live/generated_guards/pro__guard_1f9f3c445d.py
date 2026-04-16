def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    macd = features.get("macd_histogram", 0)
    rsi = features.get("rsi_14", 50)
    stoch = features.get("stoch_k", 50)
    
    if prediction == "long" and macd < 0 and rsi > 65:
        return "skip"
    if prediction == "short" and macd > 0 and rsi < 35:
        return "skip"
    
    return prediction