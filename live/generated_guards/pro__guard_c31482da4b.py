def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like vwap_deviation, bb_pct_b, stoch_k, stoch_d, rsi_14, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Skip trades too close to VWAP (within 0.3% of fair value)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    return prediction