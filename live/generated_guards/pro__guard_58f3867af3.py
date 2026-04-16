def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, vwap_deviation, stoch_k, stoch_d, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Only allow trades at extreme BB positions (<0.05 or >0.95)
    if not (bb_pct_b < 0.05 or bb_pct_b > 0.95):
        return "skip"
    
    # Filter with RSI confirmation
    rsi_14 = features.get('rsi_14', 50)
    if prediction == "long" and rsi_14 > 45:
        return "skip"
    if prediction == "short" and rsi_14 < 55:
        return "skip"
    
    return prediction