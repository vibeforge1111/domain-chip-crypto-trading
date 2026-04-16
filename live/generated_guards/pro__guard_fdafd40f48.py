def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, vwap_deviation, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Reject longs when overbought: price near upper BB + stochastic above 80
    if prediction == "long" and bb_pct_b > 0.85 and stoch_k > 80:
        return "skip"
    
    # Reject shorts when oversold: price near lower BB + stochastic below 20
    if prediction == "short" and bb_pct_b < 0.15 and stoch_k < 20:
        return "skip"
    
    # Stochastic overbought with bearish confirmation
    if stoch_k > 85 and stoch_d > 85 and vwap_dev > 0.01:
        return "skip"
    
    # Stochastic oversold with bullish confirmation
    if stoch_k < 15 and stoch_d < 15 and vwap_dev < -0.01:
        return "skip"
    
    return prediction