def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, vwap_deviation, stoch_k, stoch_d, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Only allow trades when bb_pct_b is in extreme zones (<0.05 or >0.95)
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction