def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, vwap_deviation
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Skip long signals when both indicators show extreme overbought
    if prediction == "long" and stoch_k > 80 and bb_pct_b > 0.85:
        return "skip"
    
    # Skip short signals when both indicators show extreme oversold
    if prediction == "short" and stoch_k < 20 and bb_pct_b < 0.15:
        return "skip"
    
    return prediction