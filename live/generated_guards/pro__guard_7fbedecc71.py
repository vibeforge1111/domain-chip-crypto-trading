def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Reject trades too close to fair value (small VWAP deviation)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Reject if stochastics show exhaustion in direction of trade
    if prediction == "long" and features.get("stoch_k", 50) > 85:
        return "skip"
    if prediction == "short" and features.get("stoch_k", 50) < 15:
        return "skip"
    
    return prediction