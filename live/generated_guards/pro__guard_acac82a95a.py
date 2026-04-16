def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like vwap_deviation, bb_pct_b, stoch_k, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    vwap_dev = abs(features.get('vwap_deviation', 0))
    
    # Skip if price is too close to VWAP (within 0.2% of price = low conviction)
    if vwap_dev < 0.002:
        return "skip"
    
    return prediction