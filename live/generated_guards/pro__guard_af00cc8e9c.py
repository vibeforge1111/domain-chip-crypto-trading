def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.
    Uses bb_pct_b extremes as high-confidence entry zones.

    Args:
        features: Dict with keys like bb_pct_b, vwap_deviation, stoch_k, stoch_d, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # High-confidence entry zones: bb_pct_b at extremes
    is_extreme_low = bb_pct_b < 0.05
    is_extreme_high = bb_pct_b > 0.95
    
    # Only allow longs at extreme low, shorts at extreme high
    if prediction == "long" and not is_extreme_low:
        return "skip"
    if prediction == "short" and not is_extreme_high:
        return "skip"
    
    # Secondary confirmation: stochastic alignment
    if prediction == "long" and stoch_k > 70:
        return "skip"
    if prediction == "short" and stoch_k < 30:
        return "skip"
    
    return prediction