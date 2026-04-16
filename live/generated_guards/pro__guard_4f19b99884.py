def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like stoch_k, stoch_d, bb_pct_b, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Reject signals when stochastic is in neutral zone (35-65)
    # Crossovers in this range often lack momentum conviction
    if 35 < stoch_k < 65 and 35 < stoch_d < 65:
        return "skip"
    
    return prediction