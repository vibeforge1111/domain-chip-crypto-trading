def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like stoch_k, stoch_d, vwap_deviation, bb_pct_b
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    bb_pos = features.get("bb_pct_b", 0.5)
    
    if prediction == "long":
        if stoch_k > stoch_d:
            return "skip"
        if stoch_k > 60 or stoch_d > 60:
            return "skip"
        if vwap_dev < -0.005:
            return "skip"
    elif prediction == "short":
        if stoch_k < stoch_d:
            return "skip"
        if stoch_k < 40 or stoch_d < 40:
            return "skip"
        if vwap_dev > 0.005:
            return "skip"
    
    return prediction