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
    
    # Skip longs when both indicators show oversold extreme (bb_pct_b < 0.1 AND stoch_k < 20)
    if prediction == "long" and bb_pct_b < 0.1 and stoch_k < 20:
        return "skip"
    
    # Skip shorts when both indicators show overbought extreme (bb_pct_b > 0.9 AND stoch_k > 80)
    if prediction == "short" and bb_pct_b > 0.9 and stoch_k > 80:
        return "skip"
    
    return prediction