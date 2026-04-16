def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Only allow entries in extreme BB zones (<0.05 or >0.95)
    if bb_pct_b > 0.05 and bb_pct_b < 0.95:
        return "skip"
    
    # Additional confirmation: align with stochastic
    stoch_k = features.get("stoch_k", 50)
    if prediction == "long" and stoch_k > 25:
        return "skip"
    if prediction == "short" and stoch_k < 75:
        return "skip"
    
    return prediction