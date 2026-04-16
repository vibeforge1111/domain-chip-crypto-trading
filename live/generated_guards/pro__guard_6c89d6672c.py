def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # High-confidence entry zones: bb_pct_b at extremes (<0.05 or >0.95)
    if prediction == "long" and bb_pct_b > 0.05:
        return "skip"
    if prediction == "short" and bb_pct_b < 0.95:
        return "skip"
    
    return prediction