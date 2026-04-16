def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, vwap_deviation, stoch_k, stoch_d, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Reject longs when price is at upper band extreme
    if prediction == "long" and bb_pct_b > 0.95:
        return "skip"
    
    # Reject shorts when price is at lower band extreme
    if prediction == "short" and bb_pct_b < 0.05:
        return "skip"
    
    return prediction