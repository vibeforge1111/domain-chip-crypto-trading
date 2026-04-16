def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    rsi_2h = features.get("rsi_2h", 50)
    
    # Reject long signals when 2h RSI is deeply oversold (counter-trend)
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    
    # Reject short signals when 2h RSI is deeply overbought (counter-trend)
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    
    return prediction