def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, vwap_deviation, stoch_k, stoch_d, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # High-confidence entry zones: BB at extremes
    if prediction == "long" and (bb_pct_b >= 0.10 or stoch_k >= 40):
        return "skip"
    if prediction == "short" and (bb_pct_b <= 0.90 or stoch_k <= 60):
        return "skip"
    
    return prediction