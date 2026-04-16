def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, vwap_deviation, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    if prediction == "long" and bb_pct > 0.88 and stoch > 78:
        return "skip"
    if prediction == "short" and bb_pct < 0.12 and stoch < 22:
        return "skip"
    
    return prediction