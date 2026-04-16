def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Filter longs when overbought: both indicators confirm strength
    if prediction == "long" and stoch_k > 75 and bb_pct_b > 0.85:
        return "skip"
    
    # Filter shorts when oversold: both indicators confirm weakness
    if prediction == "short" and stoch_k < 25 and bb_pct_b < 0.15:
        return "skip"
    
    return prediction