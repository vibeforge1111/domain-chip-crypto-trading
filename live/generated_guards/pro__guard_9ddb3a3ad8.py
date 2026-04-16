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
    
    if prediction == "long" and (stoch_k < stoch_d or stoch_k > 80):
        return "skip"
    if prediction == "short" and (stoch_k > stoch_d or stoch_k < 20):
        return "skip"
    
    return prediction