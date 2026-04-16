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
    
    # Skip longs when overbought on both BB and Stochastic
    if prediction == "long" and bb_pct_b > 0.88 and stoch_k > 82:
        return "skip"
    
    # Skip shorts when oversold on both BB and Stochastic
    if prediction == "short" and bb_pct_b < 0.12 and stoch_k < 18:
        return "skip"
    
    # Skip if extreme divergence between BB position and Stochastic
    if abs(bb_pct_b - 0.5) > 0.35 and abs(stoch_k - 50) > 30:
        return "skip"
    
    return prediction