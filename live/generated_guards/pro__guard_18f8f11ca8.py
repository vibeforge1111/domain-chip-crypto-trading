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
    stoch_d = features.get("stoch_d", 50)
    
    # Skip longs when both BB and Stochastic confirm overbought extreme
    if prediction == "long" and bb_pct_b > 0.90 and stoch_k > 85:
        return "skip"
    
    # Skip shorts when both BB and Stochastic confirm oversold extreme
    if prediction == "short" and bb_pct_b < 0.10 and stoch_k < 15:
        return "skip"
    
    return prediction