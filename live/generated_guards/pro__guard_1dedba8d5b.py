def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    
    if prediction == "long":
        if rsi_2h > 72 or stoch_k > 85:
            return "skip"
    elif prediction == "short":
        if rsi_2h < 28 or stoch_k < 15:
            return "skip"
    
    return prediction