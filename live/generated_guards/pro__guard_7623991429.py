def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Skip long when price at extreme upper band (likely to reverse down)
    if prediction == "long" and bb_pct_b > 0.95:
        return "skip"
    
    # Skip short when price at extreme lower band (likely to reverse up)
    if prediction == "short" and bb_pct_b < 0.05:
        return "skip"
    
    return prediction