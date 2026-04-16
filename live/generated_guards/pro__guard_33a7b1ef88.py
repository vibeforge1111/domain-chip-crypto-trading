def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Skip longs when overbought: price at upper BB AND stochastics confirm
    if prediction == "long" and bb_pct_b > 0.88 and stoch_k > 75 and stoch_d > 75:
        return "skip"
    
    # Skip shorts when oversold: price at lower BB AND stochastics confirm
    if prediction == "short" and bb_pct_b < 0.12 and stoch_k < 25 and stoch_d < 25:
        return "skip"
    
    return prediction