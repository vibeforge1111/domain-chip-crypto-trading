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
    
    # Reject long signals at overbought extremes (stoch_k > 80 AND bb_pct_b > 0.9)
    if prediction == "long" and stoch_k > 80 and bb_pct_b > 0.9:
        return "skip"
    
    # Reject short signals at oversold extremes (stoch_k < 20 AND bb_pct_b < 0.1)
    if prediction == "short" and stoch_k < 20 and bb_pct_b < 0.1:
        return "skip"
    
    # Reject counter-trend trades: long when 2h RSI is overbought
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    
    return prediction