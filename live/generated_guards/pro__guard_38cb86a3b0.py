def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like vwap_deviation, bb_pct_b, stoch_k, stoch_d, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    vwap_dev = abs(features.get("vwap_deviation", 0))
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip if price too close to VWAP (no edge)
    if vwap_dev < 0.003:
        return "skip"
    
    # Skip if stochastic is neutral (not overbought/oversold)
    if 30 < stoch_k < 70 and 30 < stoch_d < 70:
        return "skip"
    
    return prediction