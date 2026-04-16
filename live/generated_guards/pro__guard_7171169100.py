def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like stoch_k, stoch_d, bb_pct_b, vwap_deviation, obv_slope, macd_histogram, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    obv_slope = features.get("obv_slope", 0)
    
    if prediction == "long":
        if stoch_k > 30:
            return "skip"
        if stoch_k < stoch_d and vwap_dev < -0.002 and obv_slope > 0:
            return "skip"
    
    if prediction == "short":
        if stoch_k < 70:
            return "skip"
        if stoch_k > stoch_d and vwap_dev > 0.002 and obv_slope < 0:
            return "skip"
    
    return prediction