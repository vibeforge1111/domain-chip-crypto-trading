def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, vwap_deviation, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Filter longs when overbought (bb upper + stoch overbought + above VWAP)
    if prediction == "long" and bb_pct_b > 0.90 and stoch_k > 80 and vwap_deviation > 0.005:
        return "skip"
    
    # Filter shorts when oversold (bb lower + stoch oversold + below VWAP)
    if prediction == "short" and bb_pct_b < 0.10 and stoch_k < 20 and vwap_deviation < -0.005:
        return "skip"
    
    return prediction