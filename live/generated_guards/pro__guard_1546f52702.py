def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like stoch_k, stoch_d, bb_pct_b, vwap_deviation
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_k > 70:
            return "skip"
    elif prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_k < 30:
            return "skip"
    
    return prediction