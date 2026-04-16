def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Only allow long at bottom extremes, short at top extremes
    if prediction == "long" and bb_pct_b > 0.95:
        return "skip"
    if prediction == "short" and bb_pct_b < 0.05:
        return "skip"
    
    return prediction