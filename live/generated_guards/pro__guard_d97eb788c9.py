def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like vwap_deviation, bb_pct_b, stoch_k, stoch_d, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    # Filter trades too close to fair value (VWAP)
    if abs(features.get("vwap_deviation", 0)) < 0.005:
        return "skip"
    
    return prediction