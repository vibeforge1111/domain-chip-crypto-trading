def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like vwap_deviation, momentum_score, stoch_k, stoch_d, bb_pct_b, obv_slope, macd_histogram
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    macd_hist = features.get("macd_histogram", 0)
    
    # Skip if far from VWAP but momentum disagrees
    if vwap_dev > 0.01 and stoch_k < 25:
        return "skip"
    if vwap_dev < -0.01 and stoch_k > 75:
        return "skip"
    
    # Skip if MACD histogram contradicts VWAP deviation direction
    if vwap_dev > 0.008 and macd_hist < -0.0005:
        return "skip"
    if vwap_dev < -0.008 and macd_hist > 0.0005:
        return "skip"
    
    return prediction