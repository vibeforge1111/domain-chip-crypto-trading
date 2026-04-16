def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    vwap_dev = features.get("vwap_deviation", 0)
    bb_pos = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip if price too close to VWAP (within 0.2% of fair value)
    if abs(vwap_dev) < 0.002:
        return "skip"
    
    # Skip long if too close to VWAP and at lower band
    if prediction == "long" and abs(vwap_dev) < 0.005 and bb_pos < 0.2:
        return "skip"
    
    # Skip short if too close to VWAP and at upper band
    if prediction == "short" and abs(vwap_dev) < 0.005 and bb_pos > 0.8:
        return "skip"
    
    return prediction