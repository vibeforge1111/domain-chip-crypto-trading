def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, vwap_deviation, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip long signals when both indicators show extreme oversold
    if prediction == "long" and bb_pct < 0.15 and stoch_k < 20 and stoch_d < 20:
        return "skip"
    
    # Skip short signals when both indicators show extreme overbought
    if prediction == "short" and bb_pct > 0.85 and stoch_k > 80 and stoch_d > 80:
        return "skip"
    
    return prediction