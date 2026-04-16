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
    rsi_2h = features.get("rsi_2h", 50)
    
    overbought = bb_pct_b > 0.88 and stoch_k > 80
    oversold = bb_pct_b < 0.12 and stoch_k < 20
    
    if prediction == "long" and oversold:
        return "skip"
    if prediction == "short" and overbought:
        return "skip"
    
    return prediction