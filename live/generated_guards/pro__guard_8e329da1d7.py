def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like vwap_deviation, bb_pct_b, stoch_k, stoch_d, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    vwap_dev = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    macd_hist = features.get("macd_histogram", 0)
    
    # Reject trades too close to VWAP (no edge at fair value)
    if abs(vwap_dev) < 0.002:
        return "skip"
    
    # Reject overbought/oversold extremes on 2h context
    if rsi_2h > 80 or rsi_2h < 20:
        return "skip"
    
    # Reject conflicting momentum on 2h vs 15m
    if stoch_k > 80 and macd_hist < 0:
        return "skip"
    
    if stoch_k < 20 and macd_hist > 0:
        return "skip"
    
    return prediction