def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like vwap_deviation, momentum_score, bb_pct_b, stoch_k, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Skip if strong disagreement: price above VWAP but bearish momentum
    if vwap_dev > 0.003 and momentum < -0.25:
        return "skip"
    
    # Skip if strong disagreement: price below VWAP but bullish momentum
    if vwap_dev < -0.003 and momentum > 0.25:
        return "skip"
    
    return prediction