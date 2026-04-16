def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    vwap_deviation = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Skip if price is too close to VWAP (within 0.5% of fair value)
    if abs(vwap_deviation) < 0.005:
        return "skip"
    
    # Skip if stochastic is in neutral zone (40-60) and near VWAP
    if 40 < stoch_k < 60 and 40 < stoch_d < 60:
        if abs(vwap_deviation) < 0.01:
            return "skip"
    
    return prediction