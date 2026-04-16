def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like upper_wick_ratio, lower_wick_ratio, body_ratio, range_pct, volume_ratio, atr_ratio, rsi_14, ema_slope
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Only allow trades at extreme BB positions
    if bb_pct_b < 0.05:
        # Lower band extreme - validate for long
        if prediction == "long" and vwap_deviation < 0 and stoch_k < 25 and stoch_d < 25 and rsi_2h < 35:
            return prediction
        return "skip"
    elif bb_pct_b > 0.95:
        # Upper band extreme - validate for short
        if prediction == "short" and vwap_deviation > 0 and stoch_k > 75 and stoch_d > 75 and rsi_2h > 65:
            return prediction
        return "skip"
    
    return "skip"