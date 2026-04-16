def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, rsi_2h, macd_histogram, vwap_deviation
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Detect overbought extremes: price at upper BB + overbought stoch + high 2h RSI
    overbought = bb_pct_b > 0.88 and stoch_k > 80 and rsi_2h > 65
    # Detect oversold extremes: price at lower BB + oversold stoch + low 2h RSI
    oversold = bb_pct_b < 0.12 and stoch_k < 20 and rsi_2h < 35
    
    if overbought or oversold:
        return "skip"
    
    return prediction