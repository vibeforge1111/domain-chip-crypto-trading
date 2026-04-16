def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_14 = features.get('rsi_14', 50)
    
    # Allow trades only in extreme BB zones with RSI confirmation
    if bb_pct_b < 0.05 and rsi_14 < 35:
        return prediction
    if bb_pct_b > 0.95 and rsi_14 > 65:
        return prediction
    
    return "skip"